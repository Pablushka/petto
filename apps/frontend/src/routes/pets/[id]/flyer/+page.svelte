<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import FlyerGenerator from '$lib/components/FlyerGenerator.svelte';
	import { getMessage } from '$lib/utils/message-helper';

	export let data: {
		pet: any;
		owner: any;
	};

	$: pet = data.pet;

	function goBack() {
		goto(`/pets/${data.pet.id}`);
	}
</script>

<div class="flyer-page">
	<div class="container mx-auto px-4 py-8">
		<div class="mb-6 flex items-center justify-between">
			<PageHeader title="{getMessage('print_flyer')} - {data.pet.name}" />
			<Button onclick={goBack} type="secondary">&larr; {getMessage('back_to_pet')}</Button>
		</div>

		<div class="rounded-lg bg-white p-6 shadow">
			<FlyerGenerator {pet} owner={data.owner} />
		</div>
	</div>
</div>
