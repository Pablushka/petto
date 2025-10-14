<script lang="ts">
	// 'm' not used here; import removed

	const props = $props<{
		message?: string;
		type?: 'error' | 'success' | 'info' | 'warning';
		dismissible?: boolean;
		children?: (props?: unknown) => unknown;
	}>();
	let { message = '', type = 'info', dismissible = false, children } = props;

	let visible = $state(true);

	// Alert style classes based on type
	const typeClasses: Record<'error' | 'success' | 'info' | 'warning', string> = {
		error: 'bg-red-100 text-red-800 border-red-200',
		success: 'bg-green-100 text-green-800 border-green-200',
		info: 'bg-blue-100 text-blue-800 border-blue-200',
		warning: 'bg-yellow-100 text-yellow-800 border-yellow-200'
	};

	// Icon for each alert type
	const typeIcons: Record<'error' | 'success' | 'info' | 'warning', string> = {
		error: '⚠️',
		success: '✅',
		info: 'ℹ️',
		warning: '⚠️'
	};

	function dismiss() {
		visible = false;
	}
</script>

{#if visible}
	<div
		class={`mb-4 flex items-start rounded border p-4 ${typeClasses[type as 'error' | 'success' | 'info' | 'warning']}`}
	>
		<span class="mr-2">{typeIcons[type as 'error' | 'success' | 'info' | 'warning']}</span>
		<div class="flex-1">
			{#if children}
				{@render children?.()}
			{:else}
				{message}
			{/if}
		</div>
		{#if dismissible}
			<button
				onclick={dismiss}
				class="ml-4 text-gray-500 hover:text-gray-700"
				aria-label="Dismiss alert"
			>
				✕
			</button>
		{/if}
	</div>
{/if}
