<script lang="ts">
	// 'm' not used here; import removed

	let {
		title = '',
		isOpen = $bindable(false),
		size = 'md',
		children,
		footer
	} = $props<{
		title?: string;
		isOpen?: boolean;
		size?: 'sm' | 'md' | 'lg' | 'xl';
		children?: (props?: unknown) => unknown;
		footer?: (props?: unknown) => unknown;
	}>();

	// Width classes based on size
	const sizeClasses = {
		sm: 'max-w-md',
		md: 'max-w-lg',
		lg: 'max-w-2xl',
		xl: 'max-w-4xl'
	};

	function closeModal() {
		isOpen = false;
	}

	// Close modal when Escape key is pressed
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && isOpen) {
			closeModal();
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
	<div
		class="bg-opacity-50 fixed inset-0 z-50 flex items-center justify-center bg-black p-4"
		onclick={(e) => (e.currentTarget === e.target ? closeModal() : null)}
		onkeydown={handleKeydown}
		role="presentation"
	>
		<div
			class={`${sizeClasses[size as 'sm' | 'md' | 'lg' | 'xl']} w-full overflow-hidden rounded-lg bg-white shadow-xl`}
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
		>
			<!-- Header -->
			<div class="flex items-center justify-between border-b px-6 py-4">
				<h3 id="modal-title" class="text-lg font-medium">{title}</h3>
				<button
					class="text-gray-400 hover:text-gray-500"
					onclick={closeModal}
					aria-label="Close modal"
				>
					
				</button>
			</div>

			<!-- Content -->
			<div class="px-6 py-4">
				{@render children?.()}
			</div>

			<!-- Footer (optional) -->
			{@render footer?.()}
		</div>
	</div>
{/if}
