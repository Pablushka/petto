<script lang="ts">
	// Simpler, fully reactive props (Svelte 5 still supports export let for standard props)
	export let loading: boolean = false;
	export let noResultsMessage: string = 'No results found';
	export let showNoResults: boolean = true;
</script>

{#if loading}
	<div class="flex items-center justify-center py-12">
		<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-500"></div>
	</div>
{:else}
	<slot />
	{#if showNoResults && !loading && !$$slots.default}
		<div class="py-12 text-center text-gray-500">
			<p>{noResultsMessage}</p>
		</div>
	{/if}
{/if}
