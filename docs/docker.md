# Running the stack with Docker

The project's default engine is Podman ([podman.md](podman.md)): the README and
CLAUDE.md give Podman commands. Docker runs the same
[docker-compose.yml](../docker-compose.yml) and the same `make` targets, and is a
likely choice for a future server deployment (Docker Engine + Compose v2, the
NVIDIA Container Toolkit for the GPU worker).

## What differs from Podman

| | Podman (default) | Docker |
|---|---|---|
| Compose tool | `podman-compose` | `docker compose` |
| GPU worker | service `worker-cdi`, profile `gpu-cdi` (CDI device `nvidia.com/gpu=all`) | service `worker`, profile `gpu` (device reservation, `nvidia` runtime) |
| Worker container | `nomergon-worker-cdi` | `nomergon-worker` |
| CPU worker | `worker-cpu`, profile `cpu` | the same |
| Restart after reboot | `podman-restart.service` | the Docker daemon |

Container names other than the worker (`nomotheca-legislation-db`,
`nomoscope-phoenix`) and the volume name (`euromod_pgdata`) are the same. Each
engine keeps its own images, containers and volumes: a database created under
Podman is **not** visible to Docker — move it with a dump (README, *Backup and
restore*, replacing `podman` by `docker`).

The compose file carries what Podman needs and Docker ignores (fully qualified
image names `docker.io/…`, `:ro,z` on bind mounts, `label=disable` on the CDI
worker); keep them when editing it.

## Run

The Makefile picks Podman when it is installed, else Docker; on a box with both,
force Docker with `ENGINE=docker` (`export ENGINE=docker`, or on each command).
`make help` shows the engine in use.

```sh
cp .env.example .env
ENGINE=docker make up-gpu      # = docker compose --profile gpu up -d --build
ENGINE=docker make up-cpu      # = docker compose --profile cpu up -d --build
ENGINE=docker make init-db
ENGINE=docker make update COUNTRY=FR YEAR=2025
```

Do not run the two stacks at once: they publish the same ports (5434, 5050, 6006, 4317).

The GPU worker needs the NVIDIA Container Toolkit with the Docker runtime
configured (`sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker`).
`COMPOSE_PROFILES=gpu` in `.env` makes a plain `docker compose up -d` start it.

## Podman commands, translated

| Podman (in the docs) | Docker |
|---|---|
| `podman-compose up -d` | `docker compose up -d` |
| `podman-compose --profile gpu-cdi up -d` | `docker compose --profile gpu up -d` |
| `podman exec nomergon-worker-cdi /app/.venv/bin/nomergon …` | `docker compose exec worker nomergon …` |
| `podman-compose --profile gpu-cdi up -d --no-deps --force-recreate worker-cdi` (after editing `.env`) | `docker compose --profile gpu up -d --no-deps worker` |
| `podman logs -f nomergon-worker-cdi` | `docker compose logs -f worker` |
| `podman exec -i nomotheca-legislation-db psql -U jrc -d legislation` | `docker exec -i nomotheca-legislation-db psql -U jrc -d legislation` |
| `podman volume ls \| grep pgdata` | `docker volume ls \| grep pgdata` |
| `podman run --rm -v euromod_pgdata:/data … docker.io/library/alpine …` | `docker run --rm -v euromod_pgdata:/data … alpine …` |
| `podman-compose down -v` | `docker compose down -v` — same warning: it deletes the database |

Recreate only the worker after editing `.env` (`--no-deps`): a plain `up -d` of the
worker may restart Postgres and kill a running job.
