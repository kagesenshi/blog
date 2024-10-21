---
layout: post
title: Adjusting trackpoint (or any pointing device) sensitivity through evdev
categories:
- blog
tags:
- thinkpad
- trackpoint
- linux
- fedora
image: assets/images/terminal-python.jpg
date: 2024-10-22 06:40 +0800
---
Recently I got myself a Thinkpad X1 Tablet Gen 3, however, unlike other Thinkpads, this model does
not seem to use the usual Thinkpad kernel module which allows sensitivity to be set in `sysfs`.

Thanks to some inspiration from ChatGPT, I found out that it is possible to apply multiplier
to the event stream by building a daemon that intercept the input events and modify it. 

So here's how you can do it:

## Dependency

On Fedora, you will need python3-evdev installed

```bash
sudo dnf install python3-evdev 
```

## Event modification script

Save this in `/usr/local/bin/alter-sensitivy.py`

```python
import evdev
from evdev import InputDevice, UInput, ecodes
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d','--device', required=True)
parser.add_argument('-m','--multiplier', type=int, default=2)
parser.add_argument('-t','--trigger-threshold', type=int, default=2)

args = parser.parse_args()

# Open the input device
device = InputDevice(args.device)

# Create a virtual input device to emit the modified events
ui = UInput.from_device(device, name="ModifiedDevice")

# Loop to process incoming events
for event in device.read_loop():
    if event.type == ecodes.EV_REL and abs(event.value) > args.trigger_threshold:  # Modify only relative movement events if it above threshold
        for i in range(args.multiplier):
            print(event.value)
            ui.write_event(event)
            ui.syn()
            time.sleep(0.0005) # for smoothing out the movement
    else:

        # Emit the modified event
        ui.write_event(event)
        ui.syn()
```

Find your device using `sudo libinput list-devices` and `evtest [device]`.

Test it out. In this example I'm altering event of `/dev/input/event5` input device which is
my trackpoint. `-m` option allows you to configure how much you want to multiply 
the event (default is `2`).

```bash
sudo python3 /usr/local/bin/alter-sensitivity.py -d /dev/input/event5 -m 5
```

## Systemd service

Create a systemd service file in `/etc/systemd/system/trackpoint-sensitivity.service`
(change `/dev/input/event5` to your own device)

```ini
[Unit]
Description=Trackpoint Sensitivy
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/local/bin/alter-sensitivity.py -d /dev/input/event5
Restart=always
User=root
Group=input
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Start it

```bash
systemctl daemon-reload
systemctl start trackpoint-sensitivity
```

