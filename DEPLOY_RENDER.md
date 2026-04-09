# Deploy on Render (why it failed + fix)

## Root cause

Render builds from **GitHub**, not from your laptop. These files must exist **on the branch Render deploys** (usually `main`):

- `GLYPH8/server.py`
- `GLYPH8/requirements.txt`

Right now they are **not** on `main` in `jayjonah827/8glyphs27`, so the service has nothing to run (`uvicorn server:app` fails).

## Fix (pick one)

### A. Push from a local clone

```bash
cd /path/to/8glyphs27   # your clone of jayjonah827/8glyphs27
git pull origin main

# Copy these three files from your machine (same paths as this repo):
#   GLYPH8/server.py
#   GLYPH8/requirements.txt
#   render.yaml   (optional, for Blueprint)

git add GLYPH8/server.py GLYPH8/requirements.txt render.yaml
git commit -m "Add FastAPI server and requirements for Render"
git push origin main
```

Then in Render: **Manual Deploy → Clear build cache & deploy** (or wait for auto-deploy).

### B. Add files in GitHub UI

1. Open repo → `GLYPH8/` → **Add file** → paste contents of `server.py` and `requirements.txt` from this folder.
2. Commit to `main`.

### Render dashboard settings (Web Service)

| Setting | Value |
|--------|--------|
| Root Directory | `GLYPH8` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn server:app --host 0.0.0.0 --port $PORT` |

Health check path: `/health` (optional in dashboard).

## Verify after deploy

- `https://YOUR-SERVICE.onrender.com/health` → `{"status":"ok"}`

## Note: GitHub Pages vs Render

This repo also uses **GitHub Pages** (static files under `GLYPH8/`). That is separate from **Render** (Python web process). You can keep both: Pages for static preview, Render for the live app.
