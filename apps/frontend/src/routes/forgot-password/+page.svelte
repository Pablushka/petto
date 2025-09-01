<script lang="ts">
	import { m } from '$lib/paraglide/messages';
	import { BACKEND_URL } from '$lib/config';
	let email = '';
	let sent = false;
	let error = '';

	async function handleForgot() {
		error = '';
		try {
			const res = await fetch(`${BACKEND_URL}api/forgot-password`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email })
			});
			if (!res.ok) {
				error = m.forgot_failed();
				return;
			}
			sent = true;
		} catch (e) {
			error = m.network_error();
		}
	}
</script>

<div class="mx-auto mt-16 max-w-md rounded bg-white p-8 shadow">
	<h1 class="mb-6 text-2xl font-bold">{m.forgot_title()}</h1>
	{#if sent}
		<div class="text-green-600">{m.forgot_success()}</div>
	{:else}
		{#if error}
			<div class="mb-4 text-red-600">{error}</div>
		{/if}
		<form on:submit|preventDefault={handleForgot} class="space-y-4">
			<div>
				<label class="mb-1 block font-medium">{m.email_label()}</label>
				<input type="email" bind:value={email} required class="w-full rounded border px-3 py-2" />
			</div>
			<button type="submit" class="w-full rounded bg-blue-600 py-2 text-white hover:bg-blue-700">
				{m.forgot_button()}
			</button>
		</form>
	{/if}
</div>
