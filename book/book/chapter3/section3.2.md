# 3.2 文件服务器

常用的文件服务器有samba、ftp等

## samba文件服务器

### 安装
`sudo apt-get install samba`

### 配置

在/etc/samba/smb.conf末尾添加如下段落，一段代表一个共享目录

```
[白鸽网络部]
        path=/media/pi/Linux/网络部
        writable=yes
        public=no

        #可选配置项，@代表用户组，不加代表用户,可用逗号隔开
        valid users=@wangluobu 
```

若启用用户认证,需先添加对应本地用户,再用`smbpasswd -a username`设置samba服务器的密码，还需确保对应用户有该目录的相关权限

## ftp文件服务器
比较受欢迎的是vsftpd
### 安装
`sudo apt-get install vsftpd`

### 配置
配置文件在/etc/vsftpd.conf，找到如下选项


```
pam_service_name=vsftp # 默认会使用pam模块进行认证，需要配置/etc/pam.d/vsftpd和/etc/ftpusers相关选项
```

若想默认本地用户就可登陆ftp

查看/etc/pam.d/vsftpd
```
# Standard behaviour for ftpd(8).
auth    required    pam_listfile.so item=user sense=deny file=/etc/ftpusers onerr=succeed

# Note: vsftpd handles anonymous logins on its own. Do not enable pam_ftp.so.

# Standard pam includes
@include common-account
@include common-session
@include common-auth
auth    required    pam_shells.so
```

可知，两段auth选项说明需要配置用户的登陆shell，并且此shell需要是/etc/shells列出来的之一，/etc/ftpusers里记录了禁止登录的名单

可简单编辑/etc/passwd文件设置用户的登录shell，并确保用户不在/etc/ftpusers中


否则可修改pam_service_name=ftp来禁用pam模块，或是编辑/etc/pam.d/vsftpd，注释掉`auth    required    pam_shells.so`选项


## nfs文件服务器

nfs是Linux下常用的文件共享系统

#### 安装
`sudo apt-get install nfs`

需要按照如下格式写配置文件/etc/exports
```
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
```

比如我的就是`/media/pi/Linux/  *(rw,sync,no_root_squash,no_subtree_check)`