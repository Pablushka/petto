<script lang="ts">
	import { m } from '$lib/paraglide/messages';
	import { onMount } from 'svelte';
	import LoadingState from '../LoadingState.svelte';
	import PetCard from './PetCard.svelte';
	import TextField from '../TextField.svelte';
	import Button from '../Button.svelte';
	import Pagination from '../Pagination.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import { get } from '$lib/utils/api';

	import type { PetOut } from '$lib/types/api/pet';

	// Simplified list typing: backend /api/pets returns an array of PetOut (we page client-side for now)
	type PetsResponse = PetOut[];

	// Pet list state
	let pets: PetOut[] = [];
	let loading = true;
	let error = '';

	// Filter and pagination state
	let searchQuery = '';
	let currentPage = 1;
	let totalPages = 1;
	let itemsPerPage = 9;

	// Status filter options
	// Placeholder: status filtering removed; backend model does not expose status currently

	// Load pets from API
	async function fetchPets() {
		loading = true;
		error = '';

		try {
			// Construct query parameters
			const params = new URLSearchParams();
			params.append('page', currentPage.toString());
			params.append('limit', itemsPerPage.toString());

			if (searchQuery) {
				params.append('search', searchQuery);
			}

			// Backend currently returns full list (no pagination metadata). Adjust when API adds paging.
			const data = await get<PetsResponse>(`api/pets?${params.toString()}`, { requireAuth: true });
			pets = data ?? [];
			totalPages = Math.ceil(pets.length / itemsPerPage) || 1;
		} catch (err) {
			console.error('Error fetching pets:', err);
			error = getMessage('network_error');
			loading = false;
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

	// Fetch pets on component mount
	onMount(fetchPets);
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

	<!-- Pets List -->
	<LoadingState {loading} noResultsMessage={getMessage('pet_no_results')}>
		{#if pets.length > 0}
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
				{#each pets.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage) as pet (pet.id)}
					<PetCard {pet} />
				{/each}
			</div>
			<Pagination {currentPage} {totalPages} onPageChange={handlePageChange} />
		{/if}
	</LoadingState>
</div>
