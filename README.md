# Face-Check

This project offers a simple face recognition application using [facenet-pytorch](https://github.com/timesler/facenet-pytorch) with user-friendly GUI. This is designed for actual and practical use where you need to check specific people like your colleagues, friends, and family members.

(picture)

## Requirement

This application is supporsed to run on NVIDIA Jetson Nano. Here is the detail.

* NVIDIA Jetson Nano Developer Kit
* NVIDIA JetPack 5.0 (6.0 compatible is coming soon)
* USB Web Camera or Raspberry Pi Camera module V2

## Quick Start

To install

~~~
git clone https://github.com/take5553/face-check.git
cd face-check
chmod +x run.sh
~~~

To run

~~~
./run.sh
~~~



### Sound Settings

Start button -> Sound and Video -> PulseAudio Sound Settings -> Settings Tab

Built-in Audio(The second one): Off

### `docker` command without `sudo`

~~~
sudo gpasswd -a $USER docker
sudo reboot
~~~

## Usage

(under construction)

## 