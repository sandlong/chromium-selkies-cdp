# brave-vnc-cdp

[![Docker publish](https://github.com/sandlong/brave-vnc-cdp/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/sandlong/brave-vnc-cdp/actions/workflows/docker-publish.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

A Docker image for **Brave Browser + noVNC + raw VNC + Chrome DevTools Protocol (CDP)**, intended for local browser automation on **Linux arm64/aarch64** as well as amd64.

## What it provides

- Official **Brave Browser** installed from Brave's Linux APT repository
- **Xvfb** virtual display for headed browsing inside a container
- **Openbox** lightweight desktop session
- **x11vnc** server on port `5900`
- **noVNC** web client on port `8080`
- **CDP** endpoint on port `9222`
- Persistent browser profile storage in `/data/profile`

## Quick start

### Pull from GHCR

```bash
docker pull ghcr.io/sandlong/brave-vnc-cdp:latest
```

### Docker run

```bash
docker run -d \
  --name brave-vnc-cdp \
  -p 8080:8080 \
  -p 5900:5900 \
  -p 9222:9222 \
  -e TZ=Asia/Singapore \
  -e VNC_PASS='change-me-now' \
  -e START_URL='https://example.com' \
  -v brave-data:/data \
  ghcr.io/sandlong/brave-vnc-cdp:latest
```

### Build locally

```bash
docker build -t brave-vnc-cdp .
```

### Docker Compose

```bash
docker compose up -d --build
```

## Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `TZ` | `UTC` | Container timezone |
| `VNC_PASS` | `change-me` | Password for x11vnc |
| `VNC_WIDTH` | `1440` | Virtual display width |
| `VNC_HEIGHT` | `900` | Virtual display height |
| `VNC_DEPTH` | `24` | Color depth |
| `VNC_PORT` | `5900` | Raw VNC port |
| `WEB_PORT` | `8080` | noVNC/websockify port |
| `CDP_PORT` | `9222` | Chrome DevTools Protocol port |
| `BRAVE_INTERNAL_CDP_PORT` | `9223` | Internal loopback CDP port used by Brave itself |
| `VNC_SHARED` | `false` | Allow multiple VNC viewers |
| `START_URL` | `about:blank` | Initial page to open |
| `USER_DATA_DIR` | `/data/profile` | Persistent Brave profile path |
| `BRAVE_NO_SANDBOX` | `true` | Add `--no-sandbox` inside container |
| `BRAVE_ARGS` | empty | Extra Brave flags as a single string |
| `DAILY_RESTART_AT` | empty | Restart the browser/container daily at `HH:MM` |

## Maintenance

### Daily Restart

If `DAILY_RESTART_AT` is set (e.g., `04:00`), the container process will exit at that time. When combined with Docker's `restart: always` policy, this provides a clean, daily-refreshed browser instance without losing persistent data in `/data`.

## Publishing

This repository includes a GitHub Actions workflow that builds and publishes a multi-architecture image to GHCR for `linux/amd64` and `linux/arm64`.

The workflow also runs on a daily schedule to catch upstream Brave updates. It checks the latest version available and only builds if a new version is detected.

## Logs

Runtime logs are written inside the container under `/var/log/brave-vnc-cdp/`.
