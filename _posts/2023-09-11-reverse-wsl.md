---
layout: post
title: Creating "Reverse WSL" For Running Windows Application On Linux Host
categories:
- blog
tags:
- fedora
- windows
- virtualization
image: assets/images/rwsl.png
date: 2023-09-11 00:01 +0800
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/L9j6-vpuSmY?si=-tmP8sotHIb3oUe0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### State of the linux desktop in 2023

Linux today have matured to the point where majority of activities commonly done by computer users can be achieved easily, especially considering most people are primarily using the computer to access internet applications. Even when it comes to gaming, thanks to Steam's effort in Proton and Steam Deck, Linux is now a pretty viable platform for those who who are not playing competitive games. 

People I know also have experimented with making purely non-technical people to use Linux without them knowing, with good success rate, while I myself have experimented with forcing my department staff to use Linux as their primary operating system with good success, to the point of the staff noticed that Windows is a pretty difficult platform to work with for modern day developers. 

Libreoffice also is fully capable to do all common office tasks without issues, and with some training to leverage the features available in Libreoffice, the team also discovered how frustrating it can be when working with Microsoft Office especially when trying to structurally automate formatting. A simple tool you know how to use well is a magnitude better than a fancy tool that you only know how to use its basic feature. Libreoffice also opens Microsoft Office documents well with minimal issues, except for the usual missing fonts messing with documents a bit, which easily fixed by installing the fonts.

However, Microsoft Office dominance can be an annoying problem when working with clients that primarily uses Microsoft's stack and refuses to accept or work with PDF. Microsoft Office also almost always open ODF poorly with regular corruption, while DOCX files saved by Libreoffice seems to almost always opened poorly by Microsoft Office.

