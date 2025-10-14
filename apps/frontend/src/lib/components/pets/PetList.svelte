<script lang="ts">
	import LoadingState from '../LoadingState.svelte';
	import Alert from '../Alert.svelte';
	import PetCard from './PetCard.svelte';
	import TextField from '../TextField.svelte';
	import Button from '../Button.svelte';
	import Pagination from '../Pagination.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import { get } from '$lib/utils/api';

	import type { PetOut } from '$lib/types/api/pet';

	// Backend /api/pets returns an array of PetOut (we page client-side for now)
	type PetsResponse = PetOut[];

	// Pet list state
	let pets = $state<PetOut[]>([]);
	let loading = $state(true);
	let error = $state('');

	// Filter and pagination state
	let searchQuery = $state('');
	let currentPage = $state(1);
	let itemsPerPage = $state(9);

	// Derived pagination computations (explicit numbers)
	let totalItems = $state(0);
	let totalPages = $state(1);
	let startIndex = $state(0);
	let endIndex = $state(0);
	let pagedPets = $state<PetOut[]>([]);

	// Recompute derived values when inputs change
	$effect(() => {
		totalItems = pets.length;
		totalPages = Math.max(1, Math.ceil(totalItems / itemsPerPage));
		if (currentPage > totalPages) {
			currentPage = totalPages;
		}
		if (currentPage < 1) currentPage = 1;
		startIndex = (currentPage - 1) * itemsPerPage;
		endIndex = startIndex + itemsPerPage;
		pagedPets = pets.slice(startIndex, endIndex);
	});

	// Status filter options
	// Placeholder: status filtering removed; backend model does not expose status currently

	// Load pets from API
	async function fetchPets() {
		loading = true;
		error = '';

		try {
			// Construct query parameters
			// Build query string manually to avoid mutable URLSearchParams lint rule
			const paramsArr = [
				`page=${encodeURIComponent(currentPage.toString())}`,
				`limit=${encodeURIComponent(itemsPerPage.toString())}`
			];
			if (searchQuery) paramsArr.push(`search=${encodeURIComponent(searchQuery)}`);
			const qs = paramsArr.join('&');

			// Backend currently returns full list (no pagination metadata). Adjust when API adds paging.
			const data = await get<PetsResponse>(`api/pets?${qs}`, { requireAuth: true });
			// Ensure array shape
			pets = Array.isArray(data) ? data : [];
		} catch (err) {
			console.error('Error fetching pets:', err);
			error = getMessage('network_error');
		}
		loading = false;
	}

	// Handle search
	function handleSearch() {
		currentPage = 1;
		fetchPets();
	}

	// Handle filter change
	// Filter handler removed (status not in backend model)

	// Handle page change
	function handlePageChange(page: number) {
		currentPage = page;
		fetchPets();
	}

	// Fetch pets initially and whenever dependencies change using Svelte 5 runes
	$effect(() => {
		fetchPets();
	});
</script>

<div>
	<!-- Search and Filter Controls -->
	<div class="mb-6 rounded-lg bg-white p-4 shadow">
		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			<div class="md:col-span-2">
				<TextField
					label=""
					name="search"
					bind:value={searchQuery}
					placeholder={getMessage('pet_search_placeholder')}
				/>
			</div>

			<div class="flex justify-end md:col-span-3">
				<Button type="primary" onclick={handleSearch}>
					{getMessage('button_submit')}
				</Button>
			</div>
		</div>
	</div>

	{#if error}
		<div class="mb-4">
			<Alert type="error" message={error} />
		</div>
	{/if}

	<!-- Pets List -->
	<LoadingState {loading} noResultsMessage={getMessage('pet_no_results')}>
		{#if !loading && Array.isArray(pets) && pets.length > 0}
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
				{#each pagedPets as pet (pet.id)}
					<PetCard {pet} />
				{/each}
			</div>
			<Pagination {currentPage} {totalPages} onPageChange={handlePageChange} />
		{/if}
	</LoadingState>
</div>
