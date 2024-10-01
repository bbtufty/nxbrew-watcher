# NXBrew-watcher

[![Actions](https://img.shields.io/github/actions/workflow/status/bbtufty/nxbrew-watcher/build.yaml?branch=main&style=flat-square)](https://github.com/bbtufty/nxbrew-watcher/actions)
[![License](https://img.shields.io/badge/license-GNUv3-blue.svg?label=License&style=flat-square)](LICENSE)

Intro text

Installation
------------

NXBrew-watcher can be installed by cloning the repository and installing via pip:
  
```shell
git clone https://github.com/bbtufty/nxbrew-watcher.git
cd nxbrew-watcher
pip install -e .
```

Running NXBrew-watcher
----------------------

After installing, you can run simply by:

```python
import os
os.system(r"python nxbrew-watcher\nxbrew_watcher.py")
```

Environment variables
---------------------

NXBrew-watcher pulls in a number of environment variables that can be configured. These are:

* `CONFIG_DIR`: Where to save cache and log files to
* `NXBREW_DISCORD_URL`: Webhook URL for Discord to post updates (see [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))
* `NXBREW_CADENCE`: Cadence to perform search on (in minutes). Defaults to 1.
* `NXBREW_LOG_LEVEL`: Level for log files. Defaults to INFO
