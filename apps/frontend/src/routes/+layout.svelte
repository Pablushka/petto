<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/petto.svg';
	import PageHeader from '$lib/components/PageHeader.svelte';
	// 'm' not used here; import removed
	import { getLocale } from '$lib/paraglide/runtime';
	import { session } from '$lib/stores/session';
	import type { UserOutput } from '$lib/types/api/user';
	import { getMessage } from '$lib/utils/message-helper';
	import SelectLang from '$lib/components/SelectLang.svelte';
	const { children, data } = $props();

	type Locale = 'en' | 'es' | 'jp';

	let locale = $state(getLocale());
	let showMenu = $state(false);
	let user = $state<UserOutput | null>(null);

	$effect(() => {
		const unsubscribe = session.subscribe((s) => {
			user = s?.user ?? null;
		});
		return unsubscribe;
	});

	$effect(() => {
		if (data === undefined) {
			return;
		}
		if (data?.user) {
			session.set({ user: data.user });
		} else {
			session.set(null);
		}
	});

	function handleLocaleChanged(selected: Locale) {
		// In Svelte 5, the parameter is the value passed to the event function
		locale = selected;
		console.log('Locale changed to:', locale);
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex min-h-screen flex-col bg-gray-50">
	<header class="bg-white shadow">
		<div class="container mx-auto flex items-center justify-between px-4 py-4">
			<div class="flex items-center gap-2">
				<img src={favicon} alt="Petto" class="h-8 w-8" />
				<span class="text-xl font-bold text-blue-700">Petto</span>
			</div>
			<nav class="hidden gap-6 md:flex">
				<a href="/" class="hover:text-blue-600">{getMessage('nav_home')}</a>
				<a href="/pets" class="hover:text-blue-600">{getMessage('nav_pets')}</a>
				<a href="/login" class="hover:text-blue-600">{getMessage('login_title')}</a>
				<a href="/auth-test" class="hover:text-blue-600">{getMessage('nav_auth_test')}</a>
				<a href="/demo" class="hover:text-blue-600">{getMessage('nav_demo')}</a>
			</nav>
			<div class="flex items-center gap-2">
				<SelectLang
					items={[
						{ id: 'en', option_text: 'EN' },
						{ id: 'es', option_text: 'ES' },
						{ id: 'jp', option_text: 'JP' }
					]}
					bind:selected={locale}
					onChange={handleLocaleChanged}
				/>
				{#if user}
					<span class="ml-4 text-sm text-gray-700">{user.name}</span>
				{/if}
			</div>
			<button
				class="ml-2 md:hidden"
				onclick={() => (showMenu = !showMenu)}
				aria-label="Toggle menu"
				aria-expanded={showMenu}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 6h16M4 12h16M4 18h16"
					/></svg
				>
			</button>
		</div>
		{#if showMenu}
			<nav class="border-t bg-white md:hidden">
				<a href="/" class="block px-4 py-2 hover:bg-blue-50">{getMessage('nav_home')}</a>
				<a href="/pets" class="block px-4 py-2 hover:bg-blue-50">{getMessage('nav_pets')}</a>
				<a href="/login" class="block px-4 py-2 hover:bg-blue-50">{getMessage('login_title')}</a>
				<a href="/auth-test" class="block px-4 py-2 hover:bg-blue-50"
					>{getMessage('nav_auth_test')}</a
				>
				<a href="/demo" class="block px-4 py-2 hover:bg-blue-50">{getMessage('nav_demo')}</a>
			</nav>
		{/if}
	</header>
	<!-- Global PageHeader: renders only the avatar/menu when no title is provided -->
	<PageHeader title="" subtitle="" />
	<main class="container mx-auto flex-1 px-4 py-8">
		{@render children?.()}
	</main>
	<footer class="mt-auto border-t bg-white py-4">
		<div class="container mx-auto px-4 text-center text-sm text-gray-500">
			&copy; {new Date().getFullYear()} Petto. {getMessage('all_rights_reserved')}
		</div>
	</footer>
</div>
