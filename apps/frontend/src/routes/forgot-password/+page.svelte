<script lang="ts">
  import { m } from '$lib/paraglide/messages';
  let email = '';
  let sent = false;
  let error = '';

  async function handleForgot() {
    error = '';
    try {
      const res = await fetch('/api/forgot-password', {
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

<div class="max-w-md mx-auto mt-16 p-8 bg-white rounded shadow">
  <h1 class="text-2xl font-bold mb-6">{m.forgot_title()}</h1>
  {#if sent}
    <div class="text-green-600">{m.forgot_success()}</div>
  {:else}
    {#if error}
      <div class="mb-4 text-red-600">{error}</div>
    {/if}
    <form on:submit|preventDefault={handleForgot} class="space-y-4">
      <div>
        <label class="block mb-1 font-medium">{m.email_label()}</label>
        <input type="email" bind:value={email} required class="w-full border rounded px-3 py-2" />
      </div>
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        {m.forgot_button()}
      </button>
    </form>
  {/if}
</div>
