<script lang="ts">
	import { m } from '$lib/paraglide/messages';

	const props = $props<{
		currentPage?: number;
		totalPages?: number;
		onPageChange?: (page: number) => void;
	}>();
	let { currentPage = 1, totalPages = 1, onPageChange } = props;

	// Define maximum number of page buttons to show
	const maxButtons = 5;

	let pageNumbers = $derived(getPageNumbers(currentPage, totalPages, maxButtons));

	// Function to calculate which page numbers to display
	function getPageNumbers(current: number, total: number, max: number): number[] {
		if (total <= max) {
			// If total pages is less than or equal to max buttons, show all pages
			return Array.from({ length: total }, (_, i) => i + 1);
		}

		// Calculate how many buttons to show on each side of current page
		const sideButtons = Math.floor((max - 3) / 2);
		const leftSide = Math.max(2, current - sideButtons);
		const rightSide = Math.min(total - 1, current + sideButtons);

		const pages: number[] = [1];

		// Add ellipsis if needed on left side
		if (leftSide > 2) {
			pages.push(-1); // -1 represents ellipsis
		}

		// Add middle pages
		for (let i = leftSide; i <= rightSide; i++) {
			pages.push(i);
		}

		// Add ellipsis if needed on right side
		if (rightSide < total - 1) {
			pages.push(-1); // -1 represents ellipsis
		}

		// Add last page
		if (total > 1) {
			pages.push(total);
		}

		return pages;
	}

	function handlePageChange(page: number) {
		if (page !== currentPage && page > 0 && page <= totalPages) {
			onPageChange?.(page);
		}
	}
</script>

{#if totalPages > 1}
	<div class="mt-6 flex justify-center">
		<nav class="inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
			<!-- Previous button -->
			<button
				class="relative inline-flex items-center rounded-l-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50"
				onclick={() => handlePageChange(currentPage - 1)}
				disabled={currentPage === 1}
				aria-label="Previous page"
			>
				&laquo;
			</button>

			<!-- Page numbers -->
			{#each pageNumbers as page}
				{#if page === -1}
					<!-- Ellipsis -->
					<span
						class="relative inline-flex items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700"
					>
						&hellip;
					</span>
				{:else}
					<!-- Page number button -->
					<button
						class="relative inline-flex items-center border border-gray-300 px-4 py-2 text-sm font-medium
              {page === currentPage
							? 'z-10 border-blue-500 bg-blue-50 text-blue-600'
							: 'bg-white text-gray-700 hover:bg-gray-50'}"
						onclick={() => handlePageChange(page)}
						aria-current={page === currentPage ? 'page' : undefined}
					>
						{page}
					</button>
				{/if}
			{/each}

			<!-- Next button -->
			<button
				class="relative inline-flex items-center rounded-r-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50"
				onclick={() => handlePageChange(currentPage + 1)}
				disabled={currentPage === totalPages}
				aria-label="Next page"
			>
				&raquo;
			</button>
		</nav>
	</div>
{/if}
