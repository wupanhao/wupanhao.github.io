# 1.3 树莓派常用设置

#### 添加中文支持
安装中文字库`sudo apt-get install -y ttf-wqy-zenhei`
安装中文拼音输入法`sudo apt-get install -y fcitx fcitx-pinyin`或`sudo apt-get install scim-pinyin`

#### zsh 终极shell
安装`sudo apt-get install -y zsh`
配置`sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"`
需要curl和git支持

#### 远程桌面

*vnc*
`sudo apt-get install tightvncserver`

安装完成后，运行`vncpasswd`设置密码，运行`vncserver`启动服务器

便可通过VNC Viewer等访问，注意加上端口号，默认从5901开始递增

*xrdp WINDOWS的远程桌面*

`sudo apt-get install xrdp`

#### lrzsz 简易文件传输（主要针对Windows）
`sudo apt-get install lrzsz`

安装完成后，当使用Xshell等终端远程登录时，可以使用`sz filename`发送文件，`rz`接收文件

Linux和Mac OS X可以直接用scp命令更方便

#### tmux终端分屏
`sudo apt-get install tmux`
安装完成后可通过`tmux`启动
Ctrl + b是它的热键，激活之后可以通过%切竖屏，"切横屏，上下左右切换等，非常方便，特别是配合vim使用 

#### 比较实用的Linux命令

查找大于100M的文件`sudo find / -size +100M -exec ls -lh {} \;`

利用socat做端口转发`nohup socat TCP4-LISTEN:8080,fork,su=nobody TCP6:scpi2.wupanhao.top:80 &`

查看打开的网络端口`netstat -tlnp`或`ss -l`

挂载samba共享目录`sudo mount -t cifs -o username=877594836@qq.com,password=123456 //192.168.31.189/kugou /mnt/kugou`

端口扫描`nmap 172.16.122.0/24 -p 22`

