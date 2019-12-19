#### 一、部署项目: flask-demo-service
注：
本项目中的ip地址统一替换为了192.168.1.8，按需求替换为需要的ip地址
##### 1. 创建项目

修改示总项目名称为：`flask-demo-service`

将`gunicorn_config.py`文件里的项目名字修改成： `flask-demo-service`

```python
import multiprocessing

timeout = 30
workers = 2 * multiprocessing.cpu_count() + 1
bind = 'unix:flask-demo-service.sock'
umask = 0x7
loglevel = 'info'
pidfile = '/var/run/flask-demo-service.pid'
accesslog = '/var/log/flask-demo-service/access.log'
errorlog = '/var/log/flask-demo-service/error.log'

```

新建日志目录

```shell
$ mkdir /var/log/flask-demo-service
```



##### 2. 配置环境

将项目`flask-demo-service`文件夹clone到`/opt/app/`目录下：

进入目录`/opt/app/flask-demo-service`

安装虚拟环境：

```python
$ python3.7 -m venv venv  

$ . venv/bin/activate

$ python -m pip install --upgrade pip  //使用python3.6时候pip版本对应不上出错时候使用

$ pip install -r requirements.txt
```

 

##### 3. 新建服务文件：`flask-demo-service.service`

目的：用来启动服务，通过systemd的服务启动方式来启动服务

```shell
$ vi /etc/systemd/system/flask-demo-service.service 
```

内容：

```python
[Unit]
Description=Gunicorn instance to serve flask-demo-service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/app/flask-demo-service
EnvironmentFile=/etc/default/flask-demo-service
ExecStart=/opt/app/flask-demo-service/venv/bin/gunicorn -c /opt/app/flask-demo-service/gunicorn_config.py manage:app
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
Restart=on-failure
RestartSec=300s

[Install]
WantedBy=multi-user.target
```

配置解释：

` [Service] `:  需要指定如下配置信息，其它参数可选

`WorkingDirectory`:  项目所在路径

`EnvironmentFile`:  环境变量配置所在的路径，与项目里的.env文件里的内容一样, 接下来新建这个文件

`ExecStart`:  项目启动脚本



##### 4. 新建隐私环境变量文件：`flask-demo-service`

配置参考->`192.168.1.1`服务器里的文件：`/etc/default/flask-demo-service`

```shell
$ vi /etc/default/flask-demo-service
```

内容：

```python
FLASK_CONFIG = 'testing'
SECRET_KEY=b')\xf19\axaa\xda:\x9f:d\xfb\x86\xb3\xe9W\xe7Du'
MONGO_JD_ALI_URI='mongodb://root:192.168.1.1:3717'
MYSQL_DATABASE_URI =  {'host':'192.168.1.1', 'user':'mongo_user', 'passwd':'mongo_user', 'db':'company', 'port':3306}
MYSQL_DATABASE_OUT_URI =  {'host':'192.168.1.1', 'user':'mongo_user', 'passwd':'mongo_user', 'db':'company', 'port':3306}
```


##### 5. flask启动服务

启动服务: 启动成功后服务路径下回生成一个`flask-demo-service.sock`文件，用于`nginx`和此`gunicorn`沟通

```shell
$ systemctl start flask-demo-service.service
```

查看服务状态

```shell
$ systemctl status flask-demo-service.service
```

启动成功后，显示如下：

```
● flask-demo-service.service - Gunicorn instance to serve flask-demo-service
   Loaded: loaded (/etc/systemd/system/flask-demo-service.service; disabled; vendor preset: enabled)
   Active: active (running) since Fri 2019-12-13 09:19:54 CST; 1h 41min ago
  Process: 18893 ExecStop=/bin/kill -s TERM $MAINPID (code=exited, status=0/SUCCESS)
 Main PID: 18898 (gunicorn)
    Tasks: 11
   Memory: 181.2M
      CPU: 6.605s
   CGroup: /system.slice/flask-demo-service.service
```

重启服务

```shell
$ systemctl restart flask-demo-service.service
```

停止服务

```shell
$ systemctl stop flask-demo-service.service
```

设置开机自启动

```shell
$ systemctl enable flask-demo-service.service
```



##### 6. 新建nginx配置文件：`flask-demo-service`

备注：这是配置`http服务器`nginx监听`应用服务器`gunicorn，它们之间通过socket进行通信

```shell
 $ vi /etc/nginx/sites-available/flask-demo-service
```

内容：

