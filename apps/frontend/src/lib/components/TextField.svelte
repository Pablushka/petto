<script lang="ts">
	// 'm' not used here; import removed

	let {
		label,
		name,
		type = 'text',
		value = $bindable(''),
		placeholder = '',
		required = false,
		disabled = false,
		error = ''
	} = $props<{
		label: string;
		name: string;
		type?: string;
		value?: string;
		placeholder?: string;
		required?: boolean;
		disabled?: boolean;
		error?: string;
	}>();

	// Input id derived from name for linking label
	const id = `input-${name}`;
</script>

<div class="mb-4">
	<label for={id} class="mb-1 block font-medium text-gray-700">
		{label}
		{#if required}<span class="text-red-500">*</span>{/if}
	</label>

	<input
		{id}
		{name}
		{type}
		bind:value
		{placeholder}
		{required}
		{disabled}
		class="w-full rounded border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500
      {error ? 'border-red-500 bg-red-50' : ''}"
	/>

	{#if error}
		<p class="mt-1 text-sm text-red-600">{error}</p>
	{/if}
</div>
