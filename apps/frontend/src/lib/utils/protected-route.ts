/**
 * Protected route utility for SvelteKit routes
 *
 * This module provides server-side route protection functionality through SvelteKit's
 * load function mechanism. It verifies user authentication before allowing access to
 * protected routes and handles redirects to login when authentication fails.
 *
 * @module protected-route
 */

import { redirect } from '@sveltejs/kit';
import type { LoadEvent } from '@sveltejs/kit';
import { get } from '$lib/utils/api';
import type { UserOutput } from '$lib/types/api/user';

/**
 * SvelteKit load function for protected routes
 *
 * This function implements route protection at the SvelteKit page load level.
 * It verifies the user's authentication token and performs validation against
 * the API before allowing access to the route.
 *
 * The function performs the following checks:
 * 1. Checks for the presence of an access token in localStorage
 * 2. Validates the token by making an API request to /api/users/me
 * 3. If valid, returns the user data for use in the protected route
 * 4. If invalid or missing, redirects to login with a return URL
 *
 * Example usage in a +page.ts file:
 * ```typescript
 * import { load } from '$lib/utils/protected-route';
 * export { load };
 * ```
 *
 * @param {LoadEvent} event - The SvelteKit load event object
 * @returns {Promise<{user: any}>} Object containing the authenticated user data
 * @throws {Redirect} Redirects to login page if authentication fails
 */
export async function load(event: LoadEvent) {
	const { url, fetch } = event;
	const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;

	if (!token) {
		throw redirect(302, `/login?returnUrl=${encodeURIComponent(url.pathname)}`);
	}

	try {
		const user = await get<UserOutput>('api/users/me', { requireAuth: true, fetchFn: fetch });
		return { user };
	} catch {
		// Any error will result in a redirect to login
		throw redirect(302, `/login?returnUrl=${encodeURIComponent(url.pathname)}`);
	}
}
