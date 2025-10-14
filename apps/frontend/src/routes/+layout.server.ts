import type { LayoutServerLoad } from './$types';
import { get, isUnauthorized } from '$lib/utils/api';
import type { UserOutput } from '$lib/types/api/user';
import {
	getAuthTokenFromCookies,
	getRefreshTokenFromCookies,
	setAuthCookies,
	clearAuthCookies
} from '$lib/utils/auth';

export const load: LayoutServerLoad = async ({ cookies, fetch, url }) => {
	if (
		url.pathname.startsWith('/login') ||
		url.pathname.startsWith('/register') ||
		url.pathname.startsWith('/forgot-password')
	) {
		return { user: null };
	}

	const authToken = getAuthTokenFromCookies(cookies);
	const refreshToken = getRefreshTokenFromCookies(cookies);

	try {
		const user = await get<UserOutput>('api/users/me', {
			requireAuth: true,
			fetchFn: fetch,
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
		return { user };
	} catch (error) {
		if (isUnauthorized(error)) {
			clearAuthCookies(cookies);
		}
		return { user: null };
	}
};
