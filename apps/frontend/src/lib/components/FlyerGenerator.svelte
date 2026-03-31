<script lang="ts">
	import FlyerThumb from './FlyerThumb.svelte';
	import type { PetOut } from '$lib/types/api/pet';

	type FlyerTemplatePreview = {
		name: string;
		html: string;
	};

	let {
		pet,
		flyerTemplates = []
	}: { pet: PetOut; flyerTemplates?: FlyerTemplatePreview[] } = $props();
</script>

<div class="flyer-generator">
	<div class="grid grid-cols-1 gap-2 items-start md:grid-cols-3 lg:grid-cols-4">
		{#each flyerTemplates as flyerTemplate (flyerTemplate.name)}
			<FlyerThumb
				flyerHtml={flyerTemplate.html}
				petId={pet.id}
				templateName={flyerTemplate.name}
			></FlyerThumb>
		{/each}
	</div>
</div>
