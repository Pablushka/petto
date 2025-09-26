import { redirect } from '@sveltejs/kit';
import type { Load } from '@sveltejs/kit';

/**
 * Server-side route protection that can be imported in route +page.ts files
 * Example usage:
 * ```
 * import { protectRoute } from '$lib/utils/protect-route';
 * export const load = protectRoute;
 * ```
 */
export const protectRoute: Load = async ({ url, parent }) => {
	// If using server-side rendering, we need to check server-side
	// Otherwise the client-side ProtectedRoute.svelte component will handle authentication
	// This function is for adding an extra layer of protection
	if (typeof window === 'undefined') {
		try {
			// Try to get data from the parent layout
			const data = await parent();

			// If user is not authenticated, redirect to login
			if (!data.user) {
				throw redirect(302, `/login?returnUrl=${encodeURIComponent(url.pathname)}`);
			}

			return { protected: true };
		} catch {
			// If any error occurs, redirect to login
			throw redirect(302, `/login?returnUrl=${encodeURIComponent(url.pathname)}`);
		}
	}

	// In client-side rendering, we'll let the ProtectedRoute component handle this
	return { protected: true };
};
