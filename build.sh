#!/usr/bin/env bash
# Pinned Hugo build for Cloudflare Pages (or any CI).
#
# Cloudflare Pages' built-in Hugo buildpack can install a very old default
# Hugo (0.54-era) which cannot parse this site's hugo.toml / modern template
# syntax. This script downloads the exact pinned version the site is
# developed against and builds with it. Wire it up in Pages as:
#   Build command:        bash build.sh
#   Build output dir:     public
set -euo pipefail
cd "$(dirname "$0")/hugo-site"

VERSION=0.147.2

if ! ./hugo version >/dev/null 2>&1; then
  echo ">> downloading pinned Hugo v${VERSION}..."
  curl -sL "https://github.com/gohugoio/hugo/releases/download/v${VERSION}/hugo_${VERSION}_linux-amd64.tar.gz" -o /tmp/hugo.tgz
  tar xzf /tmp/hugo.tgz hugo
fi

./hugo --gc
