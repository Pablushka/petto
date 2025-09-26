<script lang="ts">
	import { m } from '$lib/paraglide/messages';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import TextField from '$lib/components/TextField.svelte';
	import Select from '$lib/components/SelectLang.svelte';
	import Alert from '$lib/components/Alert.svelte';
	import { session } from '$lib/stores/session';
	import { getMessage } from '$lib/utils/message-helper';
	import { goto } from '$app/navigation';
	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
	import { post } from '$lib/utils/api';
	import type { PetType as PetTypeEnum, PetCreate } from '$lib/types/api/pet';

	// Form state
	let name = '';
	let petType: PetTypeEnum | '' = '';
	let notes = '';
	let image: FileList | null = null;

	let loading = false;
	let error = '';
	let success = false;

	// Pet type options based on the PetType enum in models.py
	const petTypeOptions: { id: PetTypeEnum; option_text: string }[] = [
		{ id: 'Cat', option_text: 'Cat' },
		{ id: 'Dog', option_text: 'Dog' },
		{ id: 'Lizard', option_text: 'Lizard' },
		{ id: 'Hamster', option_text: 'Hamster' },
		{ id: 'Bird', option_text: 'Bird' },
		{ id: 'Other', option_text: 'Other' }
	];

	// Handle file input change
	let imagePreview: string | null = null;
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

	// Handle form submission
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

			// Create FormData object to handle file upload
			const formData = new FormData();
			formData.append('name', name);
			formData.append('pet_type', petType);
			formData.append('notes', notes);
			formData.append('owner_id', $session.user.id.toString());

			let imageUrl = '';
			if (image && image[0]) {
				// For simplicity, we'll assume there's an image upload endpoint
				// that returns the URL of the uploaded image
				const imageFormData = new FormData();
				imageFormData.append('image', image[0]);

				// Use API helper to upload image (auto refresh on 401)
				const imageData = await post<{ url: string }>('api/upload', imageFormData, {
					requireAuth: true,
					contentType: 'form-data'
				});
				imageUrl = imageData.url;
			}

			formData.append('picture', imageUrl);

			// Create pet via API helper (auto refresh on 401)
			const body: PetCreate = {
				name,
				pet_type: (petType || 'Other') as PetTypeEnum,
				notes,
				picture: imageUrl || 'default_pet.jpg',
				owner_id: Number($session.user.id),
				status: 'at_home' // Default status for new pets
			};
			await post('api/pets', body, { requireAuth: true, contentType: 'json' });

			// Success!
			success = true;
			setTimeout(() => {
				goto('/pets'); // Redirect to pets list after success
			}, 2000);
		} catch (err) {
			error = getMessage('network_error');
			console.error(err);
		}

		loading = false;
	}
</script>

<ProtectedRoute>
	<div class="space-y-6">
		<div class="flex items-center justify-between">
			<PageHeader title={getMessage('add_new_pet')} />

			<div>
				<a href="/pets" class="inline-block">
					<Button type="secondary">
						&larr; {getMessage('back_to_list')}
					</Button>
				</a>
			</div>
		</div>

		<div class="rounded-lg bg-white p-6 shadow-md">
			{#if success}
				<Alert type="success" message={getMessage('pet_added_success')} dismissible />
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
				<!-- Pet Information -->
				<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
					<TextField label={getMessage('pet_name_label')} name="name" bind:value={name} required />

					<Select
						label="Pet Type"
						name="petType"
						bind:selected={petType as any}
						items={petTypeOptions}
						required
					/>
				</div>

				<!-- Description -->
				<div>
					<label for="notes" class="mb-1 block font-medium text-gray-700">
						{getMessage('pet_description')}
					</label>
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
					<label for="pet-image" class="mb-1 block font-medium text-gray-700">
						{getMessage('pet_image_label')}
					</label>

					<input
						id="pet-image"
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
						{getMessage('add_new_pet')}
					</Button>
				</div>
			</form>
		</div>
	</div>
</ProtectedRoute>
