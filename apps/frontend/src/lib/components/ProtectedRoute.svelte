<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { session } from '$lib/stores/session';
	import { get } from '$lib/utils/api';

	const protectedRouteProps = $props<{ returnTo?: string; children?: (props?: any) => any }>();
	let { returnTo = '', children } = protectedRouteProps;

	async function checkAuth() {
		if (!browser) return;

		// Check if we already have a session
		if ($session?.user) return;

		// No session in store, check if we have a token
		const accessToken = localStorage.getItem('access_token');
		if (!accessToken) {
			redirectToLogin();
			return;
		}

		// We have a token, try to fetch user data
		try {
			// Use API helper so 401 triggers refresh flow automatically
			const userData = await get<any>('api/users/me', { requireAuth: true });
			session.set({ user: userData });
		} catch (error) {
			// Network error or other exception
			console.error('Authentication check failed:', error);
			redirectToLogin();
		}
	}

	function redirectToLogin() {
		const path = returnTo || window.location.pathname;
		goto(`/login?returnUrl=${encodeURIComponent(path)}`);
	}

	onMount(checkAuth);
</script>

{@render children?.()}
