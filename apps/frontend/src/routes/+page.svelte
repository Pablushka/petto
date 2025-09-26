<script lang="ts">
	import { m } from '$lib/paraglide/messages';
	import { session } from '$lib/stores/session';
	import Button from '$lib/components/Button.svelte';
	import { getMessage } from '$lib/utils/message-helper';
</script>

<div class="flex flex-col items-center py-12 md:py-24">
	<h1 class="mb-6 text-center text-4xl font-bold md:text-5xl">
		{getMessage('reunite_lost_pets')}
	</h1>

	<p class="mb-12 max-w-3xl text-center text-lg text-gray-600 md:text-xl">
		{getMessage('reunite_lost_pets_description')}
	</p>

	<div class="flex flex-col gap-4 sm:flex-row">
		<a href="/pets">
			<Button type="primary" size="lg">
				{getMessage('view_listings')}
			</Button>
		</a>

		{#if $session?.user}
			<a href="/pets/report">
				<Button type="secondary" size="lg">
					{getMessage('pet_report_lost')}
				</Button>
			</a>
		{:else}
			<a href="/login">
				<Button type="secondary" size="lg">
					{getMessage('login_title')}
				</Button>
			</a>
		{/if}
	</div>

	<div class="mt-24 grid max-w-6xl grid-cols-1 gap-12 md:grid-cols-3">
		<div class="text-center">
			<div class="mb-4 inline-flex rounded-full bg-blue-100 p-4 text-blue-700">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-8 w-8"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
					/>
				</svg>
			</div>
			<h2 class="mb-2 text-xl font-bold">{getMessage('feature_report_title')}</h2>
			<p class="text-gray-600">
				{getMessage('feature_report_description')}
			</p>
		</div>

		<div class="text-center">
			<div class="mb-4 inline-flex rounded-full bg-green-100 p-4 text-green-700">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-8 w-8"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
			</div>
			<h2 class="mb-2 text-xl font-bold">{getMessage('feature_found_title')}</h2>
			<p class="text-gray-600">
				{getMessage('feature_found_description')}
			</p>
		</div>

		<div class="text-center">
			<div class="mb-4 inline-flex rounded-full bg-purple-100 p-4 text-purple-700">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-8 w-8"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
			</div>
			<h2 class="mb-2 text-xl font-bold">{getMessage('feature_browse_title')}</h2>
			<p class="text-gray-600">
				{getMessage('feature_browse_description')}
			</p>
		</div>
	</div>
</div>
