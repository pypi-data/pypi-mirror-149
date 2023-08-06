################
Racker changelog
################


in progress
===========


2022-05-08 0.1.0
================

- Add ``ImageProvider`` implementation to provision operating system images
- Add resources and documentation for sandbox setup based on Vagrant
- Supported operating systems:
  Debian, Ubuntu, Fedora, openSUSE, Arch Linux,
  CentOS, Rocky Linux, Amazon Linux, Oracle Linux
- Add basic probing for unit ``systemd-journald``
- Add example probe implementation for the Apache web server
- Add ``postroj pkgprobe`` implementation
- Add ``postroj list-images`` subcommand
- Add caching of download artefacts
- Improve robustness and documentation
- Add subcommand ``postroj pull [--all]``
- Add subcommand ``postroj selftest {hostnamectl,pkgprobe}``
- Improve process management of container wrapper
- Generalize process wrapper for launching Nspawn containers
- Add subcommand ``postroj run``
- Fix ``stty: 'standard input': Inappropriate ioctl for device``
- Refactor application settings
- Add software test framework and basic tests for ``postroj run``
- Refactor data model for curated operating systems / disk images
- Allow ``versionname`` labels like ``debian-11`` for addressing curated filesystem images
- Rename project to *Racker* and Python package to ``racker``


2022-03-16 0.0.0
================

- Add convenience wrapper around ``systemd-nspawn``
- Add convenience wrapper around Windows Docker Machine
