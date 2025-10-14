<script lang="ts">
	// 'm' not used here; import removed
	import Button from '$lib/components/Button.svelte';
	import PetList from '$lib/components/pets/PetList.svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import { session } from '$lib/stores/session';
	import { getMessage } from '$lib/utils/message-helper';

	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
</script>

<ProtectedRoute>
	<PageHeader title={getMessage('pets_title')} />

	<div class="space-y-8">
		<!-- Actions Bar -->
		<div class="flex justify-end space-x-4">
			{#if $session?.user}
				<a href="/pets/add">
					<Button type="secondary">
						{getMessage('add_new_pet')}
					</Button>
				</a>
				<a href="/pets/report">
					<Button type="primary">
						{getMessage('pet_report_lost')}
					</Button>
				</a>
			{:else}
				<a href="/login">
					<Button type="secondary">
						{getMessage('login_title')}
					</Button>
				</a>
			{/if}
		</div>

		<!-- Pet List Component -->
		<PetList />
	</div>
</ProtectedRoute>
