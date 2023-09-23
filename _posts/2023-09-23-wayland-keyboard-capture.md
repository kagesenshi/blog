---
layout: post
title: Allowing keyboard capture for Remmina, Virt Manager and other software in GNOME
  Wayland
categories:
- blog
tags:
- fedora
- wayland
image: assets/images/f39.png
date: 2023-09-23 09:26 +0800
---
One capability seems missing in Wayland compared to X11 is the ability to fully capture keyboard events, for example when using remote desktop tools or virtual machines.

Apaprently, this is implemented differently now in Wayland, where the desktop evironment need to allow application to inhibit shortcut keys. To do this in GNOME, go do **Settings > Apps > $application_name** and allow **Inhibit shortcuts**

![Wayland inhibit shortcut](assets/images/2023/09/wayland-inhibit-shortcut.png)
