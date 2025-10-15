<script lang="ts">
	import { BACKEND_URL } from '$lib/config';
	import { getMessage, type MessageKey } from '$lib/utils/message-helper';
	import { getPetCover } from '$lib/utils/pet';
	import type { PetOut } from '$lib/types/api/pet';
	import { session } from '$lib/stores/session';
	import Button from '../Button.svelte';
	import { goto } from '$app/navigation';

	const all = $props<{ pet: PetOut }>();
	let { pet } = all;

	// Subscribe to session
	let currentUserId: number | null = null;
	let isOwner = $derived(currentUserId !== null && currentUserId === pet.owner_id);

	$effect(() => {
		const unsub = session.subscribe((s) => {
			currentUserId = s?.currentUserId ?? null;
			isOwner = currentUserId !== null && currentUserId === pet.owner_id;
		});
		return unsub;
	});

	function onEdit() {
		goto(`/pets/${pet.id}/edit`);
	}

	// Derive image URL using shared helper
	function resolveCover(): string {
		const cover = getPetCover(pet);
		if (cover.startsWith('http')) return cover;
		const cleaned = cover.replace(/^\/+/, '');
		return `${BACKEND_URL}${cleaned}`.replace(/([^:]\/)\/+/, '$1/');
	}

	let petImageUrl = $derived(resolveCover());

	const petQrCodeUrl = $derived(() => `${BACKEND_URL}api/qrcode/${pet.id}`);

	const statusMessageKey: Record<string, MessageKey> = {
		lost: 'pet_status_lost',
		found: 'pet_status_found',
		at_home: 'pet_status_at_home'
	};
</script>

<div class="relative overflow-hidden rounded-lg bg-white shadow-md">
	<div class="relative h-64 overflow-hidden">
		<img
			src={petImageUrl}
			alt={pet.name}
			class="h-full w-full object-cover object-top"
			onerror={(e) => ((e.currentTarget as HTMLImageElement).src = 'static/placeholder-pet.jpg')}
		/>
		{#if pet.status}
			<span
				class="absolute top-4 left-4 rounded bg-blue-600/80 px-3 py-1 text-xs font-semibold tracking-wide text-white uppercase"
			>
				{getMessage(statusMessageKey[pet.status])}
			</span>
		{/if}
	</div>

	<div class="p-6">
		<h1 class="mb-2 text-2xl font-bold text-gray-900">{pet.name}</h1>

		{#if pet.pictures && pet.pictures.length > 1}
			<div class="mt-4">
				<h2 class="mb-2 text-sm font-semibold text-gray-700">Gallery</h2>
				<div class="grid grid-cols-4 gap-2 md:grid-cols-6">
					{#each pet.pictures.slice(1) as pic, gi (pic)}
						{#if pic}
							<img
								src={`${BACKEND_URL}${pic}`}
								alt={`Extra ${gi + 2}`}
								class="h-16 w-full rounded object-cover"
							/>
						{/if}
					{/each}
				</div>
			</div>
		{/if}

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
		{#if isOwner}
			<h1>Is Owner</h1>
			<div
				class="pointer-events-none absolute right-6 bottom-6 flex flex-col items-center text-sm text-gray-600"
			>
				<span class="mb-2 rounded bg-white/90 px-2 py-1 font-medium text-gray-800 shadow-sm"
					>Share QR Code</span
				>
				<img
					src={petQrCodeUrl()}
					alt={`QR code for ${pet.name}`}
					loading="lazy"
					class="pointer-events-auto h-56 w-56 rounded border border-gray-200 bg-white p-2 shadow-lg"
				/>
			</div>
		{/if}
	</div>
</div>
