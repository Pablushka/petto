import { BACKEND_URL } from '$lib/config';
import { goto } from '$app/navigation';

/**
 * Error type for API failures, preserving HTTP status and optional parsed body
 */
export class ApiError<TBody = unknown> extends Error {
	status: number;
	body: TBody | null;
	constructor(status: number, message: string, body: TBody | null = null) {
		super(message);
		this.status = status;
		this.body = body;
	}
}

/** Convenience type guard for 404 errors */
export function isNotFound(e: unknown): e is ApiError {
	return e instanceof ApiError && e.status === 404;
}

/** Convenience type guard for 401 errors */
export function isUnauthorized(e: unknown): e is ApiError {
	return e instanceof ApiError && e.status === 401;
}

/** Convenience type guard for 403 errors */
export function isForbidden(e: unknown): e is ApiError {
	return e instanceof ApiError && e.status === 403;
}

/** Convenience type guard for 429 errors */
export function isRateLimited(e: unknown): e is ApiError {
	return e instanceof ApiError && e.status === 429;
}

/** Convenience type guard for 5xx server errors */
export function isServerError(e: unknown): e is ApiError {
	return e instanceof ApiError && e.status >= 500;
}

/**
 * Interface for API request options
 */
export interface ApiRequestOptions {
	method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
	body?: unknown;
	headers?: Record<string, string>;
	requireAuth?: boolean;
	contentType?: 'json' | 'form-data' | 'text';
	/** Optional explicit auth token to use for the request (preferred over localStorage) */
	authToken?: string | null;
	/** Optional explicit refresh token (e.g., from HTTP-only cookies in SSR). */
	refreshToken?: string | null;
	/** Callback to persist refreshed tokens (e.g., updating cookies). */
	onTokens?: (
		tokens: { access_token: string; refresh_token?: string | null } | null
	) => void | Promise<void>;
	// Optional: use SvelteKit's load-provided fetch in load functions to avoid warnings
	fetchFn?: typeof fetch;
	/** Optional fetch credentials mode (defaults to 'include' to support cookies). */
	credentials?: RequestCredentials;
}

/**
 * Default options for API requests
 */
const defaultOptions: ApiRequestOptions = {
	method: 'GET',
	requireAuth: false,
	contentType: 'json'
};

/**
 * Makes an API request with appropriate headers and authentication
 * @param endpoint The API endpoint to call (without the base URL)
 * @param options Request options
 * @returns Promise with the response
 */

