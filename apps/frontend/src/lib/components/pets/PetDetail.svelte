<script lang="ts">
	import { BACKEND_URL } from '$lib/config';
	import { getMessage, type MessageKey } from '$lib/utils/message-helper';
	import { getPetCover } from '$lib/utils/pet';
	import type { PetOut } from '$lib/types/api/pet';
	import { session } from '$lib/stores/session';
	import Button from '../Button.svelte';
	import PetGallery from '../PetGallery.svelte';
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

	function onGenerateFlyer() {
		goto(`/pets/${pet.id}/flyer`);
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

	// Get all images including cover
	const allImages = $derived(() => {
		if (!pet.pictures || pet.pictures.length === 0) {
			return [petImageUrl];
		}
		return pet.pictures.map((pic: string) =>
			pic.startsWith('http') ? pic : `${BACKEND_URL}${pic}`
		);
	});
</script>

<div class="relative overflow-hidden rounded-lg bg-white shadow-md">
	<!-- Two-column layout on large screens -->
	<div class="lg:grid lg:grid-cols-2 lg:gap-6">
		<!-- Left column: Main Image & Gallery -->
		<div class="relative p-6 lg:p-6">
			{#if pet.status}
				<div class="mb-4">
					<span
						class="inline-block rounded bg-blue-600/90 px-3 py-1 text-xs font-semibold tracking-wide text-white uppercase shadow-lg"
					>
						{getMessage(statusMessageKey[pet.status])}
					</span>
				</div>
			{/if}

			<PetGallery images={allImages()} petName={pet.name} aspectRatio="square" />
		</div>

		<!-- Right column: Pet Details -->
		<div class="p-6 lg:p-0 lg:py-6 lg:pr-6">
			<h1 class="mb-2 text-2xl font-bold text-gray-900">{pet.name}</h1>

			<div class="mt-6">
				<h2 class="mb-3 text-lg font-semibold text-gray-800">{getMessage('pet_details_title')}</h2>
				<ul class="space-y-2">
					<li class="flex">
						<span class="w-32 font-medium">{getMessage('pet_species')}</span>
						<span>{pet.pet_type}</span>
					</li>
					{#if pet.breed}
						<li class="flex">
							<span class="w-32 font-medium">{getMessage('pet_breed')}</span>
							<span>{pet.breed}</span>
						</li>
					{/if}
					{#if pet.gender}
						<li class="flex">
							<span class="w-32 font-medium">{getMessage('pet_gender')}</span>
							<span>{pet.gender}</span>
						</li>
					{/if}
					<li class="flex">
						<span class="w-32 font-medium">ID</span>
						<span>{pet.id}</span>
					</li>
					{#if pet.last_seen_date}
						<li class="flex">
							<span class="w-32 font-medium">{getMessage('pet_date')}</span>
							<span>{pet.last_seen_date}</span>
						</li>
					{/if}
					{#if pet.last_seen_geo}
						<li class="flex">
							<span class="w-32 font-medium">{getMessage('pet_location')}</span>
							<span>{pet.last_seen_geo}</span>
						</li>
					{/if}
				</ul>
			</div>

			{#if pet.notes}
				<div class="mt-6">
					<h2 class="mb-2 text-lg font-semibold text-gray-800">
						{getMessage('pet_description')}
					</h2>
					<p class="whitespace-pre-line text-gray-700">{pet.notes}</p>
				</div>
			{/if}

			{#if pet.distinctive1 || pet.distinctive2 || pet.distinctive3 || pet.distinctive4}
				<div class="mt-6">
					<h2 class="mb-2 text-lg font-semibold text-gray-800">
						{getMessage('pet_distinctives')}
					</h2>
					<ul class="space-y-1 text-gray-700">
						{#if pet.distinctive1}
							<li>{pet.distinctive1}</li>
						{/if}
						{#if pet.distinctive2}
							<li>{pet.distinctive2}</li>
						{/if}
						{#if pet.distinctive3}
							<li>{pet.distinctive3}</li>
						{/if}
						{#if pet.distinctive4}
							<li>{pet.distinctive4}</li>
						{/if}
					</ul>
				</div>
			{/if}

			{#if isOwner}
				<div class="mt-8 flex flex-wrap gap-4">
					<Button type="primary" onclick={onEdit}>{getMessage('edit_pet')}</Button>
					<Button type="secondary" onclick={onGenerateFlyer}>{getMessage('print_flyer')}</Button>
				</div>
			{/if}

			{#if isOwner}
				<div class="mt-8 rounded-lg border border-gray-200 bg-gray-50 p-4">
					<h3 class="mb-3 text-sm font-semibold tracking-wide text-gray-700 uppercase">
						Share QR Code
					</h3>
					<div class="flex justify-center">
						<img
							src={petQrCodeUrl()}
							alt={`QR code for ${pet.name}`}
							loading="lazy"
							class="h-48 w-48 rounded border border-gray-200 bg-white p-2 shadow-sm lg:h-56 lg:w-56"
						/>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
