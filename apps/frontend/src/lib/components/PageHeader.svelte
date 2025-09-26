<script lang="ts">
	import { m } from '$lib/paraglide/messages';
	import { session } from '$lib/stores/session';
	import { derived } from 'svelte/store';
	import AccountMenu from './AccountMenu.svelte';

	const pageHeaderProps = $props<{ title?: string; subtitle?: string }>();
	let { title = '', subtitle = '' } = pageHeaderProps;

	// derive user's initials from session store
	const initials = derived(session, ($session) => {
		const user = $session?.user;
		if (!user) return null;
		const name = (user as any).name?.trim?.() || '';
		if (name) {
			const parts = name.split(/\s+/);
			const first = parts[0]?.[0] || '';
			const last = parts.length > 1 ? parts[parts.length - 1]?.[0] || '' : '';
			const letters = first + last || first;
			if (letters) return letters.toUpperCase();
		}
		// fallback to first letter of email
		const email = (user as any).email || '';
		return email ? email[0].toUpperCase() : null;
	});

	let open = $state(false);
	let avatarBtn: HTMLButtonElement | null = $state(null);
	let containerEl: HTMLDivElement | null = $state(null);

	function closeMenuAndRestoreFocus() {
		open = false;
		// Restore focus to the avatar button for keyboard users
		avatarBtn?.focus();
	}

	function onDocumentClick(e: MouseEvent) {
		const target = e.target as Node;
		if (open && containerEl && !containerEl.contains(target)) {
			closeMenuAndRestoreFocus();
		}
	}

	if (typeof window !== 'undefined') {
		window.addEventListener('click', onDocumentClick);
	}

	// Svelte 5 still supports onDestroy
	import { onDestroy } from 'svelte';
	onDestroy(() => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('click', onDocumentClick);
		}
	});
</script>

{#if title}
	<div class="mb-6 flex items-start justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">{title}</h1>
			{#if subtitle}
				<p class="mt-2 text-lg text-gray-600">{subtitle}</p>
			{/if}
		</div>
	</div>
{/if}

{#if $session?.user}
	<div class="fixed top-4 right-4 z-50" bind:this={containerEl}>
		<div class="relative">
			<button
				class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 font-semibold text-white focus:ring-2 focus:ring-blue-400 focus:outline-none"
				aria-haspopup="menu"
				aria-expanded={open}
				aria-label="Account menu"
				onclick={() => (open = !open)}
				onkeydown={(e) => e.key === 'ArrowDown' && (open = true)}
				bind:this={avatarBtn}
			>
				{#if $initials}
					{$initials}
				{:else}
					?
				{/if}
			</button>

			{#if open}
				<div class="absolute right-0 z-50 mt-2">
					<AccountMenu onClose={closeMenuAndRestoreFocus} />
				</div>
			{/if}
		</div>
	</div>
{/if}
