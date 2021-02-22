---
categories:
- howto
tags:
- fedora
- centos
- linux
- howto
- best practices
image: assets/images/best-practices.png
layout: post
title: The best practice method to install VirtualBox on Fedora 32/33 (and later)
date: 2021-02-22 22:55 +0800
---
In any linux distribution, there will be multiple methods to achieve a certain goal.
You might have encountered many guides out there on how to install [VirtualBox](https://www.virtualbox.org/) on Fedora, however, please take note, many of them uses intrusive methods
which can be difficult to maintain in long run, and would likely to break after
a kernel update.

Everytime I caught a new team member following those guides, I tend to get annoyed, so
I think I should write up the best practice method of doing this, which I have practiced
on my Fedora installation for years now.

Installing RPMFusion Repository
-------------------------------

Packages governed in Fedora official repositories are subject to several legal and technical
guideline. This mean, many software which are not 100% FOSS or not patent-encumbered would
not be available in the official repositories because they would open the sponsors of Fedora
to legal liability under the laws of United States. 

Unfortunately, many free/open source software are patent incumbered, but while they might
be illegal to distribute in the United States, they are perfectly legal to distribute in other
countries.

Many of such packages are available in [RPMFusion Repositories](https://rpmfusion.org/). 
Unlike many 3rd party repositories out there, RPMFusion contains the highest quality
packages as its contributor also consist of people who package official RPMS in Fedora, and
I generally recommend any new users of Fedora to install RPMFusion, especially if they are
not US residents.

To install and enable RPMFusion on Fedora, you can install the release package using following
command which will install both the free and nonfree repositories:

```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
    https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

Installing VirtualBox
----------------------

Once you have RPMFusion installed, you can then install VirtualBox from it. VirtualBox in 
RPMFusion is very well maintained, would remain functional after kernel updates through
an automatic kernel module builder (`akmods`), and generally carry the latest version of
VirtualBox.

```bash
sudo dnf install VirtualBox
sudo akmods
sudo modprobe vboxdrv
```

And you are done and can now launch VirtualBox from the application menu. Please
take note however, VirtualBox does not go well together with `libvirtd`. If you have
`libvirtd` installed, it is suggested for you to disable it using:

```bash
sudo systemctl stop libvirtd
sudo systemctl disable libvirtd
```

Hope this guide will help you in installing VirtualBox in a less intrusive and 
more maintainable method. 
