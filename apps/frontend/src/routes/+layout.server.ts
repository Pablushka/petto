import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
	return {
		user: locals.user ?? null,
		currentUserId: typeof locals.currentUserId === 'number' ? locals.currentUserId : null
	};
};
