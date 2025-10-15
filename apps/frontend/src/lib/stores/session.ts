import { writable } from 'svelte/store';
import type { UserOutput } from '$lib/types/api/user';

export interface Session {
	user: UserOutput;
	currentUserId: number | null;
}

export function deriveCurrentUserId(user: UserOutput | null | undefined): number | null {
	if (!user) return null;
	const parsed = Number.parseInt(user.id, 10);
	return Number.isNaN(parsed) ? null : parsed;
}

export function buildSession(user: UserOutput | null | undefined, currentUserId?: number | null) {
	if (!user) return null;
	return {
		user,
		currentUserId: currentUserId ?? deriveCurrentUserId(user)
	} satisfies Session;
}

export const session = writable<Session | null>(null);
