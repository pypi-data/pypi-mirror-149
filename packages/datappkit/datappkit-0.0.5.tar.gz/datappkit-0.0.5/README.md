# datappkit

## 简介

datappkit 是一个对数据操作的SDK，为接入方提供对标注和统计等平台沟通的接口

## 安装

普通用户安装：

``` shell
pip install datappkit
```

开发者：

``` shell
git clone git@git-core.megvii-inc.com:brain/label/infrastructure/data-service-sdk.git
cd data-service-sdk
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 使用

Debug模式
```
执行export DATAPP_KIT_DEBUG=on 可开启测试环境，所有接口会打到平台的dev环境
```

代码调用
```python
from datappkit.datapp import Datapp

datapp = Datapp()
datapp.login("account", "pwd")
datapp.get_requirement(1079)
# 其他功能见datapp模块提供的注释 或接口文档：https://wiki.megvii-inc.com/pages/viewpage.action?pageId=346934255
```

## 工程结构：
```
.
├── README.md
├── datappkit #核心代码包
│   ├── __init__.py
│   ├── common #通用基础包
│   │   ├── __init__.py
│   │   └── quota_manager.py #配额管理
│   │   └── ...
│   ├── controller #控制层，接收事件并转发给service
│   │   ├── __init__.py
│   │   └── requirement_controller.py
│   │   └── ...
│   ├── datapp.py #SDK唯一入口，接收事件并转发给响应业务的controller
│   ├── services #核心业务包
│   │   ├── __init__.py
│   │   └── requirement_service.py
│   │   └── ...
│   ├── utils #工具包
│   │   └── __init__.py
│   │   └── ...
│   └── version.py #版本信息
├── docs #包的参考文档
│   └── conf.py
│   └── ...
├── main.py
├── requirements.txt #开发依赖
├── setup.py #打包和发布管理模块
├── tests
│   ├── __init__.py
│   └── test_basic.py
│   └── ...
└── venv
```