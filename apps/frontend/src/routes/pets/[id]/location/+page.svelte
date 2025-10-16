<script lang="ts">
	import { getMessage } from '$lib/utils/message-helper';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import Button from '$lib/components/Button.svelte';
	import { goto } from '$app/navigation';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();
	const { lastScan } = data;

	function goBack() {
		goto(`/pets/${lastScan?.pet_id}`);
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<PageHeader title={getMessage('pet_location_title')} />
		<Button onclick={goBack} type="secondary">&larr; {getMessage('back_to_pet')}</Button>
	</div>

	{#if lastScan}
		<div class="rounded-lg bg-white p-6 shadow">
			<h2 class="mb-4 text-xl font-semibold">{getMessage('last_scan_location')}</h2>
			<div class="space-y-2">
				<p>
					<strong>{getMessage('scan_location')}:</strong>
					{lastScan.scan_location || getMessage('unknown_location')}
				</p>
				<p>
					<strong>{getMessage('scan_time')}:</strong>
					{new Date(lastScan.scan_time).toLocaleString()}
				</p>
				<p>
					<strong>{getMessage('qr_link')}:</strong>
					<a href={lastScan.qr_link} target="_blank" class="text-blue-600 hover:underline"
						>{lastScan.qr_link}</a
					>
				</p>
			</div>
		</div>
	{:else}
		<div class="rounded-lg bg-white p-6 shadow">
			<p>{getMessage('no_scans_found')}</p>
		</div>
	{/if}
</div>
