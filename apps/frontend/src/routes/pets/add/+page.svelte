<script lang="ts">
	// 'm' not used here; import removed
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import TextField from '$lib/components/TextField.svelte';
	import Select from '$lib/components/SelectLang.svelte';
	import Alert from '$lib/components/Alert.svelte';
	import { session } from '$lib/stores/session';
	import { getMessage } from '$lib/utils/message-helper';
	import { goto } from '$app/navigation';
	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
	import { post, uploadImage } from '$lib/utils/api';
	import type { PetType as PetTypeEnum, PetCreate } from '$lib/types/api/pet';
	import { PET_MAX_IMAGES } from '$lib/config';
	import MultiImageGallery from '$lib/components/MultiImageGallery.svelte';
	import type { GalleryItem } from '$lib/components/MultiImageGallery.svelte';

	// Form state
	let name = '';
	let petType: PetTypeEnum | '' = '';
	let notes = '';
	// Legacy single image vars retained (not used in multi version)
	let _image: FileList | null = null;
	let _imagePreview: string | null = null;

	// Multi-image state via reusable component
	let galleryItems: GalleryItem[] = [];
	const MAX_IMAGES = PET_MAX_IMAGES;

	let loading = false;
	let error = '';
	let success = false;
	// reference legacy vars to avoid lint complaints (no runtime effect)
	void _image;
	void _imagePreview;

	// Pet type options based on the PetType enum in models.py
	const petTypeOptions: { id: PetTypeEnum; option_text: string }[] = [
		{ id: 'Cat', option_text: 'Cat' },
		{ id: 'Dog', option_text: 'Dog' },
		{ id: 'Lizard', option_text: 'Lizard' },
		{ id: 'Hamster', option_text: 'Hamster' },
		{ id: 'Bird', option_text: 'Bird' },
		{ id: 'Other', option_text: 'Other' }
	];

	// MultiImageGallery now calls provided callbacks directly (items / message)
	function handleGalleryChange(items: GalleryItem[]) {
		galleryItems = items;
	}
	function handleGalleryError(message: string) {
		error = message;
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

			// Upload any new files in order; assemble pictures[] preserving order
			const visible = galleryItems.filter((g) => !g.removed);
			const pictures: string[] = [];
			for (const item of visible) {
				if (item.file) {
					try {
						const { url } = await uploadImage(item.file);
						pictures.push(url);
					} catch (e) {
						console.error('Image upload failed', e);
						error = 'Upload failed';
						loading = false;
						return;
					}
				} else if (item.value) {
					pictures.push(item.value);
				}
			}
			if (pictures.length === 0 && _imagePreview) pictures.push(_imagePreview);

			const body: PetCreate = {
				name,
				pet_type: (petType || 'Other') as PetTypeEnum,
				notes,
				picture: pictures[0] || 'default_pet.jpg',
				pictures,
				status: 'at_home'
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
						bind:selected={petType}
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

				<!-- Images Upload (multi) -->
				<div>
					<label for="multi-image-input" class="mb-1 block font-medium text-gray-700"
						>{getMessage('pet_image_label')} (max {MAX_IMAGES})</label
					>
					<MultiImageGallery
						inputId="multi-image-input"
						initial={[]}
						onChange={handleGalleryChange}
						onError={handleGalleryError}
					/>
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
