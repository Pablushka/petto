<script lang="ts">
	import { m } from '$lib/paraglide/messages';

	// Define props via $props and support event prop forwarding for click
	type ButtonType = 'primary' | 'secondary' | 'danger' | 'success' | 'warning';
	type ButtonSize = 'sm' | 'md' | 'lg';

	const props = $props<{
		type?: ButtonType;
		size?: ButtonSize;
		fullWidth?: boolean;
		disabled?: boolean;
		loading?: boolean;
		onclick?: (e: MouseEvent) => void;
		children?: any;
	}>();
	let type: ButtonType = props.type ?? 'primary';
	let size: ButtonSize = props.size ?? 'md';
	let fullWidth = props.fullWidth ?? false;
	let disabled = props.disabled ?? false;
	let loading = props.loading ?? false;
	let onclick = props.onclick;
	let children = props.children;

	// Button style classes based on type
	const typeClasses: Record<ButtonType, string> = {
		primary: 'bg-blue-600 hover:bg-blue-700 text-white',
		secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
		danger: 'bg-red-600 hover:bg-red-700 text-white',
		success: 'bg-green-600 hover:bg-green-700 text-white',
		warning: 'bg-yellow-500 hover:bg-yellow-600 text-white'
	} as const;

	// Button size classes
	const sizeClasses: Record<ButtonSize, string> = {
		sm: 'px-3 py-1 text-sm',
		md: 'px-4 py-2',
		lg: 'px-6 py-3 text-lg'
	} as const;

	// Compute classes reactively
	const buttonClasses = $derived(
		`rounded font-medium transition-colors ${typeClasses[type]} ${sizeClasses[size]} ${fullWidth ? 'w-full' : ''} ${
			disabled || loading ? 'opacity-70 cursor-not-allowed' : ''
		}`.trim()
	);
</script>

<button class={buttonClasses} disabled={disabled || loading} {onclick}>
	{#if loading}
		<span class="mr-2 inline-block animate-spin">↻</span>
	{/if}
	{@render children?.()}
</button>
