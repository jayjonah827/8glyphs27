# HEYER LIVIN' — FULL SYNC DEPLOYMENT RUNBOOK
**Date: 2026-03-26**
**Target: heyerlivin.com (Fourthwall) + 8glyphs27.heyerlivin.com (GitHub Pages) + Notion**

---

## PLATFORM 1: GITHUB — Push to jayjonah827/8glyphs27

Open terminal. Navigate to your local clone of the repo, or clone fresh:

```bash
git clone https://github.com/jayjonah827/8glyphs27.git
cd 8glyphs27
```

Copy these files from the `deploy-package/` folder into the repo root:

```
8glyphs27/
├── .github/
│   └── FUNDING.yml          ← sponsorship links (Ko-fi, BuyMeACoffee, Fiverr, Etsy, LinkedIn)
├── assets/
│   ├── art/                  ← 26 artwork PNGs
│   └── brand/
│       └── heyer_livin_thumbnail.png
├── data/
│   ├── events.json           ← convergence band event records
│   └── messages.json         ← daily messages
├── fourthwall-blocks/
│   ├── 01-home-brand.html
│   ├── 02-equation.html
│   ├── 03-data-convergence.html
│   ├── 04-portfolio.html
│   ├── 05-blog.html
│   ├── DEPLOY.md
│   ├── heyerlivin.code-workspace
│   └── workers/
│       └── notion-proxy.js
├── CNAME                     ← NOW READS: 8glyphs27.heyerlivin.com
└── index.html                ← Glyph-8 research engine (28KB)
```

Then:

```bash
git add -A
git commit -m "Full sync: CNAME fix, Fourthwall blocks, portfolio update, deploy package"
git push origin main
```

GitHub Pages will auto-deploy. The CNAME file tells GitHub to serve at `8glyphs27.heyerlivin.com`.

**DNS already points the `8glyphs27` subdomain to GitHub Pages IPs (15.197.225.128 + 3.33.251.168). No DNS change needed.**

Wait 2-5 minutes for GitHub Pages to propagate. Verify: `https://8glyphs27.heyerlivin.com`

---

## PLATFORM 2: FOURTHWALL — Paste HTML Blocks

Open Fourthwall dashboard: https://fourthwall.com (login as Heyer Livin')

### Page 1: HOME
1. Dashboard → Pages → Home → Edit
2. Add Section → Custom HTML (or edit existing Custom HTML block)
3. Open `fourthwall-blocks/01-home-brand.html` in VS Code
4. Select all, copy, paste into the Custom HTML block
5. Save and publish

### Page 2: EQUATION
1. Dashboard → Pages → Create New Page → Title: "Equation" → URL slug: `equation`
2. Add Section → Custom HTML
3. Paste contents of `fourthwall-blocks/02-equation.html`
4. Save and publish

### Page 3: DATA
1. Dashboard → Pages → Create New Page → Title: "Data" → URL slug: `data`
2. Add Section → Custom HTML
3. Paste contents of `fourthwall-blocks/03-data-convergence.html`
4. Data loads from `raw.githubusercontent.com/jayjonah827/8glyphs27/main/data/events.json`
5. Save and publish

### Page 4: PORTFOLIO
1. Dashboard → Pages → Create New Page → Title: "Portfolio" → URL slug: `portfolio`
2. Add Section → Custom HTML
3. Paste contents of `fourthwall-blocks/04-portfolio.html`
4. Art loads from GitHub raw URLs. 26 verified artworks.
5. Save and publish

### Page 5: BLOG
1. Dashboard → Pages → Create New Page → Title: "Blog" → URL slug: `blog`
2. Add Section → Custom HTML
3. Paste contents of `fourthwall-blocks/05-blog.html`
4. Static fallback posts active. Notion proxy URL set to null until Cloudflare Worker deployed.
5. Save and publish

### Page 6: STOREFRONT
Already live. Products active: Coin Flip ($27), art prints ($29, $67), Baby tee ($35). No change needed.

### Navigation
Update Fourthwall nav menu to include: Home, Shop, Portfolio, Blog, Research (Data), Equation, Glyph-8 (external link to 8glyphs27.heyerlivin.com)

---

## PLATFORM 3: NOTION — Verify Structure

Notion workspace ID: `cb59e681-206a-8104-8218-000328caf4b7`

### Existing Structure (4 hubs):
- 🔬 RESEARCH — Jonah Study (17 pages)
- 🎨 CREATIVE STUDIO — Heyer Livin' (13 pages)
- 🏭 BUSINESS — Operations (7 pages)
- ⚖️ LEGAL — Documentation (2 pages)

### Portfolio Database
ID: `ba14b656-1924-418c-8b0f-89525e9ddc1e`
Contains: The Coin, GLYPHS (Magritte Composition), 1+2=3 Framework, GLYPH8 Engine, Daily Messages
Status: LIVE

### Blog Page
ID: `32b7097e-f44e-81bc-aa13-d915c9ba9f83`
Status: EXISTS — needs blog database created underneath it with these properties:
- Name (title)
- Date (date)
- Excerpt (rich text)
- Tags (multi-select)
- Published (checkbox)

### Notion Integration (for live blog/portfolio on site):
1. Go to https://www.notion.so/my-integrations
2. Create integration: "Heyer Livin Site"
3. Copy Internal Integration Token
4. Share blog database + portfolio database with the integration
5. Deploy Cloudflare Worker (see `fourthwall-blocks/workers/notion-proxy.js`)
6. Update DATABASE_IDS in the worker with actual Notion database IDs
7. Set NOTION_PROXY_URL in blog and portfolio HTML blocks

**NOTE: Site works without Notion integration. Static fallback posts and projects display. Notion integration is an upgrade, not a blocker.**

---

## VERIFICATION CHECKLIST

After all platforms are updated:

- [ ] `https://heyerlivin.com` → Fourthwall storefront, home page shows hero + 4 expressions + 1+2=3
- [ ] `https://heyerlivin.com/pages/equation` → Equation breakdown page
- [ ] `https://heyerlivin.com/pages/data` → Convergence band with live data dots
- [ ] `https://heyerlivin.com/pages/portfolio` → Art gallery (26 pieces) + current projects
- [ ] `https://heyerlivin.com/pages/blog` → Blog with 4 fallback posts
- [ ] `https://heyerlivin.com/pages/storefront` → Products, checkout, donations
- [ ] `https://8glyphs27.heyerlivin.com` → Glyph-8 research engine
- [ ] GitHub Sponsor button active on jayjonah827/8glyphs27
- [ ] Notion 4 hubs intact, no root-level pages created

---

## SITE MAP (FINAL)

```
heyerlivin.com (Fourthwall)
├── /                    → 01-home-brand.html (Hero, Expressions, 1+2=3)
├── /pages/equation      → 02-equation.html (Master equation, K(t), artifact families)
├── /pages/data          → 03-data-convergence.html (Live convergence band, event table)
├── /pages/portfolio     → 04-portfolio.html (26 artworks, 6 projects)
├── /pages/blog          → 05-blog.html (Notion-powered or static fallback)
├── /pages/storefront    → Native Fourthwall (products, checkout, donations)
└── [nav link]           → 8glyphs27.heyerlivin.com (GitHub Pages)

8glyphs27.heyerlivin.com (GitHub Pages)
├── /                    → Glyph-8 research engine (index.html, 28KB)
├── /data/events.json    → Event records (loaded by Fourthwall data page)
├── /data/messages.json  → Daily messages
└── /assets/art/         → 26 artwork files (loaded by Fourthwall portfolio)
```
