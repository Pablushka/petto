<script lang="ts">
  import { m } from '$lib/paraglide/messages';
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  const session = writable<{ email?: string } | null>(null);
  let error = '';

  async function fetchSession() {
    error = '';
    try {
      const accessToken = localStorage.getItem('access_token');
      const res = await fetch('/api/me', {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      if (res.ok) {
        session.set(await res.json());
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

<div class="max-w-md mx-auto mt-16 p-8 bg-white rounded shadow">
  <h1 class="text-2xl font-bold mb-6">{m.auth_test_title()}</h1>
  {#if error}
    <div class="mb-4 text-red-600">{error}</div>
  {/if}
  {#if $session}
    <div class="mb-4">{m.session_greeting({ email: $session.email })}</div>
    <button class="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700" on:click={handleLogout}>
      {m.logout_button()}
    </button>
  {:else}
    <div>{m.session_not_logged_in()}</div>
    <a href="/login" class="text-blue-600 hover:underline">{m.login_button()}</a>
  {/if}
</div>
