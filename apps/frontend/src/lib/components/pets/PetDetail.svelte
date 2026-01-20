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

	// Image gallery state
	let currentImageIndex = $state(0);
	let isLightboxOpen = $state(false);
	let isMainImageLoading = $state(true);
	let isMainImageHovered = $state(false);

	// Get all images including cover
	const allImages = $derived(() => {
		if (!pet.pictures || pet.pictures.length === 0) {
			return [petImageUrl];
		}
		return pet.pictures.map((pic: string) =>
			pic.startsWith('http') ? pic : `${BACKEND_URL}${pic}`
		);
	});

	function openLightbox(index: number) {
		currentImageIndex = index;
		isLightboxOpen = true;
		document.body.style.overflow = 'hidden';
	}

	function closeLightbox() {
		isLightboxOpen = false;
		document.body.style.overflow = '';
	}

	function nextImage() {
		currentImageIndex = (currentImageIndex + 1) % allImages().length;
	}

	function prevImage() {
		currentImageIndex = (currentImageIndex - 1 + allImages().length) % allImages().length;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!isLightboxOpen) return;
		if (e.key === 'Escape') closeLightbox();
		if (e.key === 'ArrowRight') nextImage();
		if (e.key === 'ArrowLeft') prevImage();
	}

	function selectImage(index: number) {
		currentImageIndex = index;
	}

	$effect(() => {
		if (typeof window !== 'undefined') {
			window.addEventListener('keydown', handleKeydown);
			return () => window.removeEventListener('keydown', handleKeydown);
		}
	});
</script>

