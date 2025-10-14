<script lang="ts">
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
	import { BACKEND_URL, PET_MAX_IMAGES } from '$lib/config';
	import MultiImageGallery from '$lib/components/MultiImageGallery.svelte';
	import type { GalleryItem } from '$lib/components/MultiImageGallery.svelte';

	let loading = $state(true);
	// referenced to avoid unused var lint error
	void loading;
	let saving = $state(false);
	let error = $state('');
	let success = $state(false);

	let petId: string;

	// Form fields (same shape as add page)
	let name = $state('');
	let petType = $state<PetTypeEnum | ''>('');
	let notes = $state('');
	// Legacy single-image vars (no longer used but kept to avoid type breaks elsewhere if imported)
	let _image = $state<FileList | null>(null); // deprecated
	let _imagePreview = $state<string | null>(null); // deprecated
	// reference legacy variables to avoid unused-var lint errors
	void _image;
	void _imagePreview;

	// Unified gallery state (existing + newly added)
	let gallery = $state<GalleryItem[]>([]);

	let status = $state<PetStatusEnum | ''>('');
	const MAX_IMAGES = PET_MAX_IMAGES;

	// Pet type options
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
		gallery = items;
	}

	function handleGalleryError(message: string) {
		error = message;
	}

	$effect(() => {
		void (async () => {
			petId = $page.params.id || '';
			try {
				const data = await get<PetOut>(`api/pets/${petId}`, { requireAuth: true });
				// Map backend fields to form fields
				name = data.name || '';
				petType = (data.pet_type as PetTypeEnum) || '';
				notes = data.notes || '';
				status = (data.status as PetStatusEnum) || 'at_home';
				// Build gallery from existing pictures (relative URLs). Preserve order.
				const existing =
					data.pictures && data.pictures.length > 0
						? data.pictures
						: data.picture
							? [data.picture]
							: [];
				gallery = existing.map((p) => ({
					id: crypto.randomUUID(),
					preview: p.startsWith('http') ? p : `${BACKEND_URL}${p}`,
					value: p
				})); // cast to GalleryItem when used by parent
			} catch (err) {
				error = getMessage('network_error');
				console.error(err);
			} finally {
				loading = false;
			}
		})();
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

			// Prepare ordered pictures array (upload new ones, keep existing not removed)
			const visible = gallery.filter((g) => !g.removed).slice(0, MAX_IMAGES);
			const pictures: string[] = [];
			for (const item of visible) {
				if (item.file) {
					try {
						const fd = new FormData();
						fd.append('image', item.file);
						const imgData = await post<{ url: string }>('api/upload', fd, {
							requireAuth: true,
							contentType: 'form-data'
						});
						pictures.push(imgData.url);
					} catch (e) {
						console.warn('Individual image upload failed', e);
					}
				} else if (item.value) {
					pictures.push(item.value);
				}
			}
			// Fallback to legacy single image preview if nothing present
			if (pictures.length === 0 && _imagePreview) pictures.push(_imagePreview);
			const combined = pictures.slice(0, MAX_IMAGES);
			const body: PetUpdate = {
				owner_id: Number($session.user.id),
				name,
				pet_type: (petType || 'Other') as PetTypeEnum,
				notes,
				status: (status || 'at_home') as PetStatusEnum,
				picture: combined[0],
				pictures: combined
			};
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
			<PageHeader title={getMessage('edit_pet')} />
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
						bind:selected={petType as string}
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
					<label for="multi-image-input-edit" class="mb-1 block font-medium text-gray-700"
						>{getMessage('pet_image_label')} (max {MAX_IMAGES})</label
					>
					<MultiImageGallery
						inputId="multi-image-input-edit"
						initial={gallery.map((g) => ({
							url: g.preview,
							value: g.value ?? undefined,
							id: g.id
						}))}
						onChange={handleGalleryChange}
						onError={handleGalleryError}
					/>
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
