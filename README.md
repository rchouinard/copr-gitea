# Gitea on COPR

[![ico-build-status]][link-build-status]

This repository simply provides COPR builds of [Gitea][link-gitea] for recent versions of [Fedora Linux][link-fedora].

## Installation

First, you must enable the repository:

    $ sudo dnf copr enable rchouinard/gitea

Gitea is now available for installation:

    $ sudo dnf install gitea

## Usage

Application configuration is installed under `/etc/gitea`. Tune to your liking before enabling and running the service:

    $ sudo systemctl enable --now gitea

The package expects the service to run under the `gitea` user.

## Issues

Please report any application issues to the [Gitea project][link-gitea]. Any installation issues related to this package should be reported [here][link-self-github].

## Legal

The author and contributors to this repository are not affiliated with the Gitea project in any way. This project simply aims to provide a simple installation method for the Gitea application on current Fedora versions.


[ico-build-status]: https://copr.fedorainfracloud.org/coprs/rchouinard/gitea/packages/gitea/status_image/last_build.png

[link-build-status]: https://copr.fedorainfracloud.org/coprs/rchouinard/gitea/package/gitea/
[link-gitea]: https://gitea.io/
[link-fedora]: https://getfedora.org/
[link-self-github]: https://github.com/rchouinard/copr-gitea/