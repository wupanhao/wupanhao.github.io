# 2.3 freeradius数据库配置(mariadb版)

由于MySQL 被收购，而且某些支持不太完善，因此改用mariadb作为项目用数据库

## 准备工作
环境：Ubuntu16.04

## 安装：
```
apt-get install mariadb-server
```


## 修改配置文件
默认配置mariadb只能本地访问，因此需要修改一下配置文件

编辑/etc/mysql/mariadb.conf.d/50-server.cnf 

注释掉下面这两行

```
[mysqld]
    ...
    #skip-networking    #告诉MariaDB (or MySQL) 禁用 TCP/IP 连接。实际测试不注释这行也可以
    ...
    #bind-address = <some ip-address>   
    #默认绑定本地回环，也可改为公网ip或0.0.0.0，0.0.0.0等同于注释掉
    ...
```
重启mariadb 即可实现远程访问(service mysql restart)，但数据库权限还没有设置

使用mysql登陆mariadb，执行以下语句
```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'host'IDENTIFIED BY '123456';
```
主机地址、用户名和密码可根据情况更改
### 说明
其中主机地址
% => 任意主机
172.17.0.% => 172.17.0.0/24

也可加WITH GRANT OPTION 表示允许该账号把自己有的权限再授权给别的用户

### 建立相关数据表

接下来及建立freeradius所需的数据表，已导出到radius.sql文件里，直接用```mysql radius < radius.sql```语句导入即可（需要先建立radius数据库，数据库名可任意但freeradius相关配置项需与此处一致），默认带有一个账号,用户名guokai，密码123456，可用此账号测试是否配置成功

用法，在配置好freeradius服务器的机器上以root身份运行```freeradius -X```，再执行
```
radtest guokai 123456 127.0.0.1 100 testing123
```

若返回Access-Accept即说明配置成功
