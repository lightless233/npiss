# NPISS - New Private Image Storage Service

## 新版本新功能
NPISS(PISS 2.0)是一款私人图床工具，基于七牛SDK，可以快速搭建自己的私人图床系统。


## 安装
1. 复制piss/settings.py.example到piss/settings.py，并修改SECRET_KEY，DATABASE，MANAGE_TOKEN。同时根据需要选择是否开启DEBUG
2. 新建数据库piss
    ```mysql
    create database npiss charset utf8mb4
    ```
3. 安装依赖
    ``` bash
    yum install mysql-devel
    pip install -r requirements.txt
    ```
4. 建立数据表并运行
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
5. 使用supervisor进行守护（可选）
6. 使用nginx反代（可选）

## TODO
目前仍然处于开发过程中，进度较慢，敬请期待。
