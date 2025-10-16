<script lang="ts">
	import { onMount } from 'svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import type { PetOut } from '$lib/types/api/pet';

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

	// Datos del flyer
	let flyerData = {
		pet_name: pet.name,
		pet_type: pet.pet_type,
		pet_age: '',
		pet_breed: '',
		pet_color: '',
		pet_gender: '',
		pet_last_seen: '',
		pet_location: '',
		pet_description: pet.notes || '',
		pet_picture: pet.picture,
		qr_code_url: `/api/qrcode/${pet.id}`,
		owner_name: `${owner.first_name} ${owner.last_name}`,
		owner_phone: owner.phone,
		owner_email: owner.email,
		owner_address: owner.full_address,
		reward_amount: owner.recovery_bounty ? `$${owner.recovery_bounty}` : '',
		show_reward: owner.recovery_bounty ? 'block' : 'none',
		pet_id: pet.id
	};

	function printFlyer() {
		if (flyerContainer) {
			const printWindow = window.open('', '_blank');
			if (printWindow) {
				printWindow.document.write(`
					<!DOCTYPE html>
					<html>
						<head>
							<title>Flyer - ${pet.name}</title>
							<style>
								@page { size: A4; margin: 0; }
								body { margin: 0; }
								${Array.from(document.styleSheets)
									.map((sheet) => {
										try {
											return Array.from(sheet.cssRules)
												.map((rule) => rule.cssText)
												.join('\n');
										} catch {
											return '';
										}
									})
									.join('\n')}
							</style>
						</head>
						<body>
							${flyerContainer.innerHTML}
						</body>
					</html>
				`);
				printWindow.document.close();
				printWindow.print();
			}
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

	onMount(() => {
		// Inicializar el estado de edición
		toggleEdit();
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

		<button class="btn btn-outline" on:click={toggleEdit}>
			{#if isEditing}
				🔒 {getMessage('finish_editing')}
			{:else}
				✏️ {getMessage('edit_flyer')}
			{/if}
		</button>
	</div>

	<div class="flyer-preview overflow-hidden rounded-lg border bg-white">
		<div bind:this={flyerContainer} class="flyer-content">
			<!-- Header -->
			<div class="header mb-4 text-center">
				<div
					class="lost-banner mb-4 rounded-lg bg-red-500 px-4 py-3 text-center text-2xl font-bold text-white"
					contenteditable="true"
				>
					¡MASCOTA PERDIDA!
				</div>
			</div>

			<!-- Información de la mascota -->
			<div class="pet-info mb-4 flex gap-4">
				<!-- Foto de la mascota -->
				<div
					class="pet-photo flex min-h-32 flex-1 items-center justify-center overflow-hidden rounded-lg border-2 border-gray-300 bg-gray-50"
				>
					{#if flyerData.pet_picture}
						<img
							src={flyerData.pet_picture}
							alt="Foto de {flyerData.pet_name}"
							class="max-h-full max-w-full object-cover"
						/>
					{:else}
						<div class="text-center text-lg text-gray-500" contenteditable="true">
							Foto de la mascota
						</div>
					{/if}
				</div>

				<!-- Detalles de la mascota -->
				<div class="pet-details flex flex-1 flex-col gap-2">
					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Nombre:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_name}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Tipo:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_type}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Edad:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_age}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Raza:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_breed}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Color:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_color}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Sexo:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_gender}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Última vez visto:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_last_seen}</span
						>
					</div>

					<div class="detail-row mb-1 flex">
						<span class="detail-label min-w-32 font-bold text-gray-700">Lugar:</span>
						<span
							class="detail-value flex-1 border-b border-dotted border-gray-300 pb-1"
							contenteditable="true">{flyerData.pet_location}</span
						>
					</div>

					<div class="mt-3">
						<strong>Descripción:</strong><br />
						<div contenteditable="true" class="mt-1 min-h-16 rounded border border-gray-300 p-2">
							{flyerData.pet_description}
						</div>
					</div>
				</div>
			</div>

			<!-- Código QR -->
			<div class="qr-section my-4 flex items-center justify-center gap-4">
				<div
					class="qr-code flex h-16 w-16 items-center justify-center border-2 border-gray-800 bg-gray-50"
				>
					<img src={flyerData.qr_code_url} alt="QR Code" class="max-h-full max-w-full" />
				</div>
				<div class="qr-text flex-1 text-center">
					<strong>¡Escanea para más info!</strong><br />
					<small>www.petto.com/qr/{flyerData.pet_id}</small>
				</div>
			</div>

			<!-- Información de contacto -->
			<div class="contact-info my-3 rounded-lg bg-blue-50 p-3">
				<div class="contact-title mb-2 text-lg font-bold text-blue-800">
					¡Si encuentras a mi mascota, por favor contacta!
				</div>
				<div class="mt-2 flex gap-4">
					<div class="flex-1">
						<strong>Dueño:</strong> <span contenteditable="true">{flyerData.owner_name}</span><br />
						<strong>Teléfono:</strong>
						<span contenteditable="true">{flyerData.owner_phone}</span><br />
						<strong>Email:</strong> <span contenteditable="true">{flyerData.owner_email}</span>
					</div>
					<div class="flex-1">
						<strong>Dirección:</strong><br />
						<span contenteditable="true">{flyerData.owner_address}</span>
					</div>
				</div>
			</div>

			<!-- Sección de recompensa (opcional) -->
			{#if flyerData.show_reward === 'block'}
				<div class="reward-section my-3 rounded-lg border-l-4 border-yellow-400 bg-yellow-50 p-3">
					<div class="reward-title mb-1 font-bold text-yellow-800">¡RECOMPENSA!</div>
					<div contenteditable="true">{flyerData.reward_amount}</div>
				</div>
			{/if}

			<!-- Footer -->
			<div class="footer mt-auto text-center text-sm text-gray-500">
				<div contenteditable="true">Creado con ❤️ por Petto - Reunamos mascotas perdidas</div>
			</div>
		</div>

		<!-- Tabs para cortar (solo en vista previa) -->
		<div class="cut-tabs relative mt-4 h-6 border-t border-dashed border-gray-300 bg-white">
			<div
				class="tab absolute bottom-0 left-4 flex h-5 w-10 -rotate-90 transform items-center justify-center rounded-t bg-red-500 text-xs font-bold text-white"
				contenteditable="true"
			>
				{flyerData.owner_phone}
			</div>
			<div
				class="tab absolute right-4 bottom-0 flex h-5 w-10 -rotate-90 transform items-center justify-center rounded-t bg-red-500 text-xs font-bold text-white"
				contenteditable="true"
			>
				{flyerData.owner_phone}
			</div>
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
		font-family: Arial, sans-serif;
		font-size: 14px;
		line-height: 1.4;
		position: relative;
	}

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
		}
		[contenteditable] {
			outline: none !important;
			background: transparent !important;
		}
	}
</style>
