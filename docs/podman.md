# Running the stack with Podman (the default)

Podman is the project's default container engine: the README and CLAUDE.md give
Podman commands. Docker runs the same [docker-compose.yml](../docker-compose.yml)
and the same `make` targets ([docker.md](docker.md)). Podman runs rootless and needs no daemon, which is often
what a locked-down workstation or a RHEL server allows.

## What differs from Docker

| | Docker | Podman |
|---|---|---|
| Compose tool | `docker compose` | `podman-compose` |
| GPU worker | service `worker`, profile `gpu` (device reservation) | service `worker-cdi`, profile `gpu-cdi` (CDI device `nvidia.com/gpu=all`) |
| Worker container | `nomergon-worker` | `nomergon-worker-cdi` |
| CPU worker | `worker-cpu`, profile `cpu` | the same |
| Restart after reboot | the Docker daemon | `podman-restart.service` (see below) |

The compose file already carries what Podman needs and Docker ignores: fully
qualified image names (`docker.io/pgvector/pgvector:pg17`, so no short-name prompt),
`z` on the bind mounts (SELinux relabel on Fedora/RHEL) and `label=disable` on the
GPU worker.

Podman keeps its own images, containers and volumes: a database created under
Docker is **not** visible to Podman. To move one, back it up under Docker and
restore it under Podman (README, *Backup and restore*).

## Install

Podman ≥ 4.9 (5.x recommended) and podman-compose ≥ 1.1 (it must support
`depends_on: condition: service_healthy`, `env_file: required` and CDI devices).

```sh
# Ubuntu / Debian
sudo apt install podman podman-compose
# Fedora / RHEL
sudo dnf install podman podman-compose
```

`podman compose` (with a space) is a wrapper that may run `docker-compose` if one
is installed; the Makefile calls `podman-compose` directly. If you use the wrapper,
set `PODMAN_COMPOSE_PROVIDER=podman-compose`.

### GPU (NVIDIA)

Podman reaches the GPU through CDI. Install the NVIDIA Container Toolkit (≥ 1.14),
then generate the host's CDI spec (recent toolkits keep `/var/run/cdi/nvidia.yaml`
current on their own through `nvidia-cdi-refresh`; regenerate after a driver update
otherwise):

```sh
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
nvidia-ctk cdi list                       # should list nvidia.com/gpu=all
podman run --rm --device nvidia.com/gpu=all --security-opt=label=disable \
  docker.io/library/ubuntu nvidia-smi -L  # should print the GPU
```

No `nvidia-container-runtime` configuration is needed for Podman. Without an
NVIDIA GPU, use the CPU worker (`make up-cpu`).

## Run

The Makefile picks Podman when it is installed, else Docker; force one with
`ENGINE=podman` / `ENGINE=docker` (`make help` shows the engine in use).

```sh
cp .env.example .env          # the worker's keys, as with Docker
make up-gpu                   # = podman-compose --profile gpu-cdi up -d --build
make up-cpu                   # = podman-compose --profile cpu up -d --build
make init-db                  # once: params and eval schemas
make update COUNTRY=FR YEAR=2025
make status / make jobs / make logs / make down
```

Do not run the two stacks at
once: they publish the same ports (5434, 5050, 6006, 4317).

The desktop apps (`make ui`, `make rag-ui`), pgAdmin (http://localhost:5050) and
Phoenix (http://localhost:6006) work unchanged: they only talk to
`localhost:5434` and `localhost:6006`.

## Docker commands, translated

| Docker (older notes, [docker.md](docker.md)) | Podman |
|---|---|
| `docker compose --profile gpu up -d` | `podman-compose --profile gpu-cdi up -d` |
| `docker compose exec worker nomergon …` | `podman exec nomergon-worker-cdi /app/.venv/bin/nomergon …` (or `make` targets) |
| `docker compose --profile gpu up -d --no-deps worker` (after editing `.env`) | `podman-compose --profile gpu-cdi up -d --no-deps --force-recreate worker-cdi` |
| `docker exec -i nomotheca-legislation-db psql -U jrc -d legislation` | `podman exec -i nomotheca-legislation-db psql -U jrc -d legislation` |
| `docker compose logs -f worker` | `podman logs -f nomergon-worker-cdi` |
| `docker volume ls \| grep pgdata` | `podman volume ls \| grep pgdata` (same `euromod_pgdata` name) |
| `docker compose down -v` | `podman-compose down -v` — same warning: it deletes the database |

As with Docker, recreate only the worker after editing `.env` (`--no-deps`): a plain
`up -d` of the worker may restart Postgres and kill a running job.

## Restart after a reboot

Rootless Podman has no daemon to bring containers back. Containers with
`restart: unless-stopped` (all of ours) are restarted at login by:

```sh
systemctl --user enable --now podman-restart.service
loginctl enable-linger "$USER"     # start them at boot, before you log in
```

## Restore backup

```sh
podman exec -i nomotheca-legislation-db pg_restore -U jrc -d legislation --clean --if-exists < ../backups/legislation_$(date +%Y%m%d).dump
podman stop nomoscope-phoenix
podman exec -i nomotheca-legislation-db psql -U jrc -d postgres -c "DROP DATABASE IF EXISTS phoenix;"
podman exec -i nomotheca-legislation-db psql -U jrc -d postgres -c "CREATE DATABASE phoenix OWNER jrc;"
podman exec -i nomotheca-legislation-db pg_restore -U jrc -d phoenix < ../backups/phoenix_$(date +%Y%m%d).dump
podman start nomoscope-phoenix
```

## Troubleshooting

- **`unresolvable CDI devices nvidia.com/gpu=all`** — no CDI spec: run the
  `nvidia-ctk cdi generate` above (and again after an NVIDIA driver upgrade).
- **`short-name … did not resolve to an alias`** — an image added without its
  registry; write it as `docker.io/<org>/<image>:<tag>`.
- **`Permission denied` on `/docker-entrypoint-initdb.d/*.sql`** (SELinux) — a bind
  mount without `z`; every bind mount in the compose file needs `:ro,z`.
- **The worker starts before Postgres is ready** — podman-compose older than 1.1
  ignores `condition: service_healthy`; upgrade it.
- **`podman ps` shows nothing after a reboot** — see *Restart after a reboot*.
- **Rootless and ports** — rootless Podman cannot publish ports below 1024; ours are
  all above, so nothing to do.
- **Phoenix answers `401 Unauthorized` to `POST /v1/traces`** — a fresh pull of
  `phoenix:latest` (v21+) enables auth by default on a non-loopback bind, and
  the image binds `::`; the compose file sets `PHOENIX_ENABLE_AUTH: "false"`.
  An older container lacks it: recreate Phoenix alone
  (`podman stop nomoscope-phoenix && podman rm nomoscope-phoenix && podman-compose up -d --no-deps phoenix`).
  Its banner must read `Authentication ➖ Disabled` (`podman logs nomoscope-phoenix`).