```python
server {
	listen 5008;
	server_name 192.168.1.1;
    
	gzip on;
	access_log /var/log/nginx/flask-demo-service-access.log;
	error_log /var/log/nginx/flask-demo-service-error.log error;
    
	location / {
		include proxy_params;
		proxy_pass http://unix:/opt/app/flask-demo-service/flask-demo-service.sock;
	}
}
```

配置解释：

`listen`：指定该服务端口

`server_name`：监听地址/非必选项

`proxy_pass`：将接受到的请求转发给这个socket

 

##### 7. 创建软连接，启动nginx服务

创建软链接

```shell
$ ln -s /etc/nginx/sites-available/flask-demo-service /etc/nginx/sites-enabled/
```

检查新增加的nginx配置文件语法有没有问题：

```sh
$ nginx -t
```

配置成功显示如下：

```shell
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

重启`nginx`

```shell
$ nginx -s reload
```

查看服务是否搭建成功

```shell
$ netstat -tulp | grep 5010
```

若出现无权限反响代理socket，检查`nginx`的配置：`vi /etc/nginx/nginx.conf`

将第一行的`user nginx;`改成`user root;`



#### 二、增加接口

在目录`app/api/__init__.py`里面增加接口的路由，例如：

```python
from .info.resources import HelloWorld

# 给资源类HelloWorld绑定一个私有路由
api.add_resource(HelloWorld, '/index')
```

根据

```python
# 这个是指所有的接口前面的路由都加一个/api/
bp = Blueprint('api', __name__, url_prefix='/api')
```

所以新增加的这个请求接口为：`http//ip:port/api/index`

具体的定义类与函数则在`app/api/info/resources.py`的文件里定义

```python
class HelloWorld(Resource):
    # 定义了一个get请求
    def get(self):
        return "get: hello world"
    def post(self):
        return "post: hello world"
```



#### 三、连接数据库

`mongo_util.py`文件里定义`mongodb`连接与关闭的类

```python
class MongoJDAli(MongoBase):
    def __init__(self):
        # MONGO_JD_ALI_URI是current_app里的环境变量，其所有的字母必须大写
        uri = current_app.config['MONGO_JD_ALI_URI']
        super().__init__(uri)
```

在`config.py`文件里，给环境变量`MONGO_JD_ALI_URI`添加获取源头，每个Config类里都要配置

```python
MONGO_JD_ALI_URI = os.getenv('MONGO_JD_ALI_URI_UAT')
```

在`.env`文件里，给环境变量`MONGO_JD_ALI_URI_UAT`添加获取源头

```python
MONGO_JD_ALI_URI_UAT='mongodb://root:192.168.1.8:3717'
```

在调用出初始化这个类

```python
client = MongoJDAli().client()
addr_lng_lat = client.jd_combine.addr_lng_lat
```

最后记得关闭这个连接

```python
client.close()
```



#### 框架介绍

1. 文件夹介绍

   `/flask-demo-service/app/`

   里面是这个项目的总体版本文件，也可以命名为app_1_0

   `/flask-demo-service/app/api/`

   接口文件夹，里面是放的各个小项目的接口

   `/flask-demo-service/app/api/associate/`

   这个是服务里的一个`单独的小项目`的接口文件夹

   `/flask-demo-service/app/api/associate/resources/`

   小项目里的具体接口文件夹，里面每个文件都是一个具体的接口

   `/flask-demo-service/app/utils/`

   工具文件夹，里面放的是总项目统一使用的工具

2. 文件介绍

   `/flask-demo-service/app/api/associate/parsers.py`

   里面是处理请求参数的实例化对象，介绍请求的时候，根据特定的实例化参数导入特定的实例化对象，来处理请求里的参数

   `/flask-demo-service/app/api/__init__.py`

   里面是初始化各个接口的路由，将介绍参数请求的类名称导入到这里，为这个类定义对应的路由

   `/flask-demo-service/app/api/authentication.py`

   验证密码，暂时不用

   `/flask-demo-service/app/api/decorators.py`

   验证许可，暂时不用

   `/flask-demo-service/app/api/errors.py`

   报错汇总

   `/flask-demo-service/app/__init__.py`

   初始化app

   `/flask-demo-service/.env`

   里面放的是初始化的私有环境变量，不上传到gitlab上，该文件在线下调试的时候使用，在线上使用/etc/default/flask-demo-service文件

   `/flask-demo-service/.flaskenv`

   `/flask-demo-service/config.py`

   不同环境的不同配置类

   `/flask-demo-service/gunicorn_config.py`

   gunicorn服务器的配置参数，日志，性能，转发方式等

   `/flask-demo-service/manage.py`

   主文件夹，项目的初始化文件

   



































