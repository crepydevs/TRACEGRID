# SIH26151 — How to Start, Stop, and Debug the App

This is the day-to-day operations guide for running the project.

Everything below assumes you are in the **project root** (`sih26151-darkweb-intel/`) unless stated otherwise. Run `pwd` first if you're ever unsure where you are.

---

## 1. First-Time Setup (only needed once per machine)

```bash
cd sih26151-darkweb-intel
cp .env.example .env
```

If `.env.example` doesn't exist, create it:

```bash
cat > .env.example << 'EOF'
DATABASE_URL=postgresql://sih_user:sih_pass@postgres:5432/darkweb_intel
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sih_neo4j_pass
REDIS_URL=redis://redis:6379/0
TOR_SOCKS_PROXY=socks5h://tor:9050
EOF
cp .env.example .env
```

Confirm Docker is installed and running:

```bash
docker --version
docker-compose --version
docker ps
```

If `docker ps` errors out with a permission or connection issue, Docker itself isn't running or your user isn't in the `docker` group — fix that before continuing (see Section 6).

---

## 2. Starting the App

### First time, or after changing any Dockerfile / requirements.txt / package.json

```bash
docker-compose up --build
```

`--build` forces Docker to rebuild the images from scratch. Needed whenever:
- You edit `backend/Dockerfile` or `frontend/Dockerfile`
- You add/change a package in `backend/requirements.txt`
- You add/change a package in `frontend/package.json`

### Every other time (faster, reuses existing images)

```bash
docker-compose up
```

### Running in the background (detached mode)

If you don't want the containers tying up your terminal:

```bash
docker-compose up -d
```

Use this once you've confirmed everything works — for active debugging, running in the foreground (without `-d`) is easier since you see logs live.

---

## 3. Confirming It's Actually Working

Watch the terminal output (or run `docker-compose logs -f` if detached) for these five lines. All five must appear:

```
postgres_1       | database system is ready to accept connections
neo4j_1          | Started.
redis_1          | Ready to accept connections
backend_1        | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1       | VITE ready in ... ms
```

Then open these in a browser:

| Service | URL | Notes |
|---|---|---|
| Frontend | http://localhost:5173 | Your React dashboard |
| Backend API docs | http://localhost:8000/docs | Auto-generated FastAPI docs, test endpoints here directly |
| Backend health check | http://localhost:8000/health | Should return `{"status": "ok"}` |
| Neo4j browser | http://localhost:7474 | Login: `neo4j` / `sih_neo4j_pass` |

If all four load, your whole stack is running correctly.

---

## 4. Stopping the App

### Stop but keep containers (quick pause)

If running in the foreground: press `Ctrl+C` in the terminal.

### Stop and remove containers (clean stop)

```bash
docker-compose down
```

This stops and removes the containers, but **keeps your database data** (Postgres/Neo4j volumes persist).

### Stop and wipe everything, including database data

Only do this if you genuinely want to reset all stored data back to empty:

```bash
docker-compose down -v
```

The `-v` flag deletes the volumes (`pgdata`, `neo4jdata`). Use this if your database gets into a broken/weird state and you want a clean slate — but you will lose all actors, identifiers, and scan results currently stored.

---

## 5. Checking Logs

### See logs from everything, live

```bash
docker-compose logs -f
```

`-f` means "follow" — it keeps streaming new logs as they happen. `Ctrl+C` to stop watching (this does not stop the containers).

