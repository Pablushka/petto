import type { Handle } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';
import { paraglideMiddleware } from '$lib/paraglide/server';
import { get, isUnauthorized } from '$lib/utils/api';
import type { UserOutput } from '$lib/types/api/user';
import {
	getAuthTokenFromCookies,
	getRefreshTokenFromCookies,
	setAuthCookies,
	clearAuthCookies
} from '$lib/utils/auth';

const ALLOWED_RESPONSE_HEADERS = new Set([
	'content-type',
	'content-length',
	'cache-control',
	'content-language',
	'expires',
	'last-modified',
	'pragma',
	'vary',
	'x-total-count',
	'link'
]);

const authHandle: Handle = async ({ event, resolve }) => {
	// Default locals before attempting to authenticate
	event.locals.user = null;
	event.locals.currentUserId = null;

	const { cookies, request, url } = event;
	const pathname = url.pathname;
	if (pathname.startsWith('/_app/') || pathname.startsWith('/static/')) {
		return resolve(event);
	}

	const accept = request.headers.get('accept') ?? '';
	const shouldCheckAuth = accept.includes('text/html') || accept.includes('application/json');

	if (!shouldCheckAuth) {
		return resolve(event);
	}

	const authToken = getAuthTokenFromCookies(cookies);
	const refreshToken = getRefreshTokenFromCookies(cookies);

	if (!authToken && !refreshToken) {
		return resolve(event);
	}

	try {
		const user = await get<UserOutput>('api/users/me', {
			requireAuth: true,
			fetchFn: event.fetch,
			authToken,
			refreshToken,
			onTokens: (tokens) => {
				if (!tokens) {
					clearAuthCookies(cookies);
				} else {
					setAuthCookies(cookies, tokens);
				}
			}
		});
		event.locals.user = user;
		const parsedId = Number.parseInt(user.id, 10);
		event.locals.currentUserId = Number.isNaN(parsedId) ? null : parsedId;
	} catch (error) {
		if (isUnauthorized(error)) {
			clearAuthCookies(cookies);
		}
		// leave locals as null when unauthorized or other errors occur
	}

	return resolve(event);
};

const handleParaglide: Handle = ({ event, resolve }) =>
	paraglideMiddleware(event.request, ({ request, locale }) => {
		event.request = request;

		return resolve(event, {
			filterSerializedResponseHeaders: (name) => ALLOWED_RESPONSE_HEADERS.has(name.toLowerCase()),
			transformPageChunk: ({ html }) => html.replace('%paraglide.lang%', locale)
		});
	});

export const handle: Handle = sequence(authHandle, handleParaglide);
