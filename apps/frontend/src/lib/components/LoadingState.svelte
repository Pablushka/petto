<script lang="ts">
	import { m } from '$lib/paraglide/messages';

	const loadingProps = $props<{
		loading?: boolean;
		noResultsMessage?: string;
		showNoResults?: boolean;
		children?: (props?: any) => any;
	}>();
	let {
		loading = false,
		noResultsMessage = 'No results found',
		showNoResults = true,
		children
	} = loadingProps;
</script>

{#if loading}
	<div class="flex items-center justify-center py-12">
		<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-500"></div>
	</div>
{:else if children}
	{@render children?.()}
{:else if showNoResults}
	<div class="py-12 text-center text-gray-500">
		<p>{noResultsMessage}</p>
	</div>
{/if}
