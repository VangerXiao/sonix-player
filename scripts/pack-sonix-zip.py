#!/usr/bin/env python3
"""Package a SonixOS root filesystem into the sonix.zip the README describes.

    scripts/pack-sonix-zip.py <rootfs.squashfs> <out.zip>

The zip has to be built here rather than with a desktop archiver: Windows'
Compress-Archive writes backslash separators, so a zip made on Windows unpacks
on Linux into a file literally called "sonix\\rootfs.squashfs" instead of the
directory tree the boot hook needs.

Layout inside the archive:

    sonix/
    sonix/data/            empty; SonixOS keeps its settings here
    sonix/rootfs.squashfs

An empty data/ entry is included so a plain unzip leaves the mount point in
place, but an existing one on the card is not disturbed.
"""

import os
import sys
import zipfile


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        return 2
    src, out = sys.argv[1], sys.argv[2]
    if not os.path.isfile(src):
        print("not a file: %s" % src)
        return 1

    if os.path.exists(out):
        os.remove(out)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(zipfile.ZipInfo("sonix/"), "")
        z.writestr(zipfile.ZipInfo("sonix/data/"), "")
        z.write(src, "sonix/rootfs.squashfs")

    with zipfile.ZipFile(out) as z:
        for info in z.infolist():
            print("%-28s %10d -> %10d" % (info.filename, info.file_size, info.compress_size))
    print("size:", os.path.getsize(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