Wine, while becoming a great platform to run games thanks to Proton initiative, is still quite flaky to run Office due to less community investment is put on the matter. The [Wine AppDB page for Office](https://appdb.winehq.org/objectManager.php?iId=31&sClass=application) generally reported garbage rating for Office 2016 and newer.

### Windows Subsystem For Linux (WSL)

The frustration regularly faced by developers when working on Windows, and the dominance of Open Source in software development ecosystem to a degree threathened Windows, where developers preferring MacOS for their preferred desktop because of its Unix heritage and MacPorts.

In response to that , for a few years now, Windows introduced the ability to run Linux commandline seamlessly on Windows through their WSL feature which essentially runs a Linux VM on top of Windows, with seamless filesystem integration to allow access of files in the host by the guest VM. This to a degree allows developers to have access to their Linux tooling on Windows, alongside access to Microsoft Office. 

WSL also shows that, with some clever virtualization tricks to integrate the host and guest, the experience of using VM can be pretty seamless to the user if done well.

### Reverse WSL With QEMU, Libvirt, VirtIO & SPICE/RDP

For those who primarily use Linux as their daily driver and dealing with clients who are locked into Microsoft ecosystem (even rejecting Google Docs), the lack of Microsoft Office on Linux sometimes forces people to switch to Windows in order to get work done, which usually means a troublesome dual computer operation. 

However little is known to most that Linux virtualization have also improved significantly over the past several years, where it is now possible to create a "Reverse WSL" that allows you access to Microsoft Office on your Linux desktop, complete with clipboard sharing and filesystem sharing, with near-native performance using QEMU KVM virtualization. Effectively allowing you to keep using Linux as your primary operating system, while still getting access to Microsoft Office without having to dual-boot or lugging two computers around. 

This guide will help you set up your computer with a highly fine tuned VM of Windows 11, alongside customizations needed to make integration seamless between the two operating systems, so that you can get benefits of both worlds on a single unified dual operating system experience. 

#### System Requirements

This guide assumes that you have at least 4c/8t CPU with 16GB of RAM, and you are using Fedora as the primary operating system. Any other Linux distro should work too, but this guide focuses on Fedora.

You may want to use Windows 10 Pro or Windows 11 Pro as I found RDP local cursor give a better experience compared to SPICE. RDP is only available on the Pro edition of Windows.

#### Setting Up The VM

You will need to install and use QEMU and Libvirt for your virtualization, as VirtIO comes with it.

```bash
$ sudo dnf install virt-manager libvirt-daemon-kvm -y
$ sudo systemctl enable --now libvirtd.service
```

For near-native performance, we will be using VritIO to improve both disks, network and graphics I/O, which means, the VM creation process would be slightly different. 

The first step is to start up Virt Manager, and before starting with installation, you will need to enable XML editing at **Edit > Preferences**

![Screenshot from 2023-09-10 12-04-11.png](/assets/images/reverse-wsl/61b08731fb9a4109a111e2d1bf130aab.png)

Then, create a new VM with at least 2 cores, and 8GB of RAM (you can enable ballooning later). Make sure that you check "Customize configuration before install" option at the final step of VM creation.

![Screenshot from 2023-09-10 11-58-00.png](/assets/images/reverse-wsl/f5b247bf0f1342e7a32307046893f3e4.png)

![Screenshot from 2023-09-10 12-08-43.png](/assets/images/reverse-wsl//e59e943d725e489eb9c1d2ba958bada7.png)

![Screenshot from 2023-09-10 11-58-21.png](/assets/images/reverse-wsl//720b703a61e84a14a0cd9e4c5f5ee750.png)

![Screenshot from 2023-09-10 11-59-07.png](/assets/images/reverse-wsl//c84d75d9c1fc4e25b8e3e34c55a522d0.png)

At the customization page, you will need to configure the following:

1. CPU Pinning

   ![Screenshot from 2023-09-10 12-09-46.png](/assets/images/reverse-wsl//c9ee0241c59048df8be3c02213795ace.png)
   
   Replace `<vcpu>2<vcpu>` with:
   
   ```xml
     <vcpu placement="static" cpuset="1,2">2</vcpu>
     <cputune>
       <vcpupin vcpu="0" cpuset="1"/>
       <vcpupin vcpu="1" cpuset="2"/>
     </cputune>
   ```
   
   This will pin the 2 CPU to physical core 1 (second core) and core 2 (third core) of the base host, minimizing competition with the main operating system running at core 0 (first core). You can view which core tied to which cpuset by running `cat /proc/cpuinfo |egrep -i 'processor|core id'`. `processor` is the cpuset id, while `core id` is the physical core id.


2. Set SPICE port 

   ![801899947084c122e9a703b84096614a.png](/assets/images/reverse-wsl/801899947084c122e9a703b84096614a.png)

3. Change default disk to VirtIO bus

   ![f2d14462bca721f419b98ea5723d5bf7.png](/assets/images/reverse-wsl/05a73d0172fb4e71ba6f546c3e7e9f6e.png)

4. Set VirtIO Video

   ![5cb8577f26f7d63169a2988eb556c867.png](/assets/images/reverse-wsl//0a46dcf7d8e14dd99a7d85be5033cd2f.png)

   Disable 3D accelleration, as it does not work on Windows guests unless you use GPU passthrough in multi-GPU computer.

5. **(Optional)** If you will only have 1 windows VM, you may want to use TPM passthrough. 

   ![9e6f389d39dca4bd249aa6f634033d73.png](/assets/images/reverse-wsl//ccbead4b857a4fd194b1c58471f4b1fc.png)

6. Add VirtIO driver ISO image as another SATA CDROM. You will need it to load VirtIO driver

   ![3f239e940b4d6d2511a023335243b7f9.png](/assets/images/reverse-wsl//523a6fbd3fec4a37a7cb3c9c90b8b75f.png)

   You can get VirtIO driver ISO image from Fedora here: <https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso>

7. Configure HyperV optimization. 

   ![6ed357ee7d3192bb75be953cc34aea1b.png](/assets/images/reverse-wsl//335895b023734bf9a007b3d75f8b2882.png)

   Set the configuration to:
   
   ```xml
       <hyperv mode="custom">
         <relaxed state="on"/>
         <vapic state="on"/>
         <spinlocks state="on" retries="8191"/>
         <vpindex state="on"/>
         <synic state="on"/>
         <stimer state="on"/>
         <reset state="on"/>
       </hyperv>
   ```
   
8. Enable shared memory (this is needed later for filesystem sharing)

   ![24f3f26420939629495918bfd2e02a92.png](/assets/images/reverse-wsl//e9112188e131422dbf58c5320d558962.png)

9. Add filesystem sharing to your Home directory

   ![5fd1a365bcbb39fd0b427b3477bf9e82.png](/assets/images/reverse-wsl//1f462201a3614e15939b87bf08166d5d.png)

10. Then click **Begin Installation** to start installation. 

   When at the disk selection you will see that there are no disk to select. This is because Windows does not carry VirtIO disk drivers by default. You will need to load the driver from the secondary CD drive.
   
   ![d8e04293c14c805a42661a89dc42d1e0.png](/assets/images/reverse-wsl/972a12781d194a4fa32900674131b0c7.png)
   
   ![29d87b13b54d48ad069ac9d4f7224575.png](/assets/images/reverse-wsl/778ee7dee2504b0ea8c99b8733ce9c28.png)
   
   ![a8ebffcfeccb3c030fe47a6c9dbb09d1.png](/assets/images/reverse-wsl/af27f55786a54ef6bed89ed79cea936c.png)
   
   Then proceed the installation as you would normally
   
   ![c2d6c93cb0d5b566922b9b2fb2ce6113.png](/assets/images/reverse-wsl/9965f2780758427091313570a2d8172d.png)
   
   On first boot , to improve performance, disable all telemetry monitoring 
   
   ![1d0399064cb6020ed67cadfe5aa1db4c.png](/assets/images/reverse-wsl/70667860f79d444bb1f17de68d23f28e.png)
   
#### Setting up Windows 

After successful installation, you will need to then install the rest of VirtIO drivers, VirtIO guest tools, and WinFSP to further improve host-guest integration and improve user experience.

1. Install VirtIO drivers

   ![40f17b3274c9463d29682d0cef383ac8.png](/assets/images/reverse-wsl/81fe122699d04e2f96eb410e8f0a4f91.png)

2. Install VirtIO guest tools

   ![420e6f638b94174fcce664b1a27e74ca.png](/assets/images/reverse-wsl/342bc7f6205b4649a86adc160cc6cdc1.png)

3. Install WinFSP & Enable VirtIO FS

   WinFSP (<https://github.com/winfsp/winfsp>) provide capabilities similar to FUSE on Windows, which allows mounting of userspace filesystems. It is required in order to mount VirtIO shared filesystem as a drive in Windows. Download and install it, then enable VirtIO FS by enabling the following service in the Services app.

   ![Screenshot from 2023-09-10 21-53-18.png](/assets/images/reverse-wsl/6cfb6d92feac4bacba81fc122e6a3092.png)
   
   ![Screenshot from 2023-09-10 21-53-41.png](/assets/images/reverse-wsl/e1b8af902de945788f9fd19f3e6a2792.png)
   
   If enabled correctly, you will see that a new drive Z:\ appeared that links to the Linux host storage
   
   ![Screenshot from 2023-09-10 21-54-14.png](/assets/images/reverse-wsl/1f52699c2bda41d1b6af3a3dc8251d56.png)
   
4. **(Optional)** Then, enable RDP

   ![f4958f01ca425b8326bc7b15b43d36d1.png](/assets/images/reverse-wsl/fc897f17850848ddb523b5b1c8d96ead.png)

5. Afterwards, shutdown the VM, as we now need to switch the network to VirtIO. Open the VM properties and ensure that NIC is switch to VirtIO

   ![11b06bfa96cf2da6ca416feb3e132a88.png](/assets/images/reverse-wsl/be27e13d3d804f3995f7ba8fca0135d0.png)

6. Now you can start the VM back up.

#### Connecting to VM

To connect to the VM, I recommend to use Remmina

```console
$ sudo dnf install remmina remmina-plugins-spice -y
```

Launch Remmina, then you may want to disable the fullscreen toolbar in Remmina preferences for added seamlessness

![617cece718677af769e1b922937d65e0.png](/assets/images/reverse-wsl/617cece718677af769e1b922937d65e0.png)
 
##### Using SPICE

SPICE is the default remote connection protocol for QEMU and is recommended if you don't have RDP available on
your Windows version. However, it might be a bit of an overhead if you are using older device.

SPICE also uses remote cursor that is rendered on the VM side, which you may experience mouse lag if you 
have slower CPU.

On Wayland on my F37, SPICE also behave weirdly after Alt+Tab when put in full screen mode, where it 
behave as if Alt/Ctrl is always pressed until you leave full screen. 

If you face above issues, then use RDP.

To connect to SPICE, use following settings

- Protocol: SPICE 
- Basic tab:
  - Server: localhost:5900
- Advanced tab:
  - Preferred video codec: VP8
  - Preferred image compression: LZ4
  - Enable audio channel

![ac19822843405d04f683eeff7aa173a9.png](/assets/images/reverse-wsl/ac19822843405d04f683eeff7aa173a9.png)

Click **Save and connect.**, and you now have connected to the VM and can use it. 

Switch to full screen view for seamless display. You will need to set resolution to match your monitor resolution.

Optionally, for better display performance with this method of connection, launch Performance app and configure
it for best performance.

![e33461d312451dc99354652afe56b1b6.png](/assets/images/reverse-wsl/e33461d312451dc99354652afe56b1b6.png)

##### Using RDP

I recommend using RDP because it uses local cursor and suffer less mouse lag compared to SPICE. You also have
better control on display peformance tweaks on the client side, however, it might not perform that well for videos.

To connect to RDP, use following settings

- Protocol: RDP
- Basic tab:
  - Server: IP Address of the VM
  - Username: Windows login username
  - Password: Windows login password
  - Resolution: Use client resolution
  - Network connection type: LAN
- Advanced tab:
  - Quality: Medium/Good
  - Gateway transport type: RPC
  - FreeRDP log level: ERROR
  - Audio output mode: Local
 
![f6a8f2992a211f8e0ce8a54c788ed975.png](/assets/images/reverse-wsl/19189495d06345519d2f9ae38d8d57ed.png)

Click **Save and connect.**, and you now have connected to the VM and can use it.

Switch to full screen view for seamless display.

### Optimization & Tuning

For less CPU and RAM usage, you may want to also do the following:

- Uninstall Microsoft 365 
- Uninstall Microsoft Teams
- Uninstall OneDrive
- Uninstall ClipChamp
- Uninstall Microsoft Todo
- Uninstall Microsoft News
- Uninstall Xbox related packages

If you are on GNOME and is used to use top right hot corner for window switching, you may also want to install Winxcorners, and set top left corner to open Task View. 

I recommend setting the VM wallpaper to match your main desktop wallpaper.

### Conclusion

Windows-on-Linux virtualization have improved significantly today that it is possible to run Windows VM with minimal impact on performance. Open Source RDP
clients also have catched up quite well in bringing smooth integration of audio and clipboard with remote Windows connection that it become pretty seamless to use
Windows applications through RDP, especially for work related applications such as Microsoft office. VirtIO FS in the other hand makes disk integration experience
almost as if you are using Wine.

Using this method, one more barrier of adoption of Linux as primary operating system is solved as it is relatively seamless to work with documents in the VM, that
it barely feel like Microsoft Office is running in a VM.

#### References

- <https://linuxhint.com/install_virtio_drivers_kvm_qemu_windows_vm/>
- <https://leduccc.medium.com/improving-the-performance-of-a-windows-10-guest-on-qemu-a5b3f54d9cf5>


