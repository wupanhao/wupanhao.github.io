# 3.3 代理服务器

## 简单HTTP代理（你以为我会告诉你用我一般它看532？）

当然如果真要看532还要先连接师大VPN，所以，还是VPN大法好

### squid
经典的HTTP代理服务器

### 安装
`sudo apt-get install squid`

### 编辑配置文件
/etc/squid/squid.conf 
有点长，找到如下段落
```
# Example rule allowing access from your local networks.
# Adapt localnet in the ACL section to list your (internal) IP networks
# from where browsing should be allowed
#http_access allow localnet
http_access allow localhost
```
squid默认只接受localhost对特定端口的连接，显然有时不太方便，在后面添加一行
`http_access allow all`
然后重启即可
squid默认监听3128端口


### nginx用作代理服务器
只要修改一下配置就能把nginx当作代理服务器来用

参考配置文件如下

```
server { 
    resolver 8.8.8.8; 
    resolver_timeout 5s; 

    listen 8088; #代理端口

    location / { 
        proxy_pass $scheme://$host$request_uri; 
        proxy_set_header Host $http_host; 

        proxy_buffers 256 8k; 
        proxy_max_temp_file_size 0; 

        proxy_connect_timeout 30; 

        proxy_cache_valid 200 302 10m; 
        proxy_cache_valid 301 1h; 
        proxy_cache_valid any 1m; 
    } 
} 
```

命名为ng-proxy.conf放到/etc/nginx/sites-enabled/目录下重启nginx即可

### privoxy
主要是用来把SOCKS5代理转为HTTP代理的

SOCKS5代理服务器如何搭建参考后面shadowsocks部分

### 安装
`sudo apt-get install privoxy`

### 修改配置文件
/etc/privoxy/config 

做如下更改

`listen-address  localhost:8118`只监听本地显然是不好滴，一般把localhost改为0.0.0.0即可
`#        forward-socks5   /               127.0.0.1:9050 .`取消注释，根据自己SOCKS5代理监听的地址和端口来配置，别忘了最后有一个"."

重启服务器，这样你就有了一个HTTP代理了，手机电脑甚至Linux命令行都能使用

### mproxy
一个非常小巧的用c语言写的代理软件，项目地址在[https://github.com/examplecode/mproxy](https://github.com/examplecode/mproxy) (据说可以翻墙)

## VPN类
天朝局域网下有时为了科学上网的需要，常常需要搭梯子翻墙，VPN就是我们的梯子

天朝内的机器是服务科学上网的，你必须得有一台国外的机器，通常是在国外云服务器厂商那儿租一台VPS,digital ocean、搬瓦工、vultr等都是很好的选择

### shadowsocks
目前最靠谱的科学上网解决方案

### 安装

`sudo apt-get install shadowsocks`或者通过pip安装
```
sudo apt-get install python-pip
sudo pip install shadowsocks
```

安装好之后系统就多了ssserver和sslocal两条命令

### 配置

一般来说shadowsocks只需要一份json格式的配置文件就能运行

shadowsocks分为服务器端和客户端，两边需要配置相符才能正常通信

配置文件格式参照(server端，需要在国外的VPS上配置)
```
{
"server":"::",
"server_port":8388,
"local_address":"0.0.0.0",
"local_port":1080,
"password":"xxxxxxxx",
"timeout":300,
"method":"aes-256-cfb"
}
```

服务器端则只需把server改为对应服务器的ip地址即可

### 启动

假设配置文件为同目录下的shadowsocks.json

首先启动服务器端
`ssserver -c shadowsocks.json`

然后启动本地端

本地段端根据系统平台可选择相应的软件连接，主流平台几乎都支持，配置的时候填入上面设置的对应参数即可

以Linux平台为例
`sslocal -c shadowsocks.json`

不出意外你就有了一个SOCKS5代理了

此时就可以直接设置浏览器的SOCKS5代理实现科学上网了

如果感觉光是浏览器科学上网意犹未竟，也可以使用proxifier等软件将它转成全局代理

若你的环境不支持SOCKS5代理，也可参考前文用privoxy把SOCKS5代理转为HTTP代理

惨无人道的是前段时间看到据说居然好像还可以用kcptun等技术实现网络加速？？？？试了一下效果不是特别明显，有兴趣的同学可以尝试一下

### softether
softether是日本筑波大学一个学生开发的VPN软件，功能十分强大（个人使用的话太浪费了，这里只是介绍用，感兴趣的可访问官方主页[https://www.softether.org/](https://www.softether.org/)查看详情）