<script lang="ts">
	import { session } from '$lib/stores/session';
	import { m } from '$lib/paraglide/messages';
	import { BACKEND_URL } from '$lib/config';
	import { onMount } from 'svelte';

	// ...existing code...
	let error = '';

	async function fetchSession() {
		error = '';
		try {
			const accessToken = localStorage.getItem('access_token');
			const res = await fetch(BACKEND_URL + 'api/users/me', {
				headers: { Authorization: `Bearer ${accessToken}` }
			});
			if (res.ok) {
				session.set({ user: await res.json() });
			} else {
				session.set(null);
				error = m.session_invalid();
			}
		} catch {
			error = m.network_error();
		}
	}

	function handleLogout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		session.set(null);
	}

	onMount(fetchSession);
</script>

<div class="mx-auto mt-16 max-w-md rounded bg-white p-8 shadow">
	<h1 class="mb-6 text-2xl font-bold">{m.auth_test_title()}</h1>
	{#if error}
		<div class="mb-4 text-red-600">{error}</div>
	{/if}
	{#if $session}
		<div class="mb-4">{m.session_greeting({ email: $session.user?.email || '' })}</div>
		<button
			class="w-full rounded bg-red-600 py-2 text-white hover:bg-red-700"
			on:click={handleLogout}
		>
			{m.logout_button()}
		</button>
	{:else}
		<div>{m.session_not_logged_in()}</div>
		<a href="/login" class="text-blue-600 hover:underline">{m.login_button()}</a>
	{/if}
</div>