### See logs from one specific service

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery_worker
docker-compose logs -f postgres
docker-compose logs -f neo4j
docker-compose logs -f redis
```

### See only the last N lines instead of the full history

```bash
docker-compose logs --tail=50 backend
```

### Check which containers are running vs. crashed

```bash
docker-compose ps
```

Look at the `STATUS` column. `Up` means running fine. `Exited (1)` or similar means it crashed — check that service's logs next.

---

## 6. Common Problems and Fixes

### "Cannot connect to the Docker daemon"

Docker itself isn't running.

```bash
sudo systemctl start docker
```

If you get a permission error even after that:

```bash
sudo usermod -aG docker $USER
```

Then **log out and back in** (group changes don't apply to your current session).

### A container shows `Exited` in `docker-compose ps`

```bash
docker-compose logs <service-name>
```

Read the last 20-30 lines — the actual error is almost always near the bottom. Paste it into chat with Claude the same way you've been doing; the fix is usually one specific line (a missing file, wrong path, or version conflict).

### Backend crashes immediately on start

Usually a missing file. Check that all of these exist:

```bash
ls backend/app/
```

You need: `__init__.py`, `main.py`, `config.py`, `database.py`, `celery_app.py`, plus the `models/`, `schemas/`, `api/`, `services/`, `ingestion/`, `graph/` folders.

### "Port already in use" error

Something else on your machine is already using port 8000, 5173, 5432, 7474, 7687, or 6379.

Find and stop whatever's using it:

```bash
sudo lsof -i :8000
```

This lists the process using that port. Either stop that process, or if it's a leftover Docker container from a previous run:

```bash
docker-compose down
docker ps -a
```

Check for old containers still hanging around and remove them:

```bash
docker rm -f <container-id>
```

### Changes to backend code aren't showing up

The backend Dockerfile runs uvicorn with `--reload`, and `docker-compose.yml` mounts your local `backend/` folder into the container (`volumes: - ./backend:/app`), so code changes should reflect automatically without restarting. If they don't:

```bash
docker-compose restart backend
```

### Changes to frontend code aren't showing up

Same idea — Vite's dev server should hot-reload automatically. If it doesn't:

```bash
docker-compose restart frontend
```

### You changed `requirements.txt` or `package.json` but it's not picking up the new packages

You need a full rebuild, not just a restart:

```bash
docker-compose up --build backend
```
or
```bash
docker-compose up --build frontend
```

(You can rebuild just one service instead of everything by naming it.)

### Everything is broken and you want to start completely clean

```bash
docker-compose down -v
docker-compose up --build
```

This wipes containers, volumes, and rebuilds from scratch. Last resort, but reliable.

---

## 7. Useful One-Off Commands

### Run a command inside the running backend container

Useful for things like running Alembic migrations or a Python shell inside the container's environment:

```bash
docker-compose exec backend bash
```

This drops you into a shell inside the backend container. From there you can run things like:

```bash
alembic upgrade head
python -m app.ingestion.synthetic_generator
pytest tests/ -v
```

Type `exit` to leave the container shell.

### Run Alembic migrations without entering the container manually

```bash
docker-compose exec backend alembic upgrade head
```

### Open a Postgres shell directly

```bash
docker-compose exec postgres psql -U sih_user -d darkweb_intel
```

Useful commands once inside:
```sql
\dt              -- list tables
SELECT * FROM actors LIMIT 10;
\q               -- quit
```

---

## 8. Quick Reference  

| Task | Command |
|---|---|
| Start (first time / after changes) | `docker-compose up --build` |
| Start (normal) | `docker-compose up` |
| Start in background | `docker-compose up -d` |
| Stop | `Ctrl+C` or `docker-compose down` |
| Stop + wipe all data | `docker-compose down -v` |
| See all logs, live | `docker-compose logs -f` |
| See one service's logs | `docker-compose logs -f backend` |
| Check container status | `docker-compose ps` |
| Restart one service | `docker-compose restart backend` |
| Rebuild one service | `docker-compose up --build backend` |
| Shell into backend container | `docker-compose exec backend bash` |
| Run migrations | `docker-compose exec backend alembic upgrade head` |
| Open Postgres shell | `docker-compose exec postgres psql -U sih_user -d darkweb_intel` |

---

## 9. Before You Push Code — Checklist

- [ ] `docker-compose up --build` runs clean, no errors, all five "ready" log lines appear
- [ ] Frontend loads at `http://localhost:5173`
- [ ] Backend docs load at `http://localhost:8000/docs`
- [ ] `git status` doesn't show `.venv`, `node_modules`, or `.env` as untracked (means `.gitignore` is working)
- [ ] Commit with a clear message describing what changed
- [ ] `git push origin main (not main your current developnment branch teams) --nitin :->`
 