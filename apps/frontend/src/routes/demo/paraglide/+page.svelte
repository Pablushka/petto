<script lang="ts">
	import { setLocale } from '$lib/paraglide/runtime';
	import { m } from '$lib/paraglide/messages';
</script>

<h1>{m.hello_world({ name: 'SvelteKit User' })}</h1>
<h1>{m.button_submit()}</h1>
<h1>{m.button_cancel()}</h1>

<div>
	<button class="btn" onclick={() => setLocale('en')}>en</button>
	<button class="btn" onclick={() => setLocale('es')}>es</button>
	<button class="btn" onclick={() => setLocale('jp')}>jp</button>
</div>
<p>
	If you use VSCode, install the <a
		href="https://marketplace.visualstudio.com/items?itemName=inlang.vs-code-extension"
		target="_blank">Sherlock i18n extension</a
	> for a better i18n experience.
</p>
