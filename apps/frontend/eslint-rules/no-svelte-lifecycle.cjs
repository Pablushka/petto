// Disallow importing Svelte lifecycle helpers (onMount, beforeUpdate, afterUpdate)
module.exports = {
	meta: {
		type: 'problem',
		docs: {
			description: 'Disallow Svelte lifecycle imports in favor of Svelte 5 runes ($state/$effect)',
			recommended: true
		}
	},
	create(context) {
		return {
			ImportDeclaration(node) {
				if (!node.source || !node.source.value) return;
				if (node.source.value === 'svelte') {
					// ban lifecycle helpers and deprecated runtime helpers that have rune-based alternatives. Allow onDestroy which still has valid use-cases.
					const banned = ['onMount', 'beforeUpdate', 'afterUpdate', 'createEventDispatcher'];
					for (const spec of node.specifiers || []) {
						if (spec.imported && banned.includes(spec.imported.name)) {
							context.report({
								node: spec,
								message: `Import of ${spec.imported.name} is disallowed; use Svelte 5 runes instead`
							});
						}
					}
				}
			}
		};
	}
};
