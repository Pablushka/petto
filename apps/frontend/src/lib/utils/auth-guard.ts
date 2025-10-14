/**
 * Authentication guard utilities for Svelte components
 *
 * This module provides functionality to protect routes and components
 * by checking if the user is authenticated before allowing access.
 * It works with the Svelte component lifecycle to ensure authentication
 * checks happen at the appropriate time.
 *
 * @module auth-guard
 */

import { goto } from '$app/navigation';
import { browser } from '$app/environment';

/**
 * Checks if the user is authenticated and redirects to login if not
 *
 * This function should be called within a Svelte component to ensure
 * that only authenticated users can access the component. It uses
 * the onMount lifecycle hook to perform the check after the component
 * is mounted in the DOM.
 *
 * When a user is not authenticated (no access token in localStorage),
 * they are redirected to the login page with the current path as the
 * return URL, allowing them to be redirected back after successful login.
 *
 * Example usage in a Svelte component:
 * ```svelte
 * <script>
 *   import { checkAuth } from '$lib/utils/auth-guard';
 *   checkAuth();
 * </script>
 * ```
 *
 * @returns {void}
 */
export const checkAuth = () => {
	// This utility is intentionally synchronous and side-effecting so callers can
	// invoke it inside Svelte 5 runes (e.g. $effect) from components. It avoids
	// using component lifecycle helpers directly so the rule enforcement can apply.
	if (!browser) return;
	const token = localStorage.getItem('access_token');
	if (!token) {
		const currentPath = window.location.pathname;
		goto(`/login?returnUrl=${encodeURIComponent(currentPath)}`);
	}
};
