<script lang="ts">
	import { onMount } from 'svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import { m } from '$lib/paraglide/messages';
	import type { PetOut } from '$lib/types/api/pet';
	import { BACKEND_URL } from '$lib/config';

	export let pet: PetOut;

	let mounted = false;

	function printFlyer() {
		// Open the flyer in a new window using the backend endpoint
		const flyerWindow = window.open(`${BACKEND_URL}api/flyers/${pet.id}`, '_blank');
		if (flyerWindow) {
			// Wait for the page to load, then trigger print
			flyerWindow.onload = function () {
				flyerWindow.print();
			};
		}
	}

	function exportAsImage() {
		// Implementar exportación como imagen
		alert('Función de exportación como imagen próximamente disponible');
	}

	onMount(() => {
		mounted = true;
	});
</script>

<div class="flyer-generator">
	<div class="toolbar mb-4 flex gap-4">
		<button class="btn btn-primary" on:click={printFlyer}>
			🖨️ {getMessage('print_flyer')}
		</button>

		<button class="btn btn-secondary" on:click={exportAsImage}>
			📷 {getMessage('export_image')}
		</button>
	</div>

	<div class="flyer-preview overflow-hidden rounded-lg border bg-white">
		<iframe
			src={`${BACKEND_URL}api/flyers/${pet.id}`}
			class="h-full w-full border-0"
			title="Flyer Preview"
		></iframe>
	</div>
</div>

<style>
	/* Flyer preview container with A4 aspect ratio */
	.flyer-preview {
		width: 100%;
		max-width: 600px;
		margin: 0 auto;
		aspect-ratio: 210 / 297; /* A4 aspect ratio */
		position: relative;
		overflow: hidden;
		border-radius: 8px;
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
		background: #f8f9fa;
	}

	/* The iframe fills the preview container */
	.flyer-preview iframe {
		width: 100%;
		height: 100%;
		border: none;
		background: white;
	}
</style>
