<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import TextField from '$lib/components/TextField.svelte';
	import Select from '$lib/components/SelectLang.svelte';
	import Alert from '$lib/components/Alert.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import { goto } from '$app/navigation';
	import { get, post, put } from '$lib/utils/api';
	import type {
		PetType as PetTypeEnum,
		PetStatus as PetStatusEnum,
		PetOut,
		PetUpdate
	} from '$lib/types/api/pet';
	import { session } from '$lib/stores/session';

	let loading = true;
	let saving = false;
	let error = '';
	let success = false;

	let petId: string;

	// Form fields (same shape as add page)
	let name = '';
	let petType: PetTypeEnum | '' = '';
	let notes = '';
	let image: FileList | null = null;
	let imagePreview: string | null = null;

	// Pet type options
	const petTypeOptions: { id: PetTypeEnum; option_text: string }[] = [
		{ id: 'Cat', option_text: 'Cat' },
		{ id: 'Dog', option_text: 'Dog' },
		{ id: 'Lizard', option_text: 'Lizard' },
		{ id: 'Hamster', option_text: 'Hamster' },
		{ id: 'Bird', option_text: 'Bird' },
		{ id: 'Other', option_text: 'Other' }
	];

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

	onMount(async () => {
		petId = $page.params.id || '';
		try {
			const data = await get<PetOut>(`api/pets/${petId}`, { requireAuth: false });
			// Map backend fields to form fields
			name = data.name || '';
			petType = (data.pet_type as PetTypeEnum) || '';
			notes = data.notes || '';
			if (data.picture) {
				imagePreview = data.picture;
			}
		} catch (err) {
			error = getMessage('network_error');
			console.error(err);
		} finally {
			loading = false;
		}
	});

	async function handleSubmit() {
		saving = true;
		error = '';
		try {
			// Ensure user is logged in
			if (!$session?.user) {
				error = getMessage('login_required');
				saving = false;
				return;
			}

			// Prepare body
			const body: PetUpdate = {
				owner_id: Number($session.user.id),
				name,
				pet_type: (petType || 'Other') as PetTypeEnum,
				notes,
				status: (status || 'at_home') as PetStatusEnum
			};

			// Handle image upload if present (optional)
			if (image && image[0]) {
				const imageForm = new FormData();
				imageForm.append('image', image[0]);
				const imgData = await post<{ url: string }>('api/upload', imageForm, {
					requireAuth: true,
					contentType: 'form-data'
				});
				body.picture = imgData.url;
			}

			await put(`api/pets/${petId}`, body, { requireAuth: true, contentType: 'json' });

			success = true;
			setTimeout(() => goto(`/pets/${petId}`), 1200);
		} catch (err) {
			console.error(err);
			error = getMessage('network_error');
		} finally {
			saving = false;
		}
	}
</script>

<ProtectedRoute>
	<div class="space-y-6">
		<div class="flex items-center justify-between">
			<PageHeader title={getMessage('add_new_pet')} />
			<div>
				<a href="/pets" class="inline-block"
					><Button type="secondary">&larr; {getMessage('back_to_list')}</Button></a
				>
			</div>
		</div>

		<div class="rounded-lg bg-white p-6 shadow-md">
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

				<div>
					<label for="notes" class="mb-1 block font-medium text-gray-700"
						>{getMessage('pet_description')}</label
					>
					<textarea
						id="notes"
						name="notes"
						bind:value={notes}
						rows="4"
						class="w-full rounded border border-gray-300 px-3 py-2"
					></textarea>
				</div>

				<div>
					<label for="pet-image" class="mb-1 block font-medium text-gray-700"
						>{getMessage('pet_image_label')}</label
					>
					<input
						id="pet-image"
						type="file"
						accept="image/*"
						bind:files={image}
						onchange={handleImageChange}
						class="w-full text-sm text-gray-500 file:mr-4 file:rounded file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-blue-700 hover:file:bg-blue-100"
					/>

					{#if imagePreview}
						<div class="mt-2">
							<img src={imagePreview} alt="Preview" class="h-32 rounded object-cover" />
						</div>
					{/if}
				</div>

				<div class="flex justify-end">
					<button class="rounded bg-blue-600 px-4 py-2 text-white" disabled={saving} type="submit"
						>{saving ? getMessage('loading') : getMessage('button_submit')}</button
					>
				</div>
			</form>
		</div>
	</div>
</ProtectedRoute>
