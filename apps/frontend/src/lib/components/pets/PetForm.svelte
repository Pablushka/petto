<script lang="ts">
	import TextField from '../TextField.svelte';
	import Select from '../SelectLang.svelte';
	import Button from '../Button.svelte';
	import Alert from '../Alert.svelte';
	import { session } from '$lib/stores/session';
	import { getMessage } from '$lib/utils/message-helper';
	import { post, uploadImage } from '$lib/utils/api';
	import type { PetType as PetTypeEnum, PetCreate } from '$lib/types/api/pet';
	import { DEFAULT_PET_IMAGE } from '$lib/utils/pet';
	import {
		PET_MAX_IMAGES,
		PET_MAX_IMAGE_BYTES,
		PET_ALLOWED_IMAGE_MIME,
		BACKEND_URL
	} from '$lib/config';

	// Optional fetch function passed from a load function (SvelteKit)
	const { fetchFn } = $props<{ fetchFn?: typeof fetch }>();

	// Form state (match backend Pet model)
	let name = $state('');
	let petType: PetTypeEnum | '' = $state(''); // maps to backend pet_type
	let notes = $state('');
	// Multiple images (up to 5)
	let images: File[] = $state([]);
	let previews: string[] = $state([]);
	const MAX_IMAGES = PET_MAX_IMAGES;
	const MAX_IMAGE_BYTES = PET_MAX_IMAGE_BYTES;
	const ALLOWED_MIME = PET_ALLOWED_IMAGE_MIME;

	let loading = $state(false);
	let error = $state('');
	let success = $state(false);

	// PetType options must match backend enum values
	const petTypeOptions: { id: PetTypeEnum; option_text: string }[] = [
		{ id: 'Cat', option_text: 'Cat' },
		{ id: 'Dog', option_text: 'Dog' },
		{ id: 'Lizard', option_text: 'Lizard' },
		{ id: 'Hamster', option_text: 'Hamster' },
		{ id: 'Bird', option_text: 'Bird' },
		{ id: 'Other', option_text: 'Other' }
	];

	// Handle file input change
	function handleImagesChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files) return;
		const selected = Array.from(input.files);
		if (selected.length + images.length > MAX_IMAGES) {
			error = `Maximum ${MAX_IMAGES} images allowed`;
			return;
		}
		for (const file of selected) {
			if (!ALLOWED_MIME.includes(file.type)) {
				error = 'Invalid file type';
				return;
			}
			if (file.size > MAX_IMAGE_BYTES) {
				error = 'File too large (>5MB)';
				return;
			}
		}
		images = [...images, ...selected].slice(0, MAX_IMAGES);
		generatePreviews();
	}

	function generatePreviews() {
		previews = [];
		images.forEach((f, idx) => {
			const reader = new FileReader();
			reader.onload = (e) => {
				previews[idx] = e.target?.result as string;
				// Force assignment to trigger update
				previews = [...previews];
			};
			reader.readAsDataURL(f);
		});
	}

	function removeImage(index: number) {
		images = images.filter((_, i) => i !== index);
		generatePreviews();
	}

	function moveImage(from: number, to: number) {
		if (to < 0 || to >= images.length) return;
		const arr = [...images];
		const [item] = arr.splice(from, 1);
		arr.splice(to, 0, item);
		images = arr;
		generatePreviews();
	}

	// Handle form submission (JSON body via API helper)
	async function handleSubmit() {
		loading = true;
		error = '';

		try {
			// Check if user is logged in
			if (!$session?.user) {
				error = getMessage('login_required');
				loading = false;
				return;
			}

			// Upload images sequentially (could be parallel, but sequential simplifies ordering)
			let uploaded: string[] = [];
			for (const file of images) {
				try {
					const { url } = await uploadImage(file);
					uploaded.push(url);
				} catch (err) {
					// Log and continue on per-file upload errors so overall submission can continue
					console.error('image upload failed', err);
				}
			}
			if (uploaded.length === 0) {
				uploaded = [DEFAULT_PET_IMAGE];
			}

			// Build JSON body expected by backend (see backend/models.py & routers/pets.py)
			const body: PetCreate = {
				owner_id: Number($session.user.id),
				name,
				pet_type: (petType || 'Other') as PetTypeEnum,
				picture: uploaded[0],
				pictures: uploaded,
				notes,
				status: 'at_home'
			};

			// Submit JSON via API helper. If fetchFn was provided, use it.
			await post('api/pets', body, {
				requireAuth: true,
				contentType: 'json',
				fetchFn
			});

			// Success!
			success = true;
			resetForm();
		} catch (err) {
			// Network or API error
			console.error('submit pet failed', err);
			error = getMessage('network_error');
		} finally {
			loading = false;
		}
	}

	// Reset form fields
	function resetForm() {
		name = '';
		petType = '';
		notes = '';
		images = [];
		previews = [];
	}
