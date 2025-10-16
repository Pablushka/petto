import type { PageServerLoad } from './$types';
import { get, isUnauthorized } from '$lib/utils/api';
import { mapToSvelteKitError } from '$lib/utils/error-mapper';
import type { PetLocationScan } from '$lib/types/api/location';
import { getMessage } from '$lib/utils/message-helper';

export const load: PageServerLoad = async ({ params, fetch }) => {
	try {
		const scans = await get<PetLocationScan[]>(`api/pet-location/pet/${params.id}/scans`, {
			requireAuth: true,
			fetchFn: fetch
		});
		// Get the last scan
		const lastScan = scans.length > 0 ? scans[scans.length - 1] : null;
		return { lastScan };
	} catch (e) {
		console.log('Error loading pet location:', e);
		if (isUnauthorized(e)) {
			throw new Error('Unauthorized');
		}
		mapToSvelteKitError(e, (k: string) => getMessage(k as never));
	}
};
