<script lang="ts">
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import FlyerGenerator from '$lib/components/FlyerGenerator.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import type { PetOut } from '$lib/types/api/pet';
	import type { UserOutput } from '$lib/types/api/user';
	import { resolve } from '$app/paths';

	type FlyerTemplatePreview = {
		name: string;
		html: string;
	};

	export let data: {
		pet: PetOut;
		owner: UserOutput | Record<string, unknown>;
		flyerTemplates: FlyerTemplatePreview[];
	};

	const pet: PetOut = data.pet;
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<PageHeader title={`${getMessage('print_flyer')} - ${data.pet.name}`} />
		<div class="flex gap-2">
			<a href={resolve(`/pets/${data.pet.id}`)} class="inline-block" data-sveltekit-preload-data="hover">
				<Button type="secondary">&larr; {getMessage('back_to_pet')}</Button>
			</a>
		</div>
	</div>

	<div class="rounded-lg bg-white p-6 shadow">
		<FlyerGenerator {pet} flyerTemplates={data.flyerTemplates} />
	</div>
</div>
