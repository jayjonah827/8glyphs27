# Fourthwall Deployment Guide

## Architecture

```
heyerlivin.com (Fourthwall)
├── Home           → 01-home-brand.html
├── /pages/equation → 02-equation.html
├── /pages/data     → 03-data-convergence.html
├── /pages/portfolio → 04-portfolio.html
├── /pages/blog     → 05-blog.html
├── /pages/storefront → Native Fourthwall (products, checkout)
└── Link → 8glyphs27.heyerlivin.com (GitHub Pages, deep research)

8glyphs27.heyerlivin.com (GitHub Pages)
├── Glyph-8 Engine
├── Full convergence data
├── Interactive tools
└── Research archive
```

## Workflow: VS Code → Git → Fourthwall

1. Open `heyerlivin.code-workspace` in VS Code
2. Edit any block HTML file
3. Preview locally with Live Server (right-click → Open with Live Server)
4. Commit and push to Git (version control)
5. Open Fourthwall dashboard → Pages → target page → Edit
6. Paste the HTML block content into the Custom HTML section
7. Save and publish

## Fourthwall Page Setup

For each page, create it in Fourthwall dashboard:

1. **Home**: Dashboard → Pages → Home → Add Section → Custom HTML → paste `01-home-brand.html`
2. **Equation**: Dashboard → Pages → Create Page "Equation" → Custom HTML → paste `02-equation.html`
3. **Data**: Dashboard → Pages → Create Page "Data" → Custom HTML → paste `03-data-convergence.html`
4. **Portfolio**: Dashboard → Pages → Create Page "Portfolio" → Custom HTML → paste `04-portfolio.html`
5. **Blog**: Dashboard → Pages → Create Page "Blog" → Custom HTML → paste `05-blog.html`
6. **Storefront**: Already exists with products. No custom block needed.

## Notion Integration Setup

### Step 1: Create Notion Integration
- Go to https://www.notion.so/my-integrations
- Create integration named "Heyer Livin Site"
- Copy the Internal Integration Token

### Step 2: Share Databases
- Open your Blog database in Notion
- Click ••• → Connections → Add connection → "Heyer Livin Site"
- Repeat for Projects database

### Step 3: Deploy Cloudflare Worker
```bash
npm install -g wrangler
wrangler login
wrangler init notion-proxy
# Replace worker code with workers/notion-proxy.js
# Update DATABASE_IDS with your actual database IDs
wrangler secret put NOTION_TOKEN
# Paste your Notion integration token
wrangler deploy
```

### Step 4: Update Block URLs
In `05-blog.html` and `04-portfolio.html`, set:
```javascript
var NOTION_PROXY_URL = 'https://notion-proxy.YOUR-SUBDOMAIN.workers.dev/blog';
```

## DNS Verification

Current DNS (managed in Fourthwall):
- `@` → A → 34.117.223.165 (Fourthwall)
- `8glyphs27` → A → 15.197.225.128 + 3.33.251.168 (GitHub Pages)

## File Structure

```
fourthwall-blocks/
├── 01-home-brand.html        ← Home page block
├── 02-equation.html           ← Equation page block
├── 03-data-convergence.html   ← Data/K(t) page block
├── 04-portfolio.html          ← Portfolio page block
├── 05-blog.html               ← Blog page block
├── workers/
│   └── notion-proxy.js        ← Cloudflare Worker for Notion API
├── heyerlivin.code-workspace  ← VS Code workspace file
└── DEPLOY.md                  ← This file
```
