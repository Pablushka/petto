<script lang="ts">
	// 'm' not used here; import removed
	import { BACKEND_URL } from '$lib/config';
	import { getMessage, type MessageKey } from '$lib/utils/message-helper';
	import { getPetCover } from '$lib/utils/pet';
	import type { PetStatus as PetStatusEnum, PetOut } from '$lib/types/api/pet';
	import { session } from '$lib/stores/session';
	import { put } from '$lib/utils/api';
	import { goto } from '$app/navigation';

	const props = $props<{ pet: PetOut }>();
	let pet = props.pet;

	// Narrow status explicitly to satisfy index typing
	let petStatus: PetStatusEnum = $state(pet.status);

	// Define status badges colors
	const statusColors: Record<PetStatusEnum, string> = {
		lost: 'bg-red-100 text-red-800',
		found: 'bg-green-100 text-green-800',
		at_home: 'bg-blue-100 text-blue-800'
	};

	const statusMessageKey: Record<PetStatusEnum, MessageKey> = {
		lost: 'pet_status_lost',
		found: 'pet_status_found',
		at_home: 'pet_status_at_home'
	};

	// Subscribe to session
	let currentUserId: number | null = null;
	$effect(() => {
		const unsub = session.subscribe((s) => {
			currentUserId = s?.currentUserId ?? null;
		});
		isOwner = currentUserId !== null && currentUserId === pet.owner_id;
		return unsub;
	});

	let isOwner = $derived(currentUserId !== null && currentUserId === pet.owner_id);

	// Cover image using shared helper
	function resolveCover(): string {
		const c = getPetCover(pet);
		if (c.startsWith('http')) return c;
		const cleaned = c.replace(/^\/+/, '');
		return `${BACKEND_URL}${cleaned}`.replace(/([^:]\/)\/+/, '$1/');
	}

	let petImageUrl = $derived(resolveCover());

	async function markAsLost(event: Event) {
		event.preventDefault();
		event.stopPropagation();
		try {
			await put(`api/pets/${pet.id}`, { status: 'lost' });
			pet.status = 'lost';
			petStatus = 'lost';
		} catch (error) {
			console.error('Failed to mark pet as lost:', error);
		}
	}

	async function markAsAtHome(event: Event) {
		event.preventDefault();
		event.stopPropagation();
		try {
			await put(`api/pets/${pet.id}`, { status: 'at_home' });
			pet.status = 'at_home';
			petStatus = 'at_home';
		} catch (error) {
			console.error('Failed to mark pet as at home:', error);
		}
	}

	function goToLocation(event: Event) {
		event.preventDefault();
		event.stopPropagation();
		goto(`/pets/${pet.id}/location`);
	}
</script>

<a
	href={`/pets/${pet.id}`}
	class="block overflow-hidden rounded-lg bg-white shadow-md transition-shadow hover:shadow-lg"
>
	<div class="relative h-48 overflow-hidden">
		<img src={petImageUrl} alt={pet.name} class="h-full w-full object-cover object-top" />

		<div class="absolute top-2 right-2">
			{#if pet.status}
				<span class={`rounded-full px-2 py-1 text-xs font-medium ${statusColors[petStatus]}`}>
					{getMessage(statusMessageKey[petStatus])}
				</span>
			{/if}
		</div>

		{#if isOwner && pet.status === 'at_home'}
			<button
				onclick={markAsLost}
				class="absolute right-2 bottom-2 flex h-15 w-15 items-center justify-center rounded-full bg-red-600 text-white shadow-lg transition-colors hover:bg-red-700"
				aria-label="Mark as lost"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-10 w-10"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
					/>
				</svg>
			</button>
		{:else if isOwner && pet.status === 'lost'}
			<button
				onclick={markAsAtHome}
				class="absolute right-2 bottom-2 flex h-10 w-10 items-center justify-center rounded-full bg-green-600 text-white shadow-lg transition-colors hover:bg-green-700"
				aria-label="Mark as at home"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
					/>
				</svg>
			</button>
		{:else if isOwner && pet.status === 'found'}
			<button
				onclick={goToLocation}
				class="absolute right-2 bottom-2 flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white shadow-lg transition-colors hover:bg-blue-700"
				aria-label="View location"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
					/>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
					/>
				</svg>
			</button>
		{/if}
	</div>

	<div class="p-4">
		<h3 class="text-lg font-bold text-gray-900 capitalize">{pet.name}</h3>

		<div class="mt-2 space-y-1 text-sm text-gray-600">
			<p>
				<span class="font-medium">Type:</span>
				{pet.pet_type}
			</p>
			{#if pet.notes}
				<p class="line-clamp-2 whitespace-pre-wrap">{pet.notes}</p>
			{/if}
		</div>
	</div>
</a>
