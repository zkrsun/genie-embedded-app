# Genie Embedded App

A FastAPI + Vue 3 web application that embeds multiple Databricks Genie spaces into a single interface with tab-based navigation.

## Features

- Embed multiple Genie spaces (RMS, SELLIN, SELLOUT) in one page
- Tab navigation to switch between spaces
- Light-themed UI built with Vue 3 + Vite
- Deployable to Databricks Apps

## Project Structure

```
├── app.yaml              # Databricks Apps configuration
├── package.json          # Root-level build proxy for Databricks Apps
├── requirements.txt      # Python dependencies
├── backend/
│   └── app.py            # FastAPI: /api/spaces + static file serving
└── frontend/
    ├── package.json      # Vue + Vite dependencies
    ├── vite.config.js    # Dev proxy: /api → localhost:8000
    ├── index.html
    └── src/
        ├── main.js
        └── App.vue       # Navbar tabs + Genie iframe
```

## Prerequisites

- Python 3.11+
- Node.js 18+

## Local Development

### 1. Install dependencies

```bash
# Python
pip install -r requirements.txt

# Node
cd frontend && npm install && cd ..
```

### 2. Configure app.yaml

Add `DATABRICKS_TOKEN` for local authentication:

```yaml
env:
  - name: 'DATABRICKS_TOKEN'
    value: 'your-databricks-pat-token'
```

> The token is only needed locally. On Databricks Apps, credentials are injected automatically.

### 3. Start the servers

```bash
# Terminal 1 — Backend (from project root)
uvicorn app:app --app-dir backend --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
# → http://localhost:5173
```

The Vite dev server proxies `/api/*` requests to FastAPI on port 8000.

## Deployment to Databricks Apps

### 1. Fill in Genie Space IDs in app.yaml

```yaml
env:
  - name: 'GENIE_SPACE_RMS'
    value: 'your-rms-space-id'
  - name: 'GENIE_SPACE_SELLIN'
    value: 'your-sellin-space-id'
  - name: 'GENIE_SPACE_SELLOUT'
    value: 'your-sellout-space-id'
```

Find Space IDs in Databricks: Genie Space → Share → Embed space → copy the ID from the iframe src.

### 2. Sync and deploy via CLI

```bash
databricks sync . /Workspace/Users/your-email@org.com/genie-app

databricks apps deploy your-app-name \
  --source-code-path /Workspace/Users/your-email@org.com/genie-app
```

### Deploy from Git

1. Push this repository to GitHub
2. In Databricks UI: Compute → Apps → your app → Deploy → From Git
3. Enter repository URL and branch

### Databricks Apps build process

When `package.json` is detected at the root, Databricks Apps automatically runs:

```
npm install
pip install -r requirements.txt
npm run build        ← builds Vue → frontend/dist/
uvicorn app:app --app-dir backend
```

## Configuration Reference

| Variable | Description |
|---|---|
| `MODE` | `LOCAL` reads from `app.yaml`; `DBX` reads from env vars (set automatically) |
| `DATABRICKS_HOST` | Workspace URL, e.g. `https://adb-xxx.azuredatabricks.net` |
| `WORKSPACE_ID` | Numeric workspace ID |
| `GENIE_SPACE_RMS` | Genie Space ID for RMS |
| `GENIE_SPACE_SELLIN` | Genie Space ID for SELLIN |
| `GENIE_SPACE_SELLOUT` | Genie Space ID for SELLOUT |
| `DATABRICKS_TOKEN` | PAT for local dev only — do not commit |
