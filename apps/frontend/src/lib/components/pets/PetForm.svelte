<script lang="ts">
	import TextField from '../TextField.svelte';
	import Select from '../SelectLang.svelte';
	import Button from '../Button.svelte';
	import Alert from '../Alert.svelte';
	import { session } from '$lib/stores/session';
	import { getMessage } from '$lib/utils/message-helper';
	import { post } from '$lib/utils/api';
	import type { PetType as PetTypeEnum, PetCreate } from '$lib/types/api/pet';

	// Optional fetch function passed from a load function (SvelteKit)
	const { fetchFn } = $props<{ fetchFn?: typeof fetch }>();

	// Form state (match backend Pet model)
	let name = $state('');
	let petType: PetTypeEnum | '' = $state(''); // maps to backend pet_type
	let notes = $state('');
	let image: FileList | null = $state(null);

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
	let imagePreview: string | null = $state(null);
	function handleImageChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			const file = input.files[0];
			const reader = new FileReader();
			reader.onload = (e) => {
				imagePreview = e.target?.result as string;
			};
			reader.readAsDataURL(file);
		} else {
			imagePreview = null;
		}
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

			// Determine picture URL (optional upload)
			let pictureUrl = 'default_pet.jpg';
			if (image && image[0]) {
				const imageFormData = new FormData();
				imageFormData.append('image', image[0]);
				try {
					const img = await post<{ url: string }>('api/upload', imageFormData, {
						requireAuth: true,
						contentType: 'form-data',
						fetchFn
					});
					pictureUrl = img.url || pictureUrl;
				} catch (e) {
					// Ignore upload error; fallback to default
				}
			}

			// Build JSON body expected by backend (see backend/models.py & routers/pets.py)
			const body: PetCreate = {
				owner_id: Number($session.user.id),
				name,
				pet_type: (petType || 'Other') as PetTypeEnum,
				picture: pictureUrl,
				notes,
				status: 'at_home' // New pets default to 'at_home'
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
		image = null;
		imagePreview = null;
	}
</script>

<div class="rounded-lg bg-white p-6 shadow-md">
	<h2 class="mb-6 text-2xl font-bold">{getMessage('add_new_pet')}</h2>

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
				bind:selected={petType as any}
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

		<!-- Image Upload -->
		<div>
			<label for="pet-image-input" class="mb-1 block font-medium text-gray-700">
				{getMessage('pet_image_label')}
			</label>

			<input
				id="pet-image-input"
				type="file"
				accept="image/*"
				bind:files={image}
				onchange={handleImageChange}
				class="w-full text-sm text-gray-500
          file:mr-4 file:rounded file:border-0
          file:bg-blue-50 file:px-4
          file:py-2 file:text-sm
          file:font-semibold file:text-blue-700
          hover:file:bg-blue-100"
			/>

			{#if imagePreview}
				<div class="mt-2">
					<img src={imagePreview} alt="Preview" class="h-32 rounded object-cover" />
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
