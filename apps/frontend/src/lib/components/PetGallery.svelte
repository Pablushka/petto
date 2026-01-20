<script lang="ts">
	import { getMessage } from '$lib/utils/message-helper';

	interface Props {
		images: string[];
		petName: string;
		aspectRatio?: 'square' | 'video';
	}

	let { images, petName, aspectRatio = 'square' }: Props = $props();

	let currentImageIndex = $state(0);
	let isLightboxOpen = $state(false);
	let isMainImageLoading = $state(true);
	let isMainImageHovered = $state(false);

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
		currentImageIndex = (currentImageIndex + 1) % images.length;
	}

	function prevImage() {
		currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
	}

	function selectImage(index: number) {
		currentImageIndex = index;
		isMainImageLoading = true;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!isLightboxOpen) return;
		if (e.key === 'Escape') closeLightbox();
		else if (e.key === 'ArrowLeft') prevImage();
		else if (e.key === 'ArrowRight') nextImage();
	}

	$effect(() => {
		return () => {
			document.body.style.overflow = '';
		};
	});

	const aspectClass =
		aspectRatio === 'square'
			? 'aspect-video md:aspect-[4/3] lg:aspect-square'
			: 'aspect-video md:aspect-[4/3]';
</script>

<svelte:window onkeydown={handleKeydown} />

<!-- Main Image Display -->
<div class="relative overflow-hidden rounded-lg shadow-md {aspectClass}">
	<!-- Loading skeleton -->
	{#if isMainImageLoading}
		<div
			class="absolute inset-0 animate-pulse bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 bg-[length:200%_100%]"
		></div>
	{/if}

	<!-- Main image -->
	<button
		type="button"
		class="group relative h-full w-full cursor-zoom-in overflow-hidden focus:ring-2 focus:ring-blue-500 focus:outline-none"
		onclick={() => openLightbox(currentImageIndex)}
		onmouseenter={() => (isMainImageHovered = true)}
		onmouseleave={() => (isMainImageHovered = false)}
	>
		<img
			src={images[currentImageIndex]}
			alt={petName}
			class="h-full w-full object-cover transition-all duration-300 {isMainImageHovered
				? 'scale-105'
				: 'scale-100'}"
			onload={() => (isMainImageLoading = false)}
		/>

		<!-- Zoom icon overlay on hover -->
		<div
			class="absolute inset-0 flex items-center justify-center bg-black/20 transition-opacity duration-200 {isMainImageHovered
				? 'opacity-100'
				: 'opacity-0'}"
		>
			<svg class="h-12 w-12 text-white drop-shadow-lg" fill="none" viewBox="0 0 24 24">
				<path
					stroke="currentColor"
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
				></path>
			</svg>
		</div>
	</button>

	<!-- Image counter badge -->
	{#if images.length > 1}
		<div class="absolute top-2 right-2 rounded-full bg-black/60 px-3 py-1 text-sm text-white">
			{currentImageIndex + 1} / {images.length}
		</div>
	{/if}

	<!-- Navigation arrows on main image -->
	{#if images.length > 1}
		<button
			type="button"
			onclick={(e) => {
				e.stopPropagation();
				prevImage();
			}}
			class="absolute top-1/2 left-2 -translate-y-1/2 rounded-full bg-black/50 p-2 text-white opacity-0 transition-opacity group-hover:opacity-100 hover:bg-black/70 focus:opacity-100 focus:ring-2 focus:ring-white focus:outline-none"
			aria-label="Previous image"
		>
			<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
			class="absolute top-1/2 right-2 -translate-y-1/2 rounded-full bg-black/50 p-2 text-white opacity-0 transition-opacity group-hover:opacity-100 hover:bg-black/70 focus:opacity-100 focus:ring-2 focus:ring-white focus:outline-none"
			aria-label="Next image"
		>
			<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"
				></path>
			</svg>
		</button>
	{/if}
</div>

<!-- Thumbnail Gallery (only show if there are multiple images) -->
{#if images.length > 1}
	<div class="mt-4">
		<h3 class="mb-2 text-sm font-medium text-gray-700">Gallery</h3>
		<div class="grid grid-cols-4 gap-2 lg:grid-cols-4">
			{#each images as pic, index (pic)}
				<button
					type="button"
					onclick={() => selectImage(index)}
					class="group relative aspect-square overflow-hidden rounded border-2 transition-all {currentImageIndex ===
					index
						? 'border-blue-500 ring-2 ring-blue-200'
						: 'border-gray-200 hover:border-blue-300'}"
				>
					<img
						src={pic}
						alt={`${petName} - Image ${index + 1}`}
						class="h-full w-full object-cover transition-transform group-hover:scale-110"
					/>

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

<!-- Lightbox Modal -->
{#if isLightboxOpen}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 p-4"
		onclick={closeLightbox}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
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
			{currentImageIndex + 1} / {images.length}
		</div>

		<!-- Main lightbox image -->
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div class="relative max-h-[90vh] max-w-[90vw]" onclick={(e) => e.stopPropagation()}>
			<img
				src={images[currentImageIndex]}
				alt={`${petName} - Image ${currentImageIndex + 1}`}
				class="max-h-[90vh] max-w-[90vw] rounded object-contain shadow-2xl"
			/>
		</div>

		<!-- Navigation arrows -->
		{#if images.length > 1}
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
		{#if images.length > 1}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div
				class="absolute bottom-4 left-1/2 max-w-[90vw] -translate-x-1/2 overflow-x-auto"
				onclick={(e) => e.stopPropagation()}
			>
				<div class="flex gap-2 rounded-lg bg-black/50 p-2 backdrop-blur-sm">
					{#each images as pic, index (pic)}
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
