import type { Handle } from '@sveltejs/kit';
import { paraglideMiddleware } from '$lib/paraglide/server';

const ALLOWED_RESPONSE_HEADERS = new Set([
	'content-type',
	'content-length',
	'cache-control',
	'content-language',
	'expires',
	'last-modified',
	'pragma',
	'vary',
	'x-total-count',
	'link'
]);

const handleParaglide: Handle = ({ event, resolve }) =>
	paraglideMiddleware(event.request, ({ request, locale }) => {
		event.request = request;

		return resolve(event, {
			filterSerializedResponseHeaders: (name) => ALLOWED_RESPONSE_HEADERS.has(name.toLowerCase()),
			transformPageChunk: ({ html }) => html.replace('%paraglide.lang%', locale)
		});
	});

export const handle: Handle = handleParaglide;
