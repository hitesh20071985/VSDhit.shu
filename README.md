# Welcome
This is a repository for providing outputs of the workshop/tutorial I am attending these days.
A brief introduction is provided in the welcome video to provide insights of what this workshop is all about, followed by the tool installation. Although I would not hesitate to mention that after a long long time someone has beautifully covered the basics of HDL and RTL design.
## Tool Installation
A caution here, make sure that you're using Ubuntu 22.04 with minimum 100GB storage and minimum 8GB RAM allocated to it in Virtual machine. Also, do not use 3D accelerator, that would cause unexpected outputs

<details>

<summary> Tool Installation </summary>
### Installing YOSYS

```
$ git clone https://github.com/YosysHQ/yosys.git
$ cd yosys
$ sudo apt install make (If make is not installed please install it)
$ sudo apt-get install build-essential clang bison flex \
    libreadline-dev gawk tcl-dev libffi-dev git \
    graphviz xdot pkg-config python3 libboost-system-dev \
    libboost-python-dev libboost-filesystem-dev zlib1g-dev
$ make
$ sudo make install
```

![Setup](Images/image0.png)


# VSDhit.shu
# VSDhit.shu
