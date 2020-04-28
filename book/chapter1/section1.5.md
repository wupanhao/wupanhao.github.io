# 1.5 树莓派音频基础

在Linux万物皆文件的哲学下，系统对硬件的访问也是通过文件提供的接口进行的，其中音频设备是经常和我们打交道的

树莓派本身有两个音频播放接口，hdmi和模拟音频信号，无音频录制（也就是麦克风）接口，如果需要，则需自己外接usb麦克风或通过usb声卡来另接音频设备

#### 查看音频设备
`arecord -l`列出录音设备
`aplay -l`列出音频播放设备

可通过用户家目录下的.asoundrc文件定义默认的录制和播放设备，主要需根据情况修改`pcm "hw:主设备号,次设备号",可用设备号可根据上面那两条命令查看，这样在使用aplay、mpg123等命令时就无需手动指定plughw等参数了

```
pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
  }
}
pcm.speaker {
  type plug
  slave {
    pcm "hw:0,0"

  }
}
```

#### 录音命令
`arecord  -d 5 -r 16000 -c 1 -t wav -f S16_LE record.wav`
-d duration，-r rate , -c channel ， -t type，-f format

### 文本转语音

#### espeak
`sudo apt-get install espeak`
测试

`espeak "hello world"`

`espeak -v zh "你好"`
默认的中文效果不是很好，还可以配置更多参数
`espeak -vzh -p 70 -a 150  -s 250 "为您播放"`

#### festival
`sudo apt-get install festival`
测试
`festival "hello world"`

#### 百度语音合成API
百度语音平台算是比较方便使用的一个语音平台了,前往[http://yuyin.baidu.com/](http://yuyin.baidu.com/)注册一个账号并创建一个应用就可以申请它的各种开放的API KEY了

其中语音合成接口最简单，通过你获得的语音合成的KEY，访问`https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=lb5xCu4TxlBR3b8gNCUoDhxh&client_secret=your_secret_key`,把your_secret_key替换成自己的即可

会返回一个json数组，记录下access_token的值，这就是我们请求语音合成API的凭据

接下来访问如下url就会得到语音内容
`url = "http://tsn.baidu.com/text2audio?tex="+tex+"&lan=zh&per="+per+"&pit="+pit+"&spd="+spd+"&cuid=***&ctp=1&tok="+tok`
说明: #tex是要合成的语音内容，per是声音的性别，1是男，0是女，默认是女，pit是音调，spd是语速，调节范围都是1-9，最后的tok是你通过你的id和key获取到的token
也可以通过mpg123播放网络音频流直接用命令行控制播放文本转语音的结果
`os.system('mpg123  "%s" ' %(url))`


更多可参考[https://github.com/wupanhao/Tutorials/issues/8](https://github.com/wupanhao/Tutorials/issues/8)


### 语音转文本



#### 百度语音识别API

语音识别涉及到音频文件的上传，而求要求音频文件符合一定的格式，所以略复杂一些，这里直接提供python脚本

```
#encoding=utf-8
 
import wave
import urllib, urllib2, pycurl
import base64
import json
## get access token by api key & secret key
## 获得token，需要填写你的apikey以及secretkey
def get_token():
    apiKey = "xxxxxxxxxx"
    secretKey = "xxxxxxxxxxxxxx"
 
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=\
    client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
 
    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']
 
def dump_res(buf):
    if json.loads(buf)['err_msg']=='success.':
        print("ok:" + json.loads(buf)['result'][0])
 
## post audio to server
def use_cloud(token):
    fp = wave.open('record.wav', 'rb')#录音文件名
    ##已经录好音的语音片段
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
 
    cuid = "8133661" #你的产品id
    base = 'http://vop.baidu.com/server_api'
    srv_url = base + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=16000',
        'Content-Length: %d' % f_len
    ]
 
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val
 
if __name__ == "__main__":
    token = get_token()
    #获得token
    #进行处理然后
    use_cloud(token)
```

其中record.wav文件可以通过下面这条命令录制
`arecord  -d 5 -r 16000 -c 1 -t wav -f S16_LE record.wav`



#### 科大讯飞SDK

科大是国内做得比较好的一家公司了，准确率比百度要高，但是接口不太方便使用，是C语言版的，还涉及到一些库的依赖，这里就不过多介绍了


## 语音唤醒（关键词检测）

用一句特定的话唤醒一项服务，我用过的snowboy做得还不错，写过一篇教程，传送门[https://github.com/wupanhao/Tutorials/issues/9](https://github.com/wupanhao/Tutorials/issues/9)