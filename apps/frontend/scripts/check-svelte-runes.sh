#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
echo "Checking Svelte lifecycle imports in $ROOT_DIR/src"
# also detect createEventDispatcher import (deprecated pattern per project guidance)
# look for import { onMount | beforeUpdate | afterUpdate | createEventDispatcher } from 'svelte' (onDestroy is allowed)
PATTERN="import[[:space:]]*\\{[^}]*\\b(onMount|beforeUpdate|afterUpdate|createEventDispatcher)\\b"
if grep -E -R -n -- "$PATTERN" "$ROOT_DIR/src" >/dev/null 2>&1; then
  echo "Legacy Svelte lifecycle imports detected. Please use Svelte 5 runes instead (\$state/\$effect)."
  echo "Files found:"
  grep -E -R -n -- "$PATTERN" "$ROOT_DIR/src" || true
  exit 1
else
  echo "No banned lifecycle imports found."
fi

# Also detect Svelte reactive label usage ($:). These should be replaced with $effect/$derived in Svelte 5
REACTIVE_PATTERN='(^|[^\w\$])\$:'
if grep -E -R -n --exclude-dir=.svelte-kit -- "$REACTIVE_PATTERN" "$ROOT_DIR/src" >/dev/null 2>&1; then
  echo "Found Svelte reactive label(s) ('$:') — consider replacing with Svelte 5 runes (\$effect/\$derived)."
  echo "Files with reactive labels:"
  grep -E -R -n --exclude-dir=.svelte-kit -- "$REACTIVE_PATTERN" "$ROOT_DIR/src" || true
  exit 1
else
  echo "No reactive label ('$:') usages found."
fi
