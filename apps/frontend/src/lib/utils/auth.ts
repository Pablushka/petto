import { goto } from '$app/navigation';
import { session } from '$lib/stores/session';
import { get as getStore } from 'svelte/store';
import { get } from './api';
import type { UserOutput } from '$lib/types/api/user';

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

	// No session in store, check if we have a token and try to fetch user data
	const accessToken = localStorage.getItem('access_token');
	if (!accessToken) {
		// No token, redirect to login
		redirectToLogin(redirectTo);
		return false;
	}

	// We have a token, try to fetch user data
	try {
		const userData = await get<UserOutput>('api/users/me', { requireAuth: true });

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
