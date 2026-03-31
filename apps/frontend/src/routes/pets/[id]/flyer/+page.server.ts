import { error } from '@sveltejs/kit';
import { get, isUnauthorized } from '$lib/utils/api';
import type { PetOut } from '$lib/types/api/pet';
import { BACKEND_URL } from '$lib/config';
import {
	getAuthTokenFromCookies,
	getRefreshTokenFromCookies,
	setAuthCookies,
	clearAuthCookies
} from '$lib/utils/auth';

type FlyerTemplatePreview = {
	name: string;
	html: string;
};

function rewriteFlyerStaticUrls(html: string): string {
	if (!html) return html;
	const backendStaticBase = `${BACKEND_URL}static/flyers_templates/`;
	// Rewrite only root-relative flyer asset paths; keep absolute URLs unchanged.
	return html.replace(
		/(^|[\s"'(=])\/(?:static\/)?flyers_templates\//g,
		(_match, prefix: string) => `${prefix}${backendStaticBase}`
	);
}

// allow any here because generated PageServerLoad type may not be available in some dev setups
/* eslint-disable @typescript-eslint/no-explicit-any */
export const load = async (event: any) => {
	/* eslint-enable @typescript-eslint/no-explicit-any */
	try {
		const { params, cookies, fetch } = event;
		const authToken = getAuthTokenFromCookies(cookies);
		const refreshToken = getRefreshTokenFromCookies(cookies);
		const pet = await get<PetOut>(`api/pets/${params.id}`, {
			requireAuth: true,
			fetchFn: fetch,
			authToken,
			refreshToken,
			onTokens: (tokens) => {
				if (!tokens) {
					clearAuthCookies(cookies);
				} else {
					setAuthCookies(cookies, tokens);
				}
			}
		});

		const templateListResponse = await fetch(`${BACKEND_URL}api/flyers/templates`, {
			headers: {
				Cookie: `access_token=${authToken}`
			}
		});

		if (!templateListResponse.ok) {
			throw error(templateListResponse.status, 'Error loading flyer templates');
		}

		const templateList = (await templateListResponse.json()) as { templates?: string[] };
		const templateNames = (templateList.templates ?? []).sort();

		const flyerTemplates = await Promise.all(
			templateNames.map(async (templateName): Promise<FlyerTemplatePreview> => {
				const flyerResponse = await fetch(
					`${BACKEND_URL}api/flyers/${params.id}?template=${encodeURIComponent(templateName)}`,
					{
						headers: {
							Cookie: `access_token=${authToken}`
						}
					}
				);

				if (!flyerResponse.ok) {
					console.error(
						`Failed to fetch flyer HTML for template "${templateName}":`,
						flyerResponse.status
					);
					return { name: templateName, html: '' };
				}

				return {
					name: templateName,
					html: rewriteFlyerStaticUrls(await flyerResponse.text())
				};
			})
		);

		// For now, we'll create a mock owner object since the API doesn't return full owner details
		// In a real implementation, you'd need an endpoint to get owner details or modify the pet endpoint
		const owner = {
			first_name: 'Juan',
			last_name: 'Pérez',
			phone: '+1234567890',
			email: 'juan@example.com',
			full_address: 'Calle Principal 123, Ciudad, País',
			recovery_bounty: 50.0
		};

		return {
			pet,
			owner,
			flyerTemplates
		};
	} catch (err) {
		if (isUnauthorized(err)) {
			throw error(401, 'Unauthorized');
		}
		console.error('Error in flyer page load:', err);
		throw error(500, 'Error loading pet data');
	}
};
