# Image Processing Lab — Vercel Ready

## What was fixed
- Frontend files are at the repository root, so Vercel does not look in the wrong folder and return `404 NOT_FOUND`.
- Added `vercel.json` for a clean static deployment.
- Removed the hard-coded `localhost:8080` dependency from the frontend.
- The image-processing experiments remain fully browser-side and work from the public Vercel URL.
- Backend logging is optional. If the backend is not deployed, the visual lab still works.
- Backend CORS can now be configured with `CORS_ORIGIN`.
- Database schema no longer tries to create a database while connected to one.

## IMPORTANT: Vercel + Spring Boot
Vercel is being used here for the **frontend/static website**. The Java Spring Boot + PostgreSQL backend should be hosted separately (for example on Render, Railway, or another Java host).

### Fastest way to get your public link
1. Push this folder to GitHub.
2. In Vercel, click **Add New → Project**.
3. Import the GitHub repository.
4. Framework Preset: **Other** (or let Vercel detect it as static).
5. Root Directory: **`.`**.
6. Build Command: leave empty.
7. Output Directory: leave empty.
8. Click **Deploy**.
9. Open the generated `https://....vercel.app` URL.

There is no `npm install`, no Node build, and no frontend environment variable required.

## If you also want backend history/database
Deploy `backend/` separately to a Java-capable service and PostgreSQL separately.
Then edit the first line in `api.js`:

`window.API_BASE = "https://YOUR-BACKEND-DOMAIN/api";`

Also set the backend environment variable:

`CORS_ORIGIN=https://YOUR-PROJECT.vercel.app`

For the database, set:
- `SPRING_DATASOURCE_URL=jdbc:postgresql://HOST:PORT/DATABASE`
- `DB_USERNAME=...`
- `DB_PASSWORD=...`

The backend already listens on `${PORT:8080}` for hosts that provide a PORT variable.

## Local full-stack run
From this folder:
- Frontend: open `index.html` with VS Code Live Server.
- Backend: `cd backend` then `mvn spring-boot:run`.
- Database: PostgreSQL database `image_processing_lab`.

## Vercel 404 troubleshooting
If Vercel still shows `404 NOT_FOUND`, the usual cause is the wrong Root Directory. It must point to the folder containing:
- `index.html`
- `style.css`
- `app.js`
- `api.js`
- `vercel.json`

In this package, that is the repository root (`.`).
