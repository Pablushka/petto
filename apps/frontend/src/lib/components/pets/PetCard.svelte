<script lang="ts">
	// 'm' not used here; import removed
	import { BACKEND_URL } from '$lib/config';
	import { getMessage, type MessageKey } from '$lib/utils/message-helper';
	import { getPetCover } from '$lib/utils/pet';
	import type { PetStatus as PetStatusEnum, PetOut } from '$lib/types/api/pet';

	const props = $props<{ pet: PetOut }>();
	let pet = props.pet;

	// Narrow status explicitly to satisfy index typing
	let petStatus: PetStatusEnum = pet.status;

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

	// Cover image using shared helper
	function resolveCover(): string {
		const c = getPetCover(pet);
		if (c.startsWith('http')) return c;
		const cleaned = c.replace(/^\/+/, '');
		return `${BACKEND_URL}${cleaned}`.replace(/([^:]\/)\/+/, '$1/');
	}

	let petImageUrl = $derived(resolveCover());
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
