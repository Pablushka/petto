import { error } from '@sveltejs/kit';
import { get } from '$lib/utils/api';
import { mapToSvelteKitError } from '$lib/utils/error-mapper';
import type { PetOut } from '$lib/types/api/pet';
import { getMessage } from '$lib/utils/message-helper';
import { getAuthTokenFromCookies } from '$lib/utils/auth';

// allow any here because generated PageServerLoad type may not be available in some dev setups
/* eslint-disable @typescript-eslint/no-explicit-any */
export const load = async (event: any) => {
	/* eslint-enable @typescript-eslint/no-explicit-any */
	try {
		const { params, cookies, fetch } = event;
		const authToken = getAuthTokenFromCookies(cookies);
		const pet = await get<PetOut>(`api/pets/${params.id}`, {
			requireAuth: true,
			fetchFn: fetch,
			authToken
		});
		if (!pet) {
			throw error(404, 'Pet not found');
		}
		return { pet };
	} catch (e) {
		console.log('Error loading pet:', e);
		mapToSvelteKitError(e, (k: string) => getMessage(k as never));
	}
};