</script>

<div class="rounded-lg bg-white p-6 shadow-md">
	<h2 class="mb-6 text-2xl font-bold">{getMessage('edit_pet')}</h2>

	{#if success}
		<Alert type="success" message={getMessage('pet_report_success')} dismissible />
	{/if}

	{#if error}
		<Alert type="error" message={error} dismissible />
	{/if}

	<form
		onsubmit={(e) => {
			e.preventDefault();
			handleSubmit();
		}}
		class="space-y-6"
	>
		<!-- Pet Information (only model fields) -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<TextField label={getMessage('pet_name_label')} name="name" bind:value={name} required />

			<Select
				label={getMessage('pet_species')}
				name="pet_type"
				bind:selected={petType}
				items={petTypeOptions}
				required
			/>
		</div>

		<!-- Description -->
		<div>
			<label for="notes" class="mb-1 block font-medium text-gray-700"
				>{getMessage('pet_description')}</label
			>
			<textarea
				id="notes"
				name="notes"
				bind:value={notes}
				rows="4"
				class="w-full rounded border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
			></textarea>
		</div>

		<!-- Images Upload (multiple) -->
		<div>
			<label for="pet-images-input" class="mb-1 block font-medium text-gray-700">
				{getMessage('pet_image_label')} (max {MAX_IMAGES})
			</label>
			<input
				id="pet-images-input"
				type="file"
				accept="image/*"
				multiple
				onchange={handleImagesChange}
				class="w-full text-sm text-gray-500 file:mr-4 file:rounded file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-blue-700 hover:file:bg-blue-100"
			/>
			{#if previews.length > 0}
				<div class="mt-3 grid grid-cols-3 gap-3 md:grid-cols-5">
					{#each previews as p, i (p)}
						<div class="group relative">
							<img
								src={`${BACKEND_URL}${p}`}
								alt={`Preview ${i + 1}`}
								class="h-24 w-full rounded object-cover ring-2 {i === 0
									? 'ring-blue-500'
									: 'ring-transparent'}"
							/>
							<div
								class="absolute inset-0 flex items-start justify-end gap-1 p-1 opacity-0 group-hover:opacity-100"
							>
								<button
									type="button"
									class="rounded bg-black/50 px-1 text-xs text-white"
									title="Remove"
									onclick={() => removeImage(i)}>✕</button
								>
								{#if i > 0}
									<button
										type="button"
										class="rounded bg-black/50 px-1 text-xs text-white"
										title="⇡"
										onclick={() => moveImage(i, i - 1)}>⇡</button
									>
								{/if}
								{#if i < previews.length - 1}
									<button
										type="button"
										class="rounded bg-black/50 px-1 text-xs text-white"
										title="⇣"
										onclick={() => moveImage(i, i + 1)}>⇣</button
									>
								{/if}
							</div>
							{#if i === 0}
								<span
									class="absolute bottom-1 left-1 rounded bg-blue-600/80 px-1 text-[10px] font-semibold tracking-wide text-white uppercase"
									>Cover</span
								>
							{/if}
						</div>
					{/each}
				</div>
			{/if}
		</div>

		<!-- Submit Button -->
		<div class="flex justify-end">
			<Button type="primary" {loading}>
				{getMessage('button_submit')}
			</Button>
		</div>
	</form>
</div>
