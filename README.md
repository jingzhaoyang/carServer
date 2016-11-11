# 树莓派WIFI遥控小车服务端

## 部署环境

* Raspbin 8.0以上版本

* Python 2.7版本


## 安装

安装pip工具，然后使用pip安装所需的依赖库。

```
sudo apt-get install python-dev python-pip python-opencv redis-server
sudo pip install tornado json

```

## 启动

首先要启动redis服务
```
sudo systemctl start redis
```

启动到前台，用于调试

```
sudo python robot.py
```

启动到后台

```
sudo nohup python robot.py 2>&1 >/dev/null &
```

## 配置

* 修改web服务监听端口

默认web监听端口是`8000`，若要修改端口编辑`robot.py`文件

```
tornado.options.define("port",default=8000,type=int)
```
将`default`改为想要的端口

* 修改GPIO针脚

将`robot.py`内的针脚号，改为自己的。

```
IN1 = 11
IN2 = 12
IN3 = 16
IN4 = 18
```

## 控制

使用浏览器访问ip:port，然后通过`w`、`s`、`a`、`d`，四个键盘的按键控制小车前进后退。也可以用鼠标点击按钮来控制，按下按钮开始启动，松开按钮小车停止移动。

## 重要更新记录

* 2016年11月11日 添加远程视频支持

## 参考文档

[RPIO库官方文档](https://pythonhosted.org/RPIO/)

[Sunny博客-树莓派小车之按键控制](http://www.sunnyos.com/article-show-56.html)

## 联系我们

* QQ群 ： 536720498
