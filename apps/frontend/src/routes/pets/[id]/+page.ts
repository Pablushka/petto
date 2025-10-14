import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import { get } from '$lib/utils/api';
import { mapToSvelteKitError } from '$lib/utils/error-mapper';
import type { PetOut } from '$lib/types/api/pet';
import { getMessage } from '$lib/utils/message-helper';

export const load: PageLoad = async ({ params, fetch }) => {
	try {
		const pet = await get<PetOut>(`api/pets/${params.id}`, { requireAuth: true, fetchFn: fetch });
		if (!pet) {
			throw error(404, 'Pet not found');
		}
		return { pet };
	} catch (e) {
		console.log('Error loading pet:', e);
		mapToSvelteKitError(e, (k: string) => getMessage(k as never));
	}
};
