<script lang="ts">
	import { BACKEND_URL } from '$lib/config';
	import { getMessage } from '$lib/utils/message-helper';
	import type { PetOut } from '$lib/types/api/pet';
	import { session } from '$lib/stores/session';
	import Button from '../Button.svelte';
	import { goto } from '$app/navigation';

	const all = $props<{ pet: PetOut }>();
	let { pet } = all;

	// Subscribe to session
	let currentUserId: number | null = null;
	$effect(() => {
		const unsub = session.subscribe((s) => {
			currentUserId = s?.user ? Number(s.user.id) : null;
		});
		return unsub;
	});

	function onEdit() {
		goto(`/pets/${pet.id}/edit`);
	}

	// Derive image URL (fallback to placeholder)
	let petImageUrl = $derived(
		pet.picture
			? pet.picture.startsWith('http')
				? pet.picture
				: `${BACKEND_URL}${pet.picture}`
			: '/placeholder-pet.jpg'
	);

	let isOwner = $derived(currentUserId !== null && currentUserId === pet.owner_id);
</script>

<div class="overflow-hidden rounded-lg bg-white shadow-md">
	<div class="relative h-64 overflow-hidden">
		<img
			src={petImageUrl}
			alt={pet.name}
			class="h-full w-full object-cover"
			onerror={(e) => ((e.currentTarget as HTMLImageElement).src = '/placeholder-pet.jpg')}
		/>
	</div>

	<div class="p-6">
		<h1 class="mb-2 text-2xl font-bold text-gray-900">{pet.name}</h1>

		<div class="mt-4">
			<h2 class="mb-3 text-lg font-semibold text-gray-800">{getMessage('pet_details_title')}</h2>
			<ul class="space-y-2">
				<li class="flex">
					<span class="w-32 font-medium">Type</span>
					<span>{pet.pet_type}</span>
				</li>
				<li class="flex">
					<span class="w-32 font-medium">ID</span>
					<span>{pet.id}</span>
				</li>
			</ul>
		</div>

		{#if pet.notes}
			<div class="mt-6">
				<h2 class="mb-2 text-lg font-semibold text-gray-800">Notes</h2>
				<p class="whitespace-pre-line text-gray-700">{pet.notes}</p>
			</div>
		{/if}

		{#if isOwner}
			<div class="mt-8">
				<Button type="primary" onclick={onEdit}>Edit</Button>
			</div>
		{/if}
	</div>
</div>
