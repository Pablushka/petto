<script lang="ts">
  	import FlyerThumb from './FlyerThumb.svelte';
	import type { PetOut } from '$lib/types/api/pet';

	let { pet, flyerHtml = '' }: { pet: PetOut; flyerHtml?: string } = $props();


</script>

<div class="flyer-generator">
	<div class="grid grid-cols-3 gap-2 items-start">
		<FlyerThumb flyerHtml={flyerHtml} petId={pet.id}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml} petId={pet.id}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml} petId={pet.id}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml} petId={pet.id}></FlyerThumb>
		<FlyerThumb flyerHtml={flyerHtml} petId={pet.id}></FlyerThumb>
	</div>
</div>

