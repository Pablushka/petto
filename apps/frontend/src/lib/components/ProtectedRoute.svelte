<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { session, buildSession } from '$lib/stores/session';
	import type { UserOutput } from '$lib/types/api/user';
	import { get } from '$lib/utils/api';

	const protectedRouteProps = $props<{
		returnTo?: string;
		children?: (props?: unknown) => unknown;
	}>();
	let { returnTo = '', children } = protectedRouteProps;

	async function checkAuth() {
		if (!browser) return;

		if ($session?.user) return;

		try {
			const userData = await get<UserOutput>('api/users/me', {
				requireAuth: true
			});
			session.set(buildSession(userData));
		} catch (error) {
			console.error('Authentication check failed:', error);
			session.set(null);
			redirectToLogin();
		}
	}

	function redirectToLogin() {
		const path = returnTo || window.location.pathname;
		goto(`/login?returnUrl=${encodeURIComponent(path)}`);
	}

	$effect(() => {
		checkAuth();
	});
</script>

{@render children?.()}
