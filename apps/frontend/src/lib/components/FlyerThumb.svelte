<script lang="ts">
	import { browser } from '$app/environment';
	import wall from '$lib/assets/wall.jpg';

	let { flyerHtml = '' }: { flyerHtml?: string } = $props();

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
</script>

<div
	class="flyer-preview-wrapper"
	style={`--wall-url: url(${wall}); --scale: 0.3;`}
>
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
		display: flex;
		justify-content: center;
		align-items: flex-start;
		background: #f3f4f6;
		background-image: var(--wall-url);
        background-size: cover;
        background-position: center;
		background-repeat: no-repeat;
		border-radius: 20px;
		width: calc(210mm * var(--scale));
		height: calc(297mm * var(--scale));
		overflow: hidden;
	}

	/* Flyer preview container - simulates A4 paper */
	.flyer-preview {
		width: 210mm; /* A4 width */
		height: 297mm;
		position: relative;
		overflow: hidden;
		border-radius: 4px;
		box-shadow:
			0 10px 25px -5px rgba(0, 0, 0, 0.2),
			0 8px 10px -6px rgba(0, 0, 0, 0.15);
		background: white;
		transform: scale(var(--scale));
		transform-origin: top left;
	}
</style>

