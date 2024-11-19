# NXBrew-watcher

[![Actions](https://img.shields.io/github/actions/workflow/status/bbtufty/nxbrew-watcher/build.yaml?branch=main&style=flat-square)](https://github.com/bbtufty/nxbrew-watcher/actions)
[![License](https://img.shields.io/badge/license-GNUv3-blue.svg?label=License&style=flat-square)](LICENSE)

NXBrew-watcher is a Docker container designed to watch NXBrew for additions and updates, and push them through to
a Discord server.

Usage
-----

The easiest way to run NXBrew-watcher is through docker-compose:

```
services:

  nxbrew-watcher:
    image: ghcr.io/bbtufty/nxbrew-watcher:latest
    container_name: nxbrew-watcher
    network_mode: bridge
    environment:
      - NXBREW_URL=https://some_nxbrew_url.com
      - NXBREW_DISCORD_URL=https://some/webhook/url #optional
      - NXBREW_CADENCE=1 #optional
      - NXBREW_LOG_LEVEL=INFO #optional
    volumes:
      - path/to/config:/config
    restart: unless-stopped
```

Environment variables
---------------------

NXBrew-watcher pulls in a number of environment variables that can be configured. These are:

* `NXBREW_URL`: NXBrew URL. Must be set
* `NXBREW_DISCORD_URL`: Webhook URL for Discord to post updates (see [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))
* `NXBREW_CADENCE`: Cadence to perform search on (in minutes). Defaults to 1.
* `NXBREW_LOG_LEVEL`: Level for log files. Defaults to INFO
