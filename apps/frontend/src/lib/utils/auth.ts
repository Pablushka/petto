import { goto } from '$app/navigation';
import { session } from '$lib/stores/session';
import { get as getStore } from 'svelte/store';
import type { Cookies } from '@sveltejs/kit';
import type { UserOutput } from '$lib/types/api/user';
import { get } from './api';

export interface AuthTokens {
	access_token: string;
	refresh_token?: string | null;
}

export const ACCESS_TOKEN_COOKIE = 'access_token';
export const REFRESH_TOKEN_COOKIE = 'refresh_token';

const ACCESS_TOKEN_MAX_AGE = 60 * 60; // 1 hour, keep in sync with backend
const REFRESH_TOKEN_MAX_AGE = 3 * 24 * 60 * 60; // 3 days, keep in sync with backend
const COOKIE_PATH = '/';
const COOKIE_SAME_SITE = 'lax' as const;
const COOKIE_SECURE = import.meta.env?.MODE === 'production';

/**
 * Read auth token from cookies.
 * Returns access token string or null if not present.
 */
export function getAuthTokenFromCookies(cookies: Cookies): string | null {
	const token = cookies.get(ACCESS_TOKEN_COOKIE);
	return token ?? null;
}

export function getRefreshTokenFromCookies(cookies: Cookies): string | null {
	const token = cookies.get(REFRESH_TOKEN_COOKIE);
	return token ?? null;
}

export function setAuthCookies(cookies: Cookies, tokens: AuthTokens): void {
	cookies.set(ACCESS_TOKEN_COOKIE, tokens.access_token, {
		httpOnly: true,
		secure: COOKIE_SECURE,
		sameSite: COOKIE_SAME_SITE,
		path: COOKIE_PATH,
		maxAge: ACCESS_TOKEN_MAX_AGE
	});

	if (tokens.refresh_token) {
		cookies.set(REFRESH_TOKEN_COOKIE, tokens.refresh_token, {
			httpOnly: true,
			secure: COOKIE_SECURE,
			sameSite: COOKIE_SAME_SITE,
			path: COOKIE_PATH,
			maxAge: REFRESH_TOKEN_MAX_AGE
		});
	}
}

export function clearAuthCookies(cookies: Cookies): void {
	cookies.delete(ACCESS_TOKEN_COOKIE, { path: COOKIE_PATH });
	cookies.delete(REFRESH_TOKEN_COOKIE, { path: COOKIE_PATH });
}

/**
 * Check if the user is authenticated and redirect to login if not
 * @param redirectTo The path to redirect to after successful login
 * @returns True if authenticated, false if redirected
 */
export async function requireAuth(redirectTo?: string): Promise<boolean> {
	// Check if we already have a session in the store
	const currentSession = getStore(session);
	if (currentSession?.user) {
		return true;
	}

	// No session in store, try to fetch user data via cookies-backed request
	try {
		const userData = await get<UserOutput>('api/users/me', {
			requireAuth: true
		});

		// Valid user, set session and return true
		session.set({ user: userData });
		return true;
	} catch (error) {
		// Network error or other exception
		console.error('Authentication check failed:', error);
		redirectToLogin(redirectTo);
		return false;
	}
}

/**
 * Redirect to login page with optional return URL
 */
function redirectToLogin(returnUrl?: string): void {
	const loginPath = returnUrl ? `/login?returnUrl=${encodeURIComponent(returnUrl)}` : '/login';
	goto(loginPath);
}

export default getAuthTokenFromCookies;
