# Running from CompasOS's SD card

This branch is SonixOS with one addition: a third pill in the power menu that
hands the device back to CompasOS. It is the other half of
[compas-sonix-multiboot](https://github.com/VangerXiao/compas-sonix-multiboot);
CompasOS keeps the internal flash, SonixOS lives on the card, and either one can
hand over to the other without pulling the card or touching the recovery
partitions.

## The two directions

| From | Action | What happens |
|---|---|---|
| CompasOS | Settings -> System -> "Reboot to SonixOS" | writes `/sonix/boot`, reboots; CompasOS's `S20sonix` hook boots this player |
| SonixOS | power menu -> "Slide to reboot to CompasOS" | writes `/usr/data/boot_compas`, reboots; the hook clears both files and boots CompasOS |

A plain restart inside SonixOS keeps SonixOS (`/sonix/boot` is deliberately left
in place), so the choice to leave is explicit.

`/usr/data` is bind-mounted from `/sonix/data` on the card before the chroot, so
`boot_compas` lands on the card even though this player only ever sees
`/usr/data`.

## What the card needs

```
/sonix/rootfs.squashfs    this image
/sonix/data/              SonixOS's /usr/data (settings, database, covers)
/sonix/boot               written by CompasOS
/r1.upt                   recovery image for volume-up flashing
```

## Building the image

```sh
make target                      # builds the Rockbox MIPS toolchain on first run
cp sonix_player <rootfs>/usr/bin/sonix_player
cp sonix_launch <rootfs>/usr/bin/sonix_launch
mksquashfs <rootfs> rootfs.squashfs -comp lzo -b 131072 -noappend
```

## Root filesystem changes that go with it

These are in the packed image, not in this repository's source:

- `/etc/init.d/S11jpeg_display_shell` and `S21mount_ubifs` get
  `grep -q " /usr/data " /proc/mounts ||` in front of their `mount_ubifs.sh
  userdata /usr/data/` calls, so they leave the bind mount alone.
- `/usr/data` is created in the image as a mount point.

Without those, SonixOS would mount the internal `userdata` volume over the card's
directory and lose its own settings on every boot.

The language entry for the new pill is in
`sonix-packer/assets/R1/usr/resource/sonix/language/*.ini`.
