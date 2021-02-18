---
categories:
- howto
tags:
- fedora
- centos
- linux
- howto
image: assets/images/terminal-python.jpg
layout: post
title: Creating XDG custom url scheme handler
date: 2021-02-18 22:49 +0800

---

If you develop system tools or desktop software on Linux that also have an 
accompanying web application, you might want to have a way for the web application
to launch the tool with some parameters specified through a web based link. For
example, a link with [`dnf://inkscape`](dnf://inkscape) as url, might be used to launch
Gnome Software, and display the description of Inkscape, so that user may choose
to install it or not.

In Linux, registering a custom URL handler can be done using [XDG desktop file](
https://specifications.freedesktop.org/desktop-entry-spec/latest/), of which 
it is configured to open `x-scheme-handler` MimeType. 

To achieve this, you can simply create a `.desktop` in `~/.local/share/applications/`, or
`/usr/local/share/applications`, and configure it with `MimeType=x-scheme-handler/<your-custom-proto>`.

For example, if you have a script `dnfurl` which takes `dnf://<package-name>` as its,
first parameter and launch Gnome Software with the package name, you can create a `.desktop`
file with this content:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=dnfurl
Exec=dnfurl %U
Terminal=false
NoDisplay=true
MimeType=x-scheme-handler/dnf
```

After installing the `.desktop` file, do run `update-desktop-database` to update the related
indexes/cache. If you installed the `.desktop` file in `~/.local/share/applications/`, you will have to run `update-desktop-database ~/.local/share/applications`. 

If you interested with the example `dnfurl` program above, you can check it out at this git
repository: [`github.com/kagesenshi/dnfurl`](https://github.com/kagesenshi/dnfurl). Or if you are in Fedora, you can install
it [from copr](https://copr.fedorainfracloud.org/coprs/izhar/dnfurl/) by running:

```bash
dnf copr enable izhar/dnfurl
dnf install dnfurl
```

Have fun~.
