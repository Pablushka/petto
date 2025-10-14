<script lang="ts">
	import { session } from '$lib/stores/session';
	import { goto } from '$app/navigation';

	// Callback from parent (Svelte 5 style)
	const accountMenuProps = $props<{ onClose?: () => void }>();
	let { onClose } = accountMenuProps;

	let menuEl: HTMLDivElement | null = null;

	function focusFirstItem() {
		const items = menuEl?.querySelectorAll<HTMLButtonElement>('[role="menuitem"]');
		if (items && items.length > 0) {
			items[0].focus();
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		const items = Array.from(
			menuEl?.querySelectorAll<HTMLButtonElement>('[role="menuitem"]') || []
		);
		const activeIndex = items.findIndex((el) => el === document.activeElement);

		switch (e.key) {
			case 'Escape':
				e.preventDefault();
				onClose?.();
				break;
			case 'Tab': {
				if (items.length === 0) return;
				const first = items[0];
				const last = items[items.length - 1];
				// Trap focus inside the menu
				if (e.shiftKey) {
					if (document.activeElement === first) {
						e.preventDefault();
						last.focus();
					}
				} else {
					if (document.activeElement === last) {
						e.preventDefault();
						first.focus();
					}
				}
				break;
			}
			case 'ArrowDown': {
				e.preventDefault();
				if (items.length === 0) return;
				const next = activeIndex === -1 ? 0 : (activeIndex + 1) % items.length;
				items[next].focus();
				break;
			}
			case 'ArrowUp': {
				e.preventDefault();
				if (items.length === 0) return;
				const prev =
					activeIndex === -1 ? items.length - 1 : (activeIndex - 1 + items.length) % items.length;
				items[prev].focus();
				break;
			}
			case 'Home':
				e.preventDefault();
				items[0]?.focus();
				break;
			case 'End':
				e.preventDefault();
				items[items.length - 1]?.focus();
				break;
		}
	}

	function onProfile() {
		goto('/profile');
		onClose?.();
	}

	function onLogout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		session.set(null);
		goto('/login');
		onClose?.();
	}

	$effect(() => {
		// Delay to ensure elements are in DOM then focus
		const t = setTimeout(() => focusFirstItem());
		return () => clearTimeout(t);
	});
</script>

<div
	class="w-48 rounded bg-white py-2 shadow-md outline-none"
	role="menu"
	aria-label="Account menu"
	tabindex="-1"
	bind:this={menuEl}
	onkeydown={handleKeydown}
>
	<button
		class="w-full px-4 py-2 text-left hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
		role="menuitem"
		tabindex="-1"
		onclick={onProfile}
	>
		Profile
	</button>
	<button
		class="w-full px-4 py-2 text-left text-red-600 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
		role="menuitem"
		tabindex="-1"
		onclick={onLogout}
	>
		Logout
	</button>
</div>

<style>
	/* lightweight styles; project uses Tailwind but keep fallback */
</style>
