<script lang="ts">
	import { getMessage } from '$lib/utils/message-helper';
	import PetDetail from '$lib/components/pets/PetDetail.svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import type { PetOut } from '$lib/types/api/pet';
	const { data } = $props<{ data: { pet: PetOut } }>();
	const { pet } = data;
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<PageHeader title={pet.name || getMessage('pet_details_title')} />
		<div class="flex gap-2">
			<a href="/pets" class="inline-block">
				<Button type="secondary">&larr; {getMessage('back_to_list')}</Button>
			</a>
			<a href={`/pets/${pet.id}/edit`} class="inline-block">
				<Button type="primary">Edit</Button>
			</a>
		</div>
	</div>
	<PetDetail {pet} />
</div>
