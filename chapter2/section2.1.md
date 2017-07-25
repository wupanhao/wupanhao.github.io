# 2.1 bind9智能dns解析配置指南

bind9 是著名的开源dns服务器，功能十分强大，这里主要想用于实现在不同的地方请求同一个域名，得到不同的解析结果

## 准备工作
环境：Ubuntu16.04

## 一、安装相关软件

```
sudo apt-get install bind9
```

## 二、修改配置文件

查看/etc/bind目录，发现主要有以下几个文件
/etc/bind/named.conf
/etc/bind/named.conf.options
/etc/bind/named.conf.local
/etc/bind/named.conf.default-zones

查看配置文件可以发现实际上是named.conf把另外三个配置文件包含了进来

我们可以直接更改named.conf.local，这默认是一个没有任何配置项的文件，在文末添加如下内容

```
acl trusted {  localhost; };
acl guest   { 10.10.10.0/24; };//如果用户不在acl域对应的ip范围里会出现查询不到的情况，因此若要投入使用必须保证包含所有ip地址

view trusted {
    match-clients { trusted; };

    allow-recursion { any; };

    zone "myzone.example" {
        type master;
        file "trusted/db.myzone.example";//最新测试相对路径无效，改用绝对路径/etc/bind/trusted/db.myzone.example才成功
    };
    zone "7.168.192.in-addr.arpa" {  //反向解析，也可以不要
        type master;
        file "trusted/db.192.168.7";
    };
};

view guest {
    match-clients { guest; };

    allow-recursion { any; };

    zone "myzone.example" {
        type master;
        file "guest/db.myzone.example";//最新测试相对路径无效，改用绝对路径/etc/bind/guest/db.myzone.example才成功
    };
};
```

这段内容声明了两个acl域，分别是localhost与10.10.10.0/24局域网段，并用两个view来针对这两个网段对同一个域myzone.example进行不同的解析，解析文件分别是自定义的trusted/db.myzone.example和guest/db.myzone.example

guest/db.myzone.example内容如下
```
$TTL    604800
@   IN  SOA myzone.example. root.myzone.example. (
                  2     ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
    IN  NS  ns
@   IN  A   192.168.1.1
@   IN  AAAA    ::1
www IN  A   172.16.1.2
ns  IN  A   127.0.0.1
```

trusted/db.myzone.example内容如下

```
$TTL    604800
@   IN  SOA myzone.example. root.myzone.example. (
                  2     ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
    IN  NS  ns
@   IN  A   192.168.1.1
@   IN  AAAA    ::1
www IN  A   192.168.1.3
ns  IN  A   127.0.0.1
```

因为启用了view，所有的zone必须放在view里面，配置文件/etc/bind/named.conf里对/etc/bind/named.conf.default-zones的包含就需要注释掉，否则检查不通过，通过添加双斜杠注释掉
更改为如下
```
include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
//include "/etc/bind/named.conf.default-zones";
```

最后确认一下配置有无错误
用```named-checkconf```检查配置文件格式
执行```named-checkzone myzone.example /etc/bind/trusted/db.myzone.example```
和```named-checkzone myzone.example /etc/bind/guest/db.myzone.example```

检查zone文件格式是否正确

若无报错，则说明zone文件语法正确

重启bind9服务测试效果```sudo service bind9 restart```

zone文件格式无误还不能保证bind9正常加载zone文件，还应运行service bind9 status 检查配置文件是否被正常加载

## 三、测试
在本机上，执行```dig @127.0.0.1  www.myzone.example``` 查询到ip为trusted/db.myzone.example里的192.168.1.3
在局域网的另一台机器上，修改dns服务器为这台机器的局域网ip，ping www.myzone.example ，得到的是guest/db.myzone.example 里的172.16.1.2

说明配置成功，接下来便可根据不同区域的ip划分不同的acl组来实现dns的智能解析

## 四、番外


### 检测主机的可用性
为保证dns的高可用性，需要检测自己解析的每一台主机是否正常工作


#### 使用shell script
这正是Linux的强项，一份shell script足以胜任这份工作


```
#!/bin/bash
server_list="1.1.1.1 2.2.2.2 3.3.3.3 4.4.4.4"

for i in $server_list
    do
    echo "nc -z -w 5 $i 443"
    nc -z -w 5 $i 443
    if [ $? -eq 0 ];then
        echo "server $i is on \n"
        sed -i "/$i/s/^;//" /etc/bind/db.schonet.*
    else
        echo "server $i is off \n"
        sed -i "/$i/s/^;//" /etc/bind/db.schonet.*
        sed -i "/$i/s/^/;/" /etc/bind/db.schonet.*
    fi
    done
    service bind9 restart
```


简要说明,利用sed命令去匹配配置文件下有对应ip的解析记录，根据nc的结果决定该取消还是启用该条解析记录,可定期运行该脚本更新解析纪录

#### 根据server.list文件自动生成配置文件

每次服务器变动都要手动修改配置文件，而且很容易写错，于是利用python读取服务器ip信息自动生成解析记录，只需维护一份server.list文件

server.list文件


```
@bnu
1.1.1.1
2.2.2.2

@china
1.2.3.4
5.6.7.8

@other
1.1.1.1
2.2.2.2
```


python文件代码如下

```
with open("server.list","r") as fin, open("/etc/bind/db.schonet.other",'w') as fout:
    base = '''$TTL    600
@   IN  SOA schonet.cn. root.schonet.cn. (
                  2     ; Serial
                  1H    ; Refresh
                  5M    ; Retry
                  1W    ; Expire
                  10M ) ; Negative Cache TTL
;
    IN  NS  ns
@   IN  A   127.0.0.1
@   IN  AAAA    ::1
www IN  A   219.143.237.175
ns  IN  A   120.25.101.88
'''
    fout.write(base)
    zones = fin.read().split('@')
    for i in zones[1:]:
        print('-'+i)
        zone = i.split()
        print(zone[0])
        for ip in zone[1:]:
            fout.write(zone[0].ljust(15)+'IN  A    '+ip+'\n')
            print('+'+ip)
```


运行这份脚本，将根据server.list文件,生成bnu.schonet.cn、china.schonet.cn等的解析记录
