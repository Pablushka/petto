<script lang="ts">
	import { onMount } from 'svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import { m } from '$lib/paraglide/messages';
	import type { PetOut } from '$lib/types/api/pet';
	import { BACKEND_URL } from '$lib/config';

	export let pet: PetOut;
	export let flyerHtml: string;

	let mounted = false;

	// Extract the body content and styles from the HTML
	$: flyerContent = (() => {
		if (!flyerHtml) return '';
		
		// Extract content between <body> tags
		const bodyMatch = flyerHtml.match(/<body[^>]*>([\s\S]*)<\/body>/i);
		return bodyMatch ? bodyMatch[1] : flyerHtml;
	})();

	$: flyerStyles = (() => {
		if (!flyerHtml) return '';
		
		// Extract all <style> tags
		const styleMatches = flyerHtml.match(/<style[^>]*>([\s\S]*?)<\/style>/gi);
		if (!styleMatches) return '';
		
		// Combine all styles
		return styleMatches.map(style => {
			const content = style.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
			return content ? content[1] : '';
		}).join('\n');
	})();

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

<svelte:head>
	{#if flyerStyles}
		{@html `<style>${flyerStyles}</style>`}
	{/if}
</svelte:head>

<div class="flyer-generator">
	<div class="toolbar mb-4 flex gap-4">
		<button class="btn btn-primary" on:click={printFlyer}>
			🖨️ {getMessage('print_flyer')}
		</button>

		<button class="btn btn-secondary" on:click={exportAsImage}>
			📷 {getMessage('export_image')}
		</button>
	</div>

	<div class="flyer-preview-wrapper">
		<div class="flyer-preview">
			{@html flyerContent}
		</div>
	</div>
</div>

<style>
	.flyer-preview-wrapper {
		display: flex;
		justify-content: center;
		padding: 2rem 0;
		background: #f3f4f6;
	}

	/* Flyer preview container - simulates A4 paper */
	.flyer-preview {
		width: 210mm; /* A4 width */
		height: 297mm; /* A4 height */
		position: relative;
		overflow: hidden;
		border-radius: 4px;
		box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2), 0 8px 10px -6px rgba(0, 0, 0, 0.15);
		background: white;
		/* Scale down to fit on screen while maintaining aspect ratio */
		transform: scale(0.85);
		transform-origin: top center;
	}

	/* Ensure buttons have proper styling */
	.btn {
		padding: 0.5rem 1rem;
		border-radius: 0.375rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
		border: none;
	}

	.btn-primary {
		background-color: #3b82f6;
		color: white;
	}

	.btn-primary:hover {
		background-color: #2563eb;
	}

	.btn-secondary {
		background-color: #6b7280;
		color: white;
	}

	.btn-secondary:hover {
		background-color: #4b5563;
	}

	/* Responsive scaling for smaller screens */
	@media (max-width: 900px) {
		.flyer-preview {
			transform: scale(0.6);
		}
	}

	@media (max-width: 600px) {
		.flyer-preview {
			transform: scale(0.4);
		}
	}
</style>