<div class="relative overflow-hidden rounded-lg bg-white shadow-md">
	<!-- Two-column layout on large screens -->
	<div class="lg:grid lg:grid-cols-2 lg:gap-6">
		<!-- Left column: Main Image -->
		<div class="relative">
			<div
				class="relative aspect-video overflow-hidden bg-gray-100 md:aspect-[4/3] lg:aspect-square"
			>
				{#if isMainImageLoading}
					<div
						class="absolute inset-0 animate-pulse bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200"
					></div>
				{/if}

				<button
					type="button"
					onclick={() => openLightbox(currentImageIndex)}
					onmouseenter={() => (isMainImageHovered = true)}
					onmouseleave={() => (isMainImageHovered = false)}
					class="relative h-full w-full cursor-zoom-in transition-transform duration-300 {isMainImageHovered
						? 'scale-105'
						: 'scale-100'}"
				>
					<img
						src={allImages()[currentImageIndex]}
						alt={pet.name}
						class="h-full w-full object-cover transition-opacity duration-300"
						style="opacity: {isMainImageLoading ? 0 : 1}"
						onload={() => (isMainImageLoading = false)}
						onerror={(e) => {
							(e.currentTarget as HTMLImageElement).src = 'static/placeholder-pet.jpg';
							isMainImageLoading = false;
						}}
					/>

					<!-- Image counter overlay -->
					{#if allImages().length > 1}
						<div
							class="absolute right-4 bottom-4 rounded-full bg-black/60 px-3 py-1 text-sm font-medium text-white"
						>
							{currentImageIndex + 1} / {allImages().length}
						</div>
					{/if}

					<!-- Zoom hint on hover -->
					{#if isMainImageHovered}
						<div
							class="absolute inset-0 flex items-center justify-center bg-black/20 transition-opacity"
						>
							<svg
								class="h-12 w-12 text-white"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7"
								></path>
							</svg>
						</div>
					{/if}
				</button>

				{#if pet.status}
					<span
						class="absolute top-4 left-4 rounded bg-blue-600/90 px-3 py-1 text-xs font-semibold tracking-wide text-white uppercase shadow-lg"
					>
						{getMessage(statusMessageKey[pet.status])}
					</span>
				{/if}

				<!-- Navigation arrows for multiple images -->
				{#if allImages().length > 1}
					<button
						type="button"
						onclick={prevImage}
						class="absolute top-1/2 left-2 -translate-y-1/2 rounded-full bg-black/50 p-2 text-white transition-all hover:bg-black/70 focus:ring-2 focus:ring-white focus:outline-none"
						aria-label="Previous image"
					>
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M15 19l-7-7 7-7"
							></path>
						</svg>
					</button>
					<button
						type="button"
						onclick={nextImage}
						class="absolute top-1/2 right-2 -translate-y-1/2 rounded-full bg-black/50 p-2 text-white transition-all hover:bg-black/70 focus:ring-2 focus:ring-white focus:outline-none"
						aria-label="Next image"
					>
						<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"
							></path>
						</svg>
					</button>
				{/if}
			</div>
		</div>

		<!-- Right column: Pet Details -->
		<div class="p-6 lg:p-0 lg:py-6 lg:pr-6">
			<h1 class="mb-2 text-2xl font-bold text-gray-900">{pet.name}</h1>

			<!-- Enhanced Gallery with larger clickable thumbnails -->
			{#if allImages().length > 1}
				<div class="mt-6">
					<h2 class="mb-3 text-sm font-semibold tracking-wide text-gray-700 uppercase">
						Pet Photos ({allImages().length})
					</h2>
					<div class="grid grid-cols-4 gap-3 md:grid-cols-5 lg:grid-cols-4">
						{#each allImages() as pic, index (pic)}
							<button
								type="button"
								onclick={() => {
									selectImage(index);
									openLightbox(index);
								}}
								class="group relative aspect-square overflow-hidden rounded-lg border-2 transition-all {currentImageIndex ===
								index
									? 'border-blue-500 ring-2 ring-blue-200'
									: 'border-gray-200 hover:border-blue-300'}"
							>
								<img
									src={pic}
									alt={`${pet.name} photo ${index + 1}`}
									class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
								/>
								<!-- Overlay on hover -->
								<div class="absolute inset-0 bg-black/0 transition-all group-hover:bg-black/20">
									<div
										class="flex h-full items-center justify-center opacity-0 transition-opacity group-hover:opacity-100"
									>
										<svg
											class="h-8 w-8 text-white"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
											></path>
										</svg>
									</div>
								</div>
								<!-- Current image indicator -->
								{#if currentImageIndex === index}
									<div class="absolute right-1 bottom-1 rounded-full bg-blue-500 p-1">
										<svg class="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
											<path
												fill-rule="evenodd"
												d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
												clip-rule="evenodd"
											></path>
										</svg>
									</div>
								{/if}
							</button>
						{/each}
					</div>
				</div>
			{/if}

			<div class="mt-6">
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

<!-- Lightbox Modal -->
{#if isLightboxOpen}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 p-4"
		onclick={closeLightbox}
	>
		<!-- Close button -->
		<button
			type="button"
			onclick={closeLightbox}
			class="absolute top-4 right-4 rounded-full bg-white/10 p-2 text-white transition-colors hover:bg-white/20 focus:ring-2 focus:ring-white focus:outline-none"
			aria-label="Close"
		>
			<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M6 18L18 6M6 6l12 12"
				></path>
			</svg>
		</button>

		<!-- Image counter -->
		<div
			class="absolute top-4 left-1/2 -translate-x-1/2 rounded-full bg-white/10 px-4 py-2 text-white backdrop-blur-sm"
		>
			{currentImageIndex + 1} / {allImages().length}
		</div>

		<!-- Main lightbox image -->
		<div class="relative max-h-[90vh] max-w-[90vw]" onclick={(e) => e.stopPropagation()}>
			<img
				src={allImages()[currentImageIndex]}
				alt={`${pet.name} - Image ${currentImageIndex + 1}`}
				class="max-h-[90vh] max-w-[90vw] rounded object-contain shadow-2xl"
			/>
		</div>

		<!-- Navigation arrows -->
		{#if allImages().length > 1}
			<button
				type="button"
				onclick={(e) => {
					e.stopPropagation();
					prevImage();
				}}
				class="absolute top-1/2 left-4 -translate-y-1/2 rounded-full bg-white/10 p-3 text-white transition-colors hover:bg-white/20 focus:ring-2 focus:ring-white focus:outline-none"
				aria-label="Previous image"
			>
				<svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"
					></path>
				</svg>
			</button>
			<button
				type="button"
				onclick={(e) => {
					e.stopPropagation();
					nextImage();
				}}
				class="absolute top-1/2 right-4 -translate-y-1/2 rounded-full bg-white/10 p-3 text-white transition-colors hover:bg-white/20 focus:ring-2 focus:ring-white focus:outline-none"
				aria-label="Next image"
			>
				<svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"
					></path>
				</svg>
			</button>
		{/if}

		<!-- Thumbnail strip -->
		{#if allImages().length > 1}
			<div
				class="absolute bottom-4 left-1/2 max-w-[90vw] -translate-x-1/2 overflow-x-auto"
				onclick={(e) => e.stopPropagation()}
			>
				<div class="flex gap-2 rounded-lg bg-black/50 p-2 backdrop-blur-sm">
					{#each allImages() as pic, index (pic)}
						<button
							type="button"
							onclick={() => selectImage(index)}
							class="h-16 w-16 flex-shrink-0 overflow-hidden rounded border-2 transition-all {currentImageIndex ===
							index
								? 'border-white'
								: 'border-transparent opacity-60 hover:opacity-100'}"
						>
							<img src={pic} alt={`Thumbnail ${index + 1}`} class="h-full w-full object-cover" />
						</button>
					{/each}
				</div>
			</div>
		{/if}

		<!-- Keyboard hints -->
		<div class="absolute right-4 bottom-4 text-sm text-white/60">
			Press <kbd class="rounded bg-white/10 px-2 py-1">ESC</kbd> to close,
			<kbd class="rounded bg-white/10 px-2 py-1">←</kbd>
			<kbd class="rounded bg-white/10 px-2 py-1">→</kbd> to navigate
		</div>
	</div>
{/if}
