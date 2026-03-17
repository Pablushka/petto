<script lang="ts">
  	import FlyerThumb from './FlyerThumb.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import type { PetOut } from '$lib/types/api/pet';
	import { BACKEND_URL } from '$lib/config';
	import Button from '$lib/components/Button.svelte';

	let { pet, flyerHtml = '' }: { pet: PetOut; flyerHtml?: string } = $props();


</script>

<div class="flyer-generator">
	<div class="toolbar mb-4 flex gap-4">
		<Button
			type="primary"
			onclick={() => window.open(`${BACKEND_URL}api/flyers/${pet.id}`, '_blank')}
		>
			🖨️ {getMessage('print_flyer')}
		</Button>
		<Button type="secondary" onclick={() => alert('Function to export image coming soon')}>
			📷 {getMessage('export_image')}
		</Button>
	</div>

	<div class="grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-4 items-start">
		<FlyerThumb flyerHtml={flyerHtml}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml}></FlyerThumb>		

	</div>

</div>

