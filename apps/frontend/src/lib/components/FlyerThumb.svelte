<script lang="ts">
	import { browser } from '$app/environment';
	import wall from '$lib/assets/wall.jpg';
	import { BACKEND_URL } from '$lib/config';

	let { flyerHtml = '', petId }: { flyerHtml?: string; petId?: number } = $props();

	const mounted = $derived(browser);

	function sanitizeHtml(html: string) {
		if (!html) return '';
		if (typeof window === 'undefined') return '';
		const parser = new DOMParser();
		const doc = parser.parseFromString(html, 'text/html');

		// remove dangerous elements
		['script', 'iframe', 'object', 'embed', 'link', 'form', 'meta'].forEach((tag) => {
			doc.querySelectorAll(tag).forEach((n) => n.remove());
		});

		// remove event handlers and javascript: href/src
		doc.querySelectorAll('*').forEach((el) => {
			[...el.attributes].forEach((attr) => {
				const name = attr.name;
				const value = attr.value || '';
				if (/^on/i.test(name)) el.removeAttribute(name);
				if (/(href|src|xlink:href|formaction)/i.test(name) && /^\s*javascript:/i.test(value))
					el.removeAttribute(name);
				if (
					/(href|src)/i.test(name) &&
					/^\s*data:/i.test(value) &&
					/^\s*data:(text|application)\/html/i.test(value)
				)
					el.removeAttribute(name);
			});
		});

		// Return full document HTML for iframe srcdoc
		return '<!doctype html>\n' + doc.documentElement.outerHTML;
	}

	const sanitizedDoc = $derived(browser ? sanitizeHtml(flyerHtml) : '');
	const printUrl = $derived(petId ? `${BACKEND_URL}api/flyers/${petId}` : '');
</script>

<div
	class="flyer-preview-wrapper"
	style={`--wall-url: url(${wall}); --preview_scale: 0.26; --wrapper_scale: 0.3;`}
>
	{#if printUrl}
		<button
			type="button"
			class="flyer-print-button"
			onclick={() => window.open(printUrl, '_blank')}
			aria-label="Print flyer"
		>
			🖨️
		</button>
	{/if}
    <div class="flyer-preview">
        {#if mounted}
            <iframe title="Flyer Preview" srcdoc={sanitizedDoc} class="h-[29.7cm] w-[21cm]"></iframe>
        {:else}
            <div class="h-[29.7cm] w-[21cm] bg-gray-100"></div>
        {/if}
    </div>
</div>

<style>
	.flyer-preview-wrapper {
		position: relative;
		background: #f3f4f6;
		background-image: var(--wall-url);
        background-size: cover;
        background-position: center;
		background-repeat: no-repeat;
		border-radius: 10px;
		/* width: calc(210mm * var(--wrapper_scale)); */
		height: calc(297mm * var(--wrapper_scale));
		overflow: hidden;
	}

	.flyer-print-button {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		height: 2rem;
		width: 2rem;
		border-radius: 999px;
		border: 0;
		background: rgba(255, 255, 255, 0.9);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-size: 0.9rem;
		opacity: 0;
		transition: opacity 160ms ease;
		cursor: pointer;
		z-index: 2;
	}

	.flyer-preview-wrapper:hover .flyer-print-button {
		opacity: 1;
	}

    /* Always show print button on touch devices */
	@media (hover: none), (pointer: coarse) {
		.flyer-print-button {
			opacity: 1;
		}
	}

	/* Flyer preview container - simulates A4 paper */
	.flyer-preview {
		width: 210mm; /* A4 width */
		height: 297mm;
		top: 0;
		left: 0;
		overflow: hidden;
		border-radius: 4px;
		box-shadow:
			0 10px 25px -5px rgba(0, 0, 0, 0.2),
			0 8px 10px -6px rgba(0, 0, 0, 0.15);
		background: white;
		transform: scale(var(--preview_scale));
		transform-origin: top;
        justify-self: center;
        margin-top: 1.5rem;
	}
</style>

