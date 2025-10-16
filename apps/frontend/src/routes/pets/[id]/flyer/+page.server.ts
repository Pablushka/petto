import { error } from '@sveltejs/kit';
import { get, isUnauthorized } from '$lib/utils/api';
import type { PetOut } from '$lib/types/api/pet';
import {
	getAuthTokenFromCookies,
	getRefreshTokenFromCookies,
	setAuthCookies,
	clearAuthCookies
} from '$lib/utils/auth';

// allow any here because generated PageServerLoad type may not be available in some dev setups
/* eslint-disable @typescript-eslint/no-explicit-any */
export const load = async (event: any) => {
	/* eslint-enable @typescript-eslint/no-explicit-any */
	try {
		const { params, cookies, fetch } = event;
		const authToken = getAuthTokenFromCookies(cookies);
		const refreshToken = getRefreshTokenFromCookies(cookies);
		const pet = await get<PetOut>(`api/pets/${params.id}`, {
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

		// For now, we'll create a mock owner object since the API doesn't return full owner details
		// In a real implementation, you'd need an endpoint to get owner details or modify the pet endpoint
		const owner = {
			first_name: 'Juan',
			last_name: 'Pérez',
			phone: '+1234567890',
			email: 'juan@example.com',
			full_address: 'Calle Principal 123, Ciudad, País',
			recovery_bounty: 50.0
		};

		return {
			pet,
			owner
		};
	} catch (err) {
		if (isUnauthorized(err)) {
			error(401, 'Unauthorized');
		}
		error(500, 'Error loading pet data');
	}
};
