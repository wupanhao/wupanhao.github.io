# 1.6 pianopi 把你的树莓派变成一架钢琴


一直有个想法，想给自己制作一件乐器，作为一名程序员，每天跟键盘打交道，要是把敲键盘变成弹奏乐曲，那是相当美妙的一件事

去网上搜索资料，发现不是我有这个想法，早已有人成功实现，自己也成功移植到树莓派上，下面介绍一下相关经历

### 先更新软件包
sudo apt update

### 再安装所需软件
sudo apt install git python-scipy python-pygame

### clone github上的代码

`cd ~ ; git clone https://github.com/Zulko/pianoputer`

再`cd pianoputer`然后`python pianoputer.py`，稍等大约一分钟然后你就拥有一台用树莓派制作的"钢琴"了，注意这里一定需要在图形界面下运行(VNC 或者 连显示器，pygame需要打开一个图形窗口捕捉键盘事件)


## 配置开机自启动
如果每次启动都需要访问图形界面岂不是太麻烦，我们可以设置开机自动运行，这样你就有一架行走的"钢琴"了，移动电源供电可以轻松带起几个小时~

### 先创建一个启动脚本
`vim ~/pianopi.sh`

```
#!/bin/bash
sudo su - pi -c " cd /home/pi/pianoputer ; python pianoputer.py"
```

别忘了给它加上可执行权限，否则无法启动成功`chmod +x ~/pianopi.sh`


### 配置在图形界面下的开机自启动
默认会读取用户家目录下.config/autostart文件夹下的*.desktop文件一个一个执行，因此创建一个即可

```
mkdir -p ~/.config/autostart
vim ~/.config/autostart/piano.desktop
```

```
[Desktop Entry]
Type=Application
Exec=/home/pi/pianopi.sh
```

### 更改键盘对应的音符
默认的键盘映射不太符合个人习惯，改为了从左shift开始逐行升调，找了会音乐的同学校对了一下音准，如下图

# image

```
left shift
z
x
c
v
b
n
m
,
.
/
right shift
a
s
d
f
g
h
j
k
l
;
'
tab
q
w
e
r
t
y
u
i
o
p
[
]
#
`
1
2
3
4
5
6
7
8
9
0
-
=
```