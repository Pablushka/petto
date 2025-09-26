<script lang="ts">
	import { m } from '$lib/paraglide/messages';
	import { BACKEND_URL } from '$lib/config';
	import { getMessage } from '$lib/utils/message-helper';
	import type { PetStatus as PetStatusEnum, PetOut } from '$lib/types/api/pet';

	const all = $props<{ pet: PetOut }>();
	let { pet } = all;

	// Narrow status explicitly to satisfy index typing
	let petStatus: PetStatusEnum = pet.status;

	// Define status badges colors
	const statusColors: Record<PetStatusEnum, string> = {
		lost: 'bg-red-100 text-red-800',
		found: 'bg-green-100 text-green-800',
		at_home: 'bg-blue-100 text-blue-800'
	};

	// Format the pet image URL with the backend URL if it's a relative path
	let petImageUrl = $derived(
		pet.picture
			? pet.picture.startsWith('http')
				? pet.picture
				: `${BACKEND_URL}${pet.picture}`
			: '/placeholder-pet.jpg'
	);
</script>

<a
	href={`/pets/${pet.id}`}
	class="block overflow-hidden rounded-lg bg-white shadow-md transition-shadow hover:shadow-lg"
>
	<div class="relative h-48 overflow-hidden">
		<img
			src={petImageUrl}
			alt={pet.name}
			class="h-full w-full object-cover"
			onerror={(e) => ((e.currentTarget as HTMLImageElement).src = '/placeholder-pet.jpg')}
		/>
		<div class="absolute top-2 right-2">
			{#if pet.status}
				<span class={`rounded-full px-2 py-1 text-xs font-medium ${statusColors[petStatus]}`}>
					{petStatus === 'lost'
						? getMessage('pet_status_lost')
						: petStatus === 'found'
							? getMessage('pet_status_found')
							: getMessage('pet_status_reunited')}
				</span>
			{/if}
		</div>
	</div>

	<div class="p-4">
		<h3 class="text-lg font-bold text-gray-900">{pet.name}</h3>

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
