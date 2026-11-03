# Scripts

| Script | Purpose |
|---|---|
| `pack-sonix-zip.py` | build the `sonix.zip` the dual-boot release ships (`sonix/rootfs.squashfs` plus an empty `sonix/data/`) |

## Why a script and not "just zip it"

A zip made on Windows with `Compress-Archive` stores backslash separators. On
Linux it then unpacks into a single file named `sonix\rootfs.squashfs`, and the
boot hook finds no root filesystem at all. `pack-sonix-zip.py` writes proper
forward-slash entries, so the archive behaves the same everywhere.

## Building the image itself

This repository builds the player; the SD-card image is a stock SonixOS root
filesystem with two changes:

1. `/usr/bin/sonix_player` and `/usr/bin/sonix_launch` replaced by
   `make target` output;
2. `/etc/init.d/S11jpeg_display_shell` and `S21mount_ubifs` guarded with
   `grep -q " /usr/data " /proc/mounts ||` in front of their
   `mount_ubifs.sh userdata /usr/data/` calls, and `/usr/data` created as a
   mount point — see `docs/COMPAS-MULTIBOOT.md`.

Then:

```sh
scripts/pack-sonix-zip.py rootfs.squashfs sonix.zip
```
