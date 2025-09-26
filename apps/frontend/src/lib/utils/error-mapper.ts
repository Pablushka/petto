import { error as skError } from '@sveltejs/kit';
import {
	ApiError,
	isNotFound,
	isUnauthorized,
	isForbidden,
	isRateLimited,
	isServerError
} from './api';

/** Shape returned by mapper to throw or return */
export interface MappedError {
	status: number;
	message: string;
}

/**
 * Map arbitrary error to SvelteKit HTTP error semantics.
 * Customize mapping rules here (e.g., auth, rate limiting, etc.).
 */
export type Translator = (key: string) => string;

export function mapToSvelteKitError(e: unknown, t: Translator): never {
	if (isNotFound(e)) {
		throw skError(404, t('pet_not_found'));
	}
	if (e instanceof ApiError) {
		if (isUnauthorized(e)) {
			throw skError(401, t('error_unauthorized'));
		}
		if (isForbidden(e)) {
			throw skError(403, t('error_forbidden'));
		}
		if (isRateLimited(e)) {
			throw skError(429, t('error_rate_limited'));
		}
		if (isServerError(e)) {
			throw skError(500, t('error_server'));
		}
		// Fallback for other 4xx
		throw skError(e.status, t('error_request_failed'));
	}
	// Non-API errors
	throw skError(500, t('error_unexpected'));
}
