<script lang="ts">
	import { session, buildSession } from '$lib/stores/session';
	// 'm' not used here; import removed
	import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
	import { getMessage } from '$lib/utils/message-helper';
	import { get } from '$lib/utils/api';
	import { BACKEND_URL } from '$lib/config';
	import type { UserOutput } from '$lib/types/api/user';

	// ...existing code...
	let error = $state('');

	async function fetchSession() {
		error = '';
		try {
			const user = await get<UserOutput>('api/users/me', {
				requireAuth: true,
				credentials: 'include'
			});
			session.set(buildSession(user));
		} catch (err) {
			session.set(null);
			error = getMessage('network_error');
		}
	}

	async function handleLogout() {
		try {
			await fetch(`${BACKEND_URL}/api/logout`, {
				method: 'POST',
				credentials: 'include'
			});
		} catch (err) {
			console.warn('Failed to logout', err);
		}
		session.set(null);
	}

	$effect(() => {
		fetchSession();
	});
</script>

<ProtectedRoute>
	<div class="mx-auto mt-16 max-w-md rounded bg-white p-8 shadow">
		<h1 class="mb-6 text-2xl font-bold">{getMessage('auth_test_title')}</h1>
		{#if error}
			<div class="mb-4 text-red-600">{error}</div>
		{/if}
		{#if $session}
			<div class="mb-4">
				{getMessage('session_greeting', { email: $session.user?.email || '' })}
			</div>
			<button
				class="w-full rounded bg-red-600 py-2 text-white hover:bg-red-700"
				onclick={handleLogout}
			>
				{getMessage('logout_button')}
			</button>
		{:else}
			<div>{getMessage('session_not_logged_in')}</div>
			<a href="/login" class="text-blue-600 hover:underline">{getMessage('login_button')}</a>
		{/if}
	</div>
</ProtectedRoute>
