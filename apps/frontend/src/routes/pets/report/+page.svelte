<script lang="ts">
	import PageHeader from '$lib/components/PageHeader.svelte';
	import PetForm from '$lib/components/pets/PetForm.svelte';
	import Button from '$lib/components/Button.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
</script>

<ProtectedRoute>
	<div class="space-y-6">
		<div class="flex items-center justify-between">
			<PageHeader title={getMessage('pet_report_lost')} />

			<div>
				<a href="/pets" class="inline-block">
					<Button type="secondary">
						&larr; {getMessage('back_to_list')}
					</Button>
				</a>
			</div>
		</div>

		<PetForm />
	</div>
</ProtectedRoute>
