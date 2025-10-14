<script module lang="ts">
	export interface InitialImage {
		id?: string;
		url: string;
		value?: string;
	}
	export interface GalleryItem {
		id: string;
		preview: string;
		value: string | null;
		file?: File;
		removed?: boolean;
	}
	export interface Props {
		initial?: InitialImage[];
		maxImages?: number;
		disabled?: boolean;
		inputId?: string;
		onChange?: (items: GalleryItem[]) => void;
		onError?: (message: string) => void;
	}
</script>

<script lang="ts">
	import { PET_MAX_IMAGES, PET_MAX_IMAGE_BYTES, PET_ALLOWED_IMAGE_MIME } from '$lib/config';

	// Props via Svelte 5 runes
	const _props = $props<{
		initial?: InitialImage[];
		maxImages?: number;
		disabled?: boolean;
		inputId?: string;
		onChange?: (items: GalleryItem[]) => void;
		onError?: (message: string) => void;
	}>();

	let {
		initial = [],
		maxImages = PET_MAX_IMAGES,
		disabled = false,
		inputId,
		onChange,
		onError
	} = _props;

	// Mutable gallery state
	let gallery = $state<GalleryItem[]>([]);

	function initGallery() {
		gallery = initial.map((img: InitialImage) => ({
			id: img.id || crypto.randomUUID(),
			preview: img.url,
			value: img.value ?? img.url // assume provided url is the value if value missing
		}));
	}

	// Initialize once
	initGallery();

	// Re-run init when initial changes AFTER async load (only if gallery still empty to avoid clobbering user edits)
	$effect(() => {
		if (initial && initial.length > 0 && gallery.length === 0) {
			initGallery();
		}
	});

	// Notify parent via callback when gallery changes
	$effect(() => {
		if (typeof onChange === 'function') onChange(gallery);
	});

	function emitError(message: string) {
		if (typeof onError === 'function') onError(message);
		else console.warn(message);
	}

	function handleFilesSelect(event: Event) {
		if (disabled) return;
		const input = event.target as HTMLInputElement;
		if (!input.files) return;
		const selected = Array.from(input.files);
		if (selected.length + gallery.filter((g) => !g.removed).length > maxImages) {
			return emitError(`Maximum ${maxImages} images allowed`);
		}
		for (const f of selected) {
			if (!PET_ALLOWED_IMAGE_MIME.includes(f.type)) {
				return emitError('Invalid file type');
			}
			if (f.size > PET_MAX_IMAGE_BYTES) {
				return emitError('File too large (>5MB)');
			}
			const reader = new FileReader();
			reader.onload = (e) => {
				gallery = [
					...gallery,
					{
						id: crypto.randomUUID(),
						preview: e.target?.result as string,
						value: null,
						file: f
					}
				].slice(0, maxImages);
			};
			reader.readAsDataURL(f);
		}
	}

	function removeImage(index: number) {
		const visible = gallery.filter((g) => !g.removed);
		const target = visible[index];
		if (!target) return;
		gallery = gallery.map((g) => (g === target ? { ...g, removed: true } : g));
	}

	function move(from: number, to: number) {
		const visible = gallery.filter((g) => !g.removed);
		if (to < 0 || to >= visible.length) return;
		const reordered = [...visible];
		const [item] = reordered.splice(from, 1);
		reordered.splice(to, 0, item);
		const removed = gallery.filter((g) => g.removed);
		gallery = [...reordered, ...removed];
	}
</script>

<div class="space-y-2">
	<input
		id={inputId}
		type="file"
		multiple
		accept="image/*"
		onchange={handleFilesSelect}
		class="w-full text-sm text-gray-500 file:mr-4 file:rounded file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
		{disabled}
	/>

	{#if gallery.filter((g) => !g.removed).length > 0}
		<div class="mt-3 grid grid-cols-3 gap-3 md:grid-cols-5">
			{#each gallery.filter((g) => !g.removed) as g, i (g.id)}
				<div class="group relative">
					<img
						src={g.preview}
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
								onclick={() => move(i, i - 1)}>⇡</button
							>
						{/if}
						{#if i < gallery.filter((g) => !g.removed).length - 1}
							<button
								type="button"
								class="rounded bg-black/50 px-1 text-xs text-white"
								title="⇣"
								onclick={() => move(i, i + 1)}>⇣</button
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

<style>
	/* No additional styles for now */
</style>
