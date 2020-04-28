# 2.5 树莓派配置为路由器

树莓派3支持 wifi、网线，由于实验室网络环境，选择wifi
连接比较方便
做路由器至少需要双网卡，自带的接口为wlan0，自己加的usb无线网卡为wlan1，由于驱动问题用它创建无线AP没成功，因此用来联网
待会儿做的就是把wlan0作为无线热点，将wlan1连接的网络分享出去

打开终端，运行sudo apt-get update更新软件源（树莓派官方
操作系统是基于debian的raspbian）

## 安装相关软件

`sudo apt-get install hostapd udhcpd`

## 修改配置文件

### 配置hostapd

创建并编辑hostapd.conf文件
`sudo vi /etc/hostapd/hostapd.conf`

改为如下内容
```
interface=wlan0
hw_mode=g
channel=10
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=12345678
ssid=rPi3
```


然后指定配置文件位置
修改配置文件/etc/default/hostapd
`sudo vi  /etc/default/hostapd`
将
`#DAEMON_CONF=""`
改为
`DAEMON_CONF="/etc/hostapd/hostapd.conf"`

然后启动hostapd服务
`sudo service hostapd restart`
此时就可以在wifi列表里搜索到rPi3的热点了
但是因为DHCP、iptables等没配置好所以还不能上网

## 配置udhcpd（默认网段是192.168.0.0/24，这里不做修改）

`sudo vi /etc/udhcpd.conf`
更改下列选项（start end 选项是DHCP分配的ip范围）
```
start       192.168.0.20    #default: 192.168.0.20
end     192.168.0.254   #default: 192.168.0.254
interface wlan0 # The device uDHCP listens on.
remaining yes
opt dns 8.8.8.8 8.8.4.4 # The DNS servers client devices will use.
opt subnet 255.255.255.0
opt router 192.168.0.1 # The Pi's IP address on wlan0 which we will set up shortly.
```

然后还要修改/etc/default/udhcpd
`sudo vi /etc/default/udhcpd`
注释掉这一行
`#DHCPD_ENABLED="no"`
然后启动udhcpd服务
`sudo service udhcpd restart`

此时就可以通过DHCP获取到ip地址了


## 配置树莓派网络

`sudo vi /etc/network/interfaces`

将wlan0那段改为如下
```
allow-hotplug wlan0
iface wlan0 inet static
  address 192.168.0.1
  netmask 255.255.255.0
```

重启wlan0
```
sudo ifdown wlan0
sudo ifup wlan0
```

开启内核转发
`sudo vi /etc/sysctl.conf`
将`net.ipv4.ip_forward=1`取消注释
重新读入内核参数，使修改生效
`sudo sysctl -p`

## 设置iptables 转发规则

```
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
```

不出意外便大功告成~~~~

如需使它开机自动配置成路由器
只需确保hostapd 和 udhcpd 默认自动运行并将iptables规则写入配置文件即可

