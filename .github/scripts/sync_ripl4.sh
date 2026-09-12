#!/usr/bin/env bash
# Mirror the riplpy source tree into a checkout of IAEA-NDS/RIPL-4 under
# RIPLpy/, so the vendored copy there tracks this repository's main branch.
#
#   sync_ripl4.sh <riplpy-source-dir> <ripl4-checkout-dir>
#
# Uses rsync --delete against a staged payload, so files removed upstream in
# riplpy (setup.py and requirements.txt, dropped in the 0.6.1 packaging
# migration) are actually deleted from the vendored copy rather than left
# behind. A plain copy would silently keep shipping the broken setup.py.
#
# Exits 0 with no changes staged if the copy is already current.

set -euo pipefail

SRC="${1:?usage: sync_ripl4.sh <riplpy-source-dir> <ripl4-checkout-dir>}"
DEST_REPO="${2:?usage: sync_ripl4.sh <riplpy-source-dir> <ripl4-checkout-dir>}"
DEST="$DEST_REPO/RIPLpy"

# Exactly what the vendored copy should contain. Anything in RIPLpy/ not
# produced from this list is removed by the --delete below.
PATHS=(
  riplpy
  tests
  tools
  README.md
  LICENSE.txt
  CATALOG.md
  SCHEMA.json
  pyproject.toml
  pytest.ini
  MANIFEST.in
)

stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

for p in "${PATHS[@]}"; do
  if [ -e "$SRC/$p" ]; then
    cp -R "$SRC/$p" "$stage/"
  else
    echo "warning: '$p' not found in source tree, skipping" >&2
  fi
done

# Never vendor build output, caches, OS cruft, or our own CI config.
find "$stage" \( -name '__pycache__' -o -name '*.egg-info' \) -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$stage" \( -name '*.py[cod]' -o -name '.DS_Store' \) -type f -delete 2>/dev/null || true

mkdir -p "$DEST"
rsync -a --delete "$stage"/ "$DEST"/

echo "Synced into $DEST:"
( cd "$DEST" && ls -A )
