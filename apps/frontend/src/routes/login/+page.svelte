<script lang="ts">
	// 'm' not used here; import removed
	import { goto } from '$app/navigation';
	import { BACKEND_URL } from '$lib/config';
	import { get } from '$lib/utils/api';
	import { getMessage } from '$lib/utils/message-helper';
	import { session, buildSession } from '$lib/stores/session';
	import type { UserOutput } from '$lib/types/api/user';
	import { page } from '$app/state';

	let email = '';
	let password = '';
	let error = '';
	let loading = false;

	async function handleLogin() {
		loading = true;
		error = '';
		try {
			const res = await fetch(BACKEND_URL + 'api/login', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password }),
				credentials: 'include'
			});
			if (!res.ok) {
				error = getMessage('login_failed');
				loading = false;
				return;
			}
			const tokens = await res.json();
			// Best-effort: populate session after successful login
			try {
				const user = await get<UserOutput>('api/users/me', {
					requireAuth: true,
					credentials: 'include'
				});
				session.set(buildSession(user));
			} catch (fetchErr) {
				console.warn('Unable to load user after login', fetchErr);
				session.set(null);
			}
			const returnTo = page.url.searchParams.get('returnUrl') || '/';
			goto(returnTo);
		} catch (err) {
			console.error('login failed', err);
			error = getMessage('network_error');
		}
		loading = false;
	}
</script>

<div class="mx-auto mt-16 max-w-md rounded bg-white p-8 shadow">
	<h1 class="mb-6 text-2xl font-bold">{getMessage('login_title')}</h1>
	{#if error}
		<div class="mb-4 text-red-600">{error}</div>
	{/if}
	<form
		onsubmit={(e) => {
			e.preventDefault();
			handleLogin();
		}}
		class="space-y-4"
	>
		<div>
			<label for="email" class="mb-1 block font-medium">{getMessage('email_label')}</label>
			<input
				id="email"
				type="email"
				bind:value={email}
				required
				class="w-full rounded border px-3 py-2"
			/>
		</div>
		<div>
			<label for="password" class="mb-1 block font-medium">{getMessage('password_label')}</label>
			<input
				id="password"
				type="password"
				bind:value={password}
				required
				class="w-full rounded border px-3 py-2"
			/>
		</div>
		<button
			type="submit"
			class="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700"
			disabled={loading}
		>
			{loading ? getMessage('loading') : getMessage('login_button')}
		</button>
	</form>
	<div class="mt-4 text-sm">
		<a href="/forgot-password" class="text-blue-600 hover:underline"
			>{getMessage('forgot_password_link')}</a
		>
	</div>
</div>
