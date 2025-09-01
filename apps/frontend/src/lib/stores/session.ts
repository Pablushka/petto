import { writable } from 'svelte/store';
import type { UserOutput } from '$lib/types/api/user';

export interface Session {
	user?: UserOutput;
}

export const session = writable<Session | null>(null);
