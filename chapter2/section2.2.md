# 2.2 freeradius认证服务器配置

## 准备工作
环境：Ubuntu16.04

## 一、安装相关软件
```
sudo apt-get install freeradius freeradius-mysql
```


## 二、修改配置文件
修改/etc/freeradius/radius.conf
取消$INCLUDE sql.conf这一行的注释以启用sql
修改/etc/freeradius/clients.conf以配置连接的客户端的相关参数，主要为ip和密钥
可简单将client localhost里的  ipaddr改为我们需要连接freeradius服务器进行认证的客户端的地址，比如softease服务器的地址。（测试时可不用更改以方便本地使用radtest）
    secret  的值默认为testing123
修改/etc/freeradius/sql.conf以配置数据库链接
比如
```
    server = "10.10.10.105"
    port = 3306
    login = "radserver"
    password = "123123"
    radius_db = "radius"
```

最后修改\etc\freeradius\sites-enabled\default
将所有sql有关的注释去掉，而sql_log的注释保留，否则运行会报错
注意要确保数据库中freeradius需要的数据表和相关字段，且具有数据库的访问权限

## 三、测试
配置完成之后，可以重启freeradius服务
```
sudo service freeradius stop
```

通过```sudo freerasdius -X```启用调试
若看到Ready to processrequests.则说明启动成功，此时可以在softease服务器上配置指向本机freeradius认证

若无意外，当有用户开始认证的时候，终端会有标准输出显示认证情况

