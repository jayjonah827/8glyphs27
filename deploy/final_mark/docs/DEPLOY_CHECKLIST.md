# Deployment Checklist

## Before Any Deployment

- [ ] Confirm target domain and platform
- [ ] Verify content source is in GLYPHS/sites/{platform}/
- [ ] Run exports.yaml check — confirm all files are on the allowlist
- [ ] Confirm NO QmPYcVJCV8277 references in exported files
- [ ] Confirm NO .env or secret files in export staging

## Wix (heyerlivin.com)

- [ ] Content staged in _exports/wix/
- [ ] DNS A record updated in GoDaddy (currently parked)
- [ ] Wix site builder configured
- [ ] Verify site resolves

## Fourthwall (heyerlivin.shop)

- [ ] HTML blocks in GLYPHS/sites/fourthwall/
- [ ] Paste each block into Fourthwall dashboard
- [ ] Verify pages render
- [ ] DNS: A record 34.117.223.165 confirmed

## GitHub Pages — Site 1 (8glyphs27)

- [ ] Content staged in _exports/github_site1/
- [ ] Push to jayjonah827/8glyphs27 repo
- [ ] Verify Pages deployment
- [ ] CNAME file matches target domain

## GitHub Pages — Site 2 (glyphhrlvn4culturalnav.space)

- [ ] Content staged in _exports/github_site2/
- [ ] Push to appropriate repo
- [ ] DNS A records configured in GoDaddy
- [ ] CNAME file: glyphhrlvn4culturalnav.space
- [ ] Verify Pages deployment

## Notion (glyphhrlvn4culturalnav.store)

- [ ] Content staged in _exports/notion/
- [ ] Notion workspace configured
- [ ] Paid Notion plan active + custom domain add-on ($10/mo)
- [ ] DNS configured
- [ ] Verify site resolves
