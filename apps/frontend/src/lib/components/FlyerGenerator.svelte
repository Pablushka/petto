<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getMessage } from '$lib/utils/message-helper';
	import { m } from '$lib/paraglide/messages';
	import type { PetOut } from '$lib/types/api/pet';
	import { getPetCover } from '$lib/utils/pet';
	import { BACKEND_URL } from '$lib/config';

	export let pet: PetOut;
	export let owner: {
		first_name: string;
		last_name: string;
		phone: string;
		email: string;
		full_address: string;
		recovery_bounty?: number;
	};

	let flyerContainer: HTMLElement;
	let isEditing = true;
	let printMode: 'color' | 'bw' = 'color'; // Modo de impresión: color o blanco y negro
	let flyerHtml = '';
	let mounted = false;

	// Función para resolver URLs absolutas
	function resolveImageUrl(url: string): string {
		if (url.startsWith('http')) return url;
		const cleaned = url.replace(/^\/+/, '');
		return `${BACKEND_URL}${cleaned}`.replace(/([^:]\/)\/+/, '$1/');
	}

	// Cargar la plantilla HTML
	async function loadTemplate() {
		if (!browser) {
			console.warn('Cannot load template during SSR');
			return null;
		}
		try {
			const response = await fetch('/flyers_templates/lost_pet_flyer.html');
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const template = await response.text();
			return template;
		} catch (error) {
			console.error('Error loading flyer template:', error);
			return null;
		}
	}

	// Función para renderizar el flyer con los datos
	async function renderFlyer() {
		const template = await loadTemplate();
		if (!template) return;

		// Datos del flyer
		const data = {
			pet_name: pet.name,
			pet_type: pet.pet_type,
			pet_age: '',
			pet_breed: '',
			pet_color: '',
			pet_gender: '',
			pet_last_seen: '',
			pet_location: '',
			pet_description: pet.notes || '',
			pet_picture: resolveImageUrl(getPetCover(pet)),
			pet_picture2: pet.pictures && pet.pictures.length > 1 ? resolveImageUrl(pet.pictures[1]) : '',
			pet_picture3: pet.pictures && pet.pictures.length > 2 ? resolveImageUrl(pet.pictures[2]) : '',
			pet_picture4: pet.pictures && pet.pictures.length > 3 ? resolveImageUrl(pet.pictures[3]) : '',
			pet_picture5: pet.pictures && pet.pictures.length > 4 ? resolveImageUrl(pet.pictures[4]) : '',
			qr_code_url: `${BACKEND_URL}api/qrcode/${pet.id}`,
			owner_name: `${owner.first_name} ${owner.last_name}`,
			owner_phone: owner.phone,
			owner_email: owner.email,
			owner_address: owner.full_address,
			reward_amount: owner.recovery_bounty ? `$${owner.recovery_bounty}` : '',
			show_reward: !!owner.recovery_bounty,
			print_mode: printMode,
			pet_id: pet.id
		};

		// Reemplazar variables en la plantilla
		let html = template;
		Object.entries(data).forEach(([key, value]) => {
			const regex = new RegExp(`{{ ${key} }}`, 'g');
			html = html.replace(regex, String(value));
		});

		// Manejar condicionales simples
		html = html.replace(/{% if (\w+) %}/g, (match, varName) => {
			return (data as any)[varName] ? '' : '<!-- ';
		});
		html = html.replace(/{% endif %}/g, (match) => {
			return ' -->';
		});

		flyerHtml = html;
	}

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

	function toggleEdit() {
		isEditing = !isEditing;
		const editableElements = flyerContainer?.querySelectorAll('[contenteditable]');
		editableElements?.forEach((el) => {
			(el as HTMLElement).contentEditable = isEditing ? 'true' : 'false';
		});
	}

	function togglePrintMode() {
		printMode = printMode === 'color' ? 'bw' : 'color';
		if (mounted) {
			renderFlyer();
		}
	}

	onMount(() => {
		mounted = true;
		// Inicializar el estado de edición
		toggleEdit();
		// Renderizar el flyer inicial
		renderFlyer();
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

		<button class="btn btn-outline" on:click={togglePrintMode}>
			{#if printMode === 'color'}
				🎨 {getMessage('color_mode')}
			{:else}
				⚪ {getMessage('bw_mode')}
			{/if}
		</button>

		<button class="btn btn-outline" on:click={toggleEdit}>
			{#if isEditing}
				🔒 {getMessage('finish_editing')}
			{:else}
				✏️ {getMessage('edit_flyer')}
			{/if}
		</button>
	</div>

	<div class="flyer-preview overflow-hidden rounded-lg border bg-white">
		<div
			bind:this={flyerContainer}
			class="flyer-content {printMode === 'bw' ? 'print-mode-bw' : 'print-mode-color'}"
		>
			{@html flyerHtml}
		</div>
	</div>
</div>

<style>
	.flyer-content {
		width: 210mm;
		min-height: 297mm;
		padding: 15mm;
		margin: 0 auto;
		background: white;
		font-family:
			'Inter',
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			sans-serif;
		font-size: 14px;
		line-height: 1.5;
		position: relative;
		transition: all 0.3s ease;
	}

	/* Modo Color - Diseño moderno y vibrante */
	.print-mode-color {
		background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
	}

	.print-mode-color .header-section {
		background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
		color: white;
		box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.1);
	}

	.print-mode-color .photo-frame {
		border: 3px solid #e5e7eb;
		box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
		background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
	}

	.print-mode-color .photo-gallery-item {
		border: 2px solid #e5e7eb;
		background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	.print-mode-color .photo-gallery-item:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 12px -2px rgba(0, 0, 0, 0.15);
	}

	.print-mode-color .qr-section {
		background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
		border: 2px solid #374151;
		color: white;
	}

	.print-mode-color .contact-section {
		background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
		border: 1px solid #93c5fd;
	}

	.print-mode-color .reward-section {
		background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
		border-left: 4px solid #f59e0b;
		box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
	}

	.print-mode-color .footer {
		margin-top: auto;
		text-align: center;
		font-size: 0.75rem;
		line-height: 1rem;
		color: #6b7280;
	}

	.print-mode-color ~ .cut-tabs .tab {
		background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
		box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
	}

	/* Modo Blanco y Negro - Alto contraste y legibilidad */
	.print-mode-bw {
		background: white;
		filter: grayscale(100%);
	}

	.print-mode-bw .header-section {
		background: #000000;
		color: white;
		border: 2px solid #000000;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
	}

	.print-mode-bw .photo-frame {
		border: 3px solid #333333;
		background: white;
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	}

	.print-mode-bw .photo-gallery-item {
		border: 2px solid #666666;
		background: #f8f8f8;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
	}

	.print-mode-bw .qr-section {
		background: #000000;
		border: 3px solid #000000;
		color: white;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
	}

	.print-mode-bw .contact-section {
		background: #f0f0f0;
		border: 2px solid #666666;
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.print-mode-bw .reward-section {
		background: #e8e8e8;
		border-left: 4px solid #333333;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.print-mode-bw .footer {
		margin-top: auto;
		text-align: center;
		font-size: 0.75rem;
		line-height: 1rem;
		color: #666666;
	}

	.print-mode-bw ~ .cut-tabs .tab {
		background: #000000;
		border: 1px solid #333333;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}

	/* Estilos comunes para ambos modos */
	.header-section {
		border-radius: 12px;
		font-weight: 700;
		font-size: 18px;
		text-align: center;
		padding: 16px;
		margin-bottom: 20px;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.photo-frame {
		border-radius: 12px;
		overflow: hidden;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.photo-frame img {
		max-width: 100%;
		max-height: 100%;
		object-fit: cover;
		filter: contrast(1.1) brightness(1.05);
	}

	.photo-gallery-item {
		border-radius: 8px;
		overflow: hidden;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.photo-gallery-item img {
		max-width: 100%;
		max-height: 100%;
		object-fit: cover;
		filter: contrast(1.05) brightness(1.02);
	}

	.qr-section {
		border-radius: 12px;
		padding: 16px;
		display: flex;
		align-items: center;
		gap: 16px;
		margin: 24px 0;
		font-weight: 600;
	}

	.qr-section img {
		border-radius: 8px;
		filter: contrast(1.2);
	}

	.contact-section {
		border-radius: 12px;
		padding: 16px;
		margin: 16px 0;
		font-weight: 500;
	}

	.reward-section {
		border-radius: 8px;
		padding: 12px 16px;
		margin: 16px 0;
		font-weight: 600;
	}

	.footer {
		margin-top: auto;
		text-align: center;
		font-size: 0.75rem;
		line-height: 1rem;
	}

	.cut-tabs .tab {
		border-radius: 4px 4px 0 0;
		font-size: 10px;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		padding: 4px 8px;
		min-width: 40px;
		text-align: center;
	}

	/* Mejoras de tipografía para impresión */
	@media print {
		.toolbar {
			display: none;
		}
		.flyer-preview {
			border: none;
			box-shadow: none;
		}
		.flyer-content {
			box-shadow: none;
			filter: none !important; /* Asegurar que el filtro se aplique solo en pantalla */
		}
		[contenteditable] {
			outline: none !important;
			background: transparent !important;
		}

		/* Forzar colores específicos para impresión según el modo */
		.print-mode-color {
			filter: none !important;
		}

		.print-mode-bw {
			filter: none !important;
		}
	}

	/* Responsive adjustments */
	@media (max-width: 1024px) and (min-width: 769px) {
		/* Medium screens (tablets) */
		.flyer-content {
			width: 90%;
			max-width: 600px;
			padding: 12mm;
		}

		.header-section {
			font-size: 18px;
			padding: 14px;
		}

		.photo-frame {
			height: 160px !important;
			width: 240px !important;
		}

		/* Adjust grid layout for medium screens */
		.grid.grid-cols-2 {
			grid-template-columns: 1fr;
			gap: 1rem;
		}

		/* Make labels more responsive */
		.min-w-40 {
			min-width: 120px;
		}

		/* Adjust text sizes for better readability */
		.font-bold {
			font-size: 13px;
		}

		/* Adjust photo gallery for medium screens */
		.grid.grid-cols-2.gap-2 {
			grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
		}

		/* Make QR section more compact */
		.qr-section {
			padding: 8px;
		}

		.qr-section .flex.h-14.w-14 {
			height: 48px !important;
			width: 48px !important;
		}
	}

	/* Large screens (desktops and larger) */
	@media (min-width: 1025px) {
		.flyer-content {
			width: 240mm;
			max-width: 100%;
			padding: 20mm;
			font-size: 16px;
		}

		.header-section {
			font-size: 20px;
			padding: 18px;
		}

		.photo-frame {
			height: 160px !important;
			width: 280px !important;
		}

		/* Adjust label widths for better spacing */
		.min-w-40 {
			min-width: 140px;
		}

		/* Make grid more spacious on large screens */
		.grid.grid-cols-2 {
			gap: 2rem;
		}

		/* Increase photo gallery spacing */
		.grid.grid-cols-2.gap-2 {
			gap: 1rem;
		}

		/* Make QR section larger */
		.qr-section {
			padding: 20px;
		}

		.qr-section .flex.h-14.w-14 {
			height: 56px !important;
			width: 56px !important;
		}

		/* Adjust contact section spacing */
		.contact-section {
			padding: 20px;
		}

		/* Make reward section more prominent */
		.reward-section {
			padding: 16px 20px;
		}
	}

	@media (max-width: 768px) {
		.flyer-content {
			width: 100%;
			padding: 10mm;
		}

		.header-section {
			font-size: 16px;
			padding: 12px;
		}
	}
</style>
