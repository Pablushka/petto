<script lang="ts">
  import { m } from '$lib/paraglide/messages';
  import { goto } from '$app/navigation';
  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleLogin() {
    loading = true;
    error = '';
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        error = m.login_failed();
        loading = false;
        return;
      }
      const { access_token, refresh_token } = await res.json();
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      goto('/auth-test');
    } catch (e) {
      error = m.network_error();
    }
    loading = false;
  }
</script>

<div class="max-w-md mx-auto mt-16 p-8 bg-white rounded shadow">
  <h1 class="text-2xl font-bold mb-6">{m.login_title()}</h1>
  {#if error}
    <div class="mb-4 text-red-600">{error}</div>
  {/if}
  <form on:submit|preventDefault={handleLogin} class="space-y-4">
    <div>
      <label class="block mb-1 font-medium">{m.email_label()}</label>
      <input type="email" bind:value={email} required class="w-full border rounded px-3 py-2" />
    </div>
    <div>
      <label class="block mb-1 font-medium">{m.password_label()}</label>
      <input type="password" bind:value={password} required class="w-full border rounded px-3 py-2" />
    </div>
    <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700" disabled={loading}>
      {loading ? m.loading() : m.login_button()}
    </button>
  </form>
  <div class="mt-4 text-sm">
    <a href="/forgot-password" class="text-blue-600 hover:underline">{m.forgot_password_link()}</a>
  </div>
</div>