export async function apiRequest<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
	// Merge options with defaults
	const requestOptions: ApiRequestOptions = { ...defaultOptions, ...options };
	const doFetch = requestOptions.fetchFn ?? fetch;

	// requestOptions.requireAuth = true;
	// Build headers
	const headers: Record<string, string> = {
		...requestOptions.headers
	};

	// Add content-type header if not form-data
	if (requestOptions.contentType === 'json' && requestOptions.body) {
		headers['Content-Type'] = 'application/json';
	} else if (requestOptions.contentType === 'text') {
		headers['Content-Type'] = 'text/plain';
	}

	const isBrowser = typeof window !== 'undefined';
	let bearerToken: string | null = null;
	if (requestOptions.requireAuth) {
		if (requestOptions.authToken) {
			bearerToken = requestOptions.authToken;
		}
		if (bearerToken) {
			headers['Authorization'] = `Bearer ${bearerToken}`;
		}
	}

	// Prepare request body
	let body: string | FormData | null = null;
	if (requestOptions.body) {
		if (requestOptions.contentType === 'json' && typeof requestOptions.body !== 'string') {
			body = JSON.stringify(requestOptions.body);
		} else if (requestOptions.body instanceof FormData) {
			body = requestOptions.body;
		} else if (typeof requestOptions.body === 'string') {
			body = requestOptions.body;
		}
	}

	// Ensure endpoint starts with a slash if it doesn't already
	const normalizedEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;

	// Build full URL
	const url = `${BACKEND_URL}${normalizedEndpoint}`;

	const credentials = requestOptions.credentials ?? ('include' as RequestCredentials);

	const executeRequest = () =>
		doFetch(url, {
			method: requestOptions.method,
			headers,
			body,
			credentials
		});

	const callOnTokens = async (
		tokens: { access_token: string; refresh_token?: string | null } | null
	) => {
		if (requestOptions.onTokens) {
			await requestOptions.onTokens(tokens);
		}
	};

	const attemptServerRefresh = async () => {
		if (!requestOptions.refreshToken) {
			await callOnTokens(null);
			return null;
		}
		const refreshUrl = `${BACKEND_URL}${'api/token/refresh'}`;
		const refreshResp = await doFetch(refreshUrl, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ refresh_token: requestOptions.refreshToken }),
			credentials
		});
		if (!refreshResp.ok) {
			await callOnTokens(null);
			return null;
		}
		const tokens = (await refreshResp.json()) as {
			access_token?: string;
			refresh_token?: string | null;
		};
		if (!tokens.access_token) {
			await callOnTokens(null);
			return null;
		}
		const normalized = {
			access_token: tokens.access_token,
			refresh_token: tokens.refresh_token ?? null
		};
		await callOnTokens(normalized);
		headers['Authorization'] = `Bearer ${normalized.access_token}`;
		return normalized;
	};

	const attemptBrowserRefresh = async () => {
		const refreshUrl = `${BACKEND_URL}${'api/token/refresh'}`;
		const refreshResp = await doFetch(refreshUrl, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({}),
			credentials
		});
		if (!refreshResp.ok) {
			await callOnTokens(null);
			goto('/login');
			return null;
		}
		const tokens = (await refreshResp.json()) as {
			access_token?: string;
			refresh_token?: string | null;
		};
		if (!tokens.access_token) {
			await callOnTokens(null);
			goto('/login');
			return null;
		}
		const normalized = {
			access_token: tokens.access_token,
			refresh_token: tokens.refresh_token ?? null
		};
		await callOnTokens(normalized);
		return normalized;
	};

	// Make the request
	let response = await executeRequest();

	// If unauthorized, attempt to refresh tokens depending on environment
	if (response.status === 401 && requestOptions.requireAuth) {
		if (isBrowser) {
			const refreshed = await attemptBrowserRefresh();
			if (!refreshed) {
				throw new Error('Unauthorized - Redirected to login');
			}
			headers['Authorization'] = `Bearer ${refreshed.access_token}`;
			response = await executeRequest();
		} else {
			const refreshed = await attemptServerRefresh();
			if (!refreshed) {
				throw new ApiError(401, 'Unauthorized');
			}
			headers['Authorization'] = `Bearer ${refreshed.access_token}`;
			response = await executeRequest();
		}
	}

	// Throw error for bad responses with structured info
	if (!response.ok) {
		let errorBody: unknown = null;
		const contentType = response.headers.get('content-type') || '';
		try {
			if (contentType.includes('application/json')) {
				errorBody = await response.json();
			} else {
				errorBody = await response.text();
			}
		} catch {
			// ignore body parse errors
		}
		throw new ApiError(
			response.status,
			`API request failed: ${response.status} ${response.statusText}`,
			errorBody
		);
	}

	// Parse response based on content type
	if (response.headers.get('content-type')?.includes('application/json')) {
		return (await response.json()) as T;
	} else {
		// Return text or blob as needed
		return (await response.text()) as unknown as T;
	}
}

/**
 * GET request helper
 */
export function get<T>(
	endpoint: string,
	options: Omit<ApiRequestOptions, 'method'> = {}
): Promise<T> {
	return apiRequest<T>(endpoint, { ...options, method: 'GET' });
}

/**
 * POST request helper
 */
export function post<T>(
	endpoint: string,
	body?: unknown,
	options: Omit<ApiRequestOptions, 'method' | 'body'> = {}
): Promise<T> {
	return apiRequest<T>(endpoint, { ...options, method: 'POST', body });
}

/**
 * PUT request helper
 */
export function put<T>(
	endpoint: string,
	body?: unknown,
	options: Omit<ApiRequestOptions, 'method' | 'body'> = {}
): Promise<T> {
	return apiRequest<T>(endpoint, { ...options, method: 'PUT', body });
}

/**
 * DELETE request helper
 */
export function del<T>(
	endpoint: string,
	options: Omit<ApiRequestOptions, 'method'> = {}
): Promise<T> {
	return apiRequest<T>(endpoint, { ...options, method: 'DELETE' });
}

/**
 * PATCH request helper
 */
export function patch<T>(
	endpoint: string,
	body?: unknown,
	options: Omit<ApiRequestOptions, 'method' | 'body'> = {}
): Promise<T> {
	return apiRequest<T>(endpoint, { ...options, method: 'PATCH', body });
}

/**
 * Upload a single image file to the backend /api/upload endpoint.
 * Returns the JSON containing the URL string.
 */
export async function uploadImage(file: File): Promise<{ url: string }> {
	const formData = new FormData();
	formData.append('image', file);
	return post<{ url: string }>('api/upload', formData, {
		requireAuth: true,
		contentType: 'form-data'
	});
}
