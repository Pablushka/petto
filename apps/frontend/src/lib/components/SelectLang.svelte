<script lang="ts">
	import { setLocale } from '$lib/paraglide/runtime';

	// Supported locales for runtime detection (used only when selecting language)
	const LOCALES = ['en', 'es', 'jp'] as const;
	type Locale = (typeof LOCALES)[number];

	// Items must have id (value) and option_text (label)
	export type Item = { id: string; option_text: string };
	interface Props {
		items: Item[];
		selected: string;
		label?: string;
		name?: string;
		error?: string;
		required?: boolean;
		disabled?: boolean;
		placeholder?: string;
		onChange?(value: string): void;
	}

	let {
		items,
		selected = $bindable(),
		label = '',
		name = '',
		error = '',
		required = false,
		disabled = false,
		placeholder = '',
		onChange
	}: Props = $props();

	// Input id derived from name for linking label
	const id = `select-${name}`;

	// Create events for Svelte 5
	function localeChange(value: string) {
		// In Svelte 5, this function declaration automatically creates an event
		// with the same name that can be listened to with on:localeChange

		// Also call the prop callback if provided
		if (onChange) {
			onChange(value);
		}
	}

	function handleChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		const newValue = target.value as string;

		// If this select is effectively a locale selector, update the app locale
		if (LOCALES.includes(newValue as Locale)) {
			setLocale(newValue as Locale);
		}

		// Dispatch the event with Svelte 5 style
		localeChange(newValue);
	}
</script>

<div class="mb-4">
	{#if label}
		<label for={id} class="mb-1 block font-medium text-gray-700">
			{label}
			{#if required}<span class="text-red-500">*</span>{/if}
		</label>
	{/if}

	<select
		{id}
		{name}
		bind:value={selected}
		{required}
		{disabled}
		onchange={handleChange}
		class="appearance-none rounded border border-gray-300 bg-none px-2 py-1 focus:border-blue-500
      focus:ring-1 focus:ring-blue-500
      {error ? 'border-red-500 bg-red-50' : ''}"
	>
		{#if placeholder}
			<option value="" disabled selected>{placeholder}</option>
		{/if}

		{#each items as item}
			<option value={item.id}>{item.option_text}</option>
		{/each}
	</select>

	{#if error}
		<p class="mt-1 text-sm text-red-600">{error}</p>
	{/if}
</div>
