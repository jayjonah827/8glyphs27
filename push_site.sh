#!/bin/bash
# HEYER LIVIN — Push Site to GitHub Pages
# Run this in Terminal: bash ~/Desktop/push_site.sh

REPO="$HOME/Desktop/Heyer Livin LLC - Cultural Intelligence Architecture _ Living Higher_files/visual layer for storefront and website /02_WEBSITE/ACTIVE/heyer-livin-fresh-clean/heyerlivin-site2"

cd "$REPO" || { echo "ERROR: Repo not found"; exit 1; }

# Remove stale lock file
rm -f .git/index.lock
echo "Lock file removed."

# Stage new site files
git add index.html css/style.css pages/research.html pages/story.html pages/dictionary.html pages/portal.html CNAME
echo "Files staged."

# Commit
git commit -m "Complete site rebuild — Jonah Study Research Portal

Permanent Marker for equations, Brush Script for subheaders, Helvetica for body.
5 pages: index, research, story, dictionary, portal (Notion embed). Dark/gold theme, responsive."

echo "Committed."

# Push
git push origin main
echo ""
echo "=== DONE ==="
echo "Site will be live at https://heyerlivin.com in 1-2 minutes."
echo "Direct link: https://jayjonah827.github.io"
