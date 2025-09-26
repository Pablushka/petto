import type { Load } from '@sveltejs/kit';
import { get } from '$lib/utils/api';
import type { UserOutput } from '$lib/types/api/user';

export const load: Load = async ({ url, fetch }) => {
	// Skip authentication check for login/register pages
	if (
		url.pathname.startsWith('/login') ||
		url.pathname.startsWith('/register') ||
		url.pathname.startsWith('/forgot-password')
	) {
		return {
			user: null
		};
	}

	// Try to get the user's session
	const accessToken =
		typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;

	if (accessToken) {
		try {
			// Use centralized API helper to leverage refresh-on-401 behavior
			const user = await get<UserOutput>('api/users/me', { requireAuth: true, fetchFn: fetch });
			return { user };
		} catch (error) {
			console.error('Error fetching user:', error);
		}
	}

	return {
		user: null
	};
};
