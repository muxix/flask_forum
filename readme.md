# 基于 Flask 框架的仿 CNode 论坛
## 目录
  - [项目地址](#项目地址)
  - [测试账号](#测试账号)
  - [项目简介](#项目简介)
  - [项目部署](#项目部署)
  - [项目功能演示](#项目功能演示)
## 项目地址
<http://134.175.32.136>

[[回到目录]](#目录)

## 测试账号
用户名：test  密码：123

[[回到目录]](#目录)

## 项目简介
  - 本项目是基于 Flask 框架的论坛：
    - 数据库使用 MySQL，实现了基于 SQLAlchemy 的 ORM；
    - 利用 Jinja2 的模板继承功能，复用通用页面元素；
    - 使用 Nginx 反向代理、并缓存静态资源，使用 Supervisor 进行进程管理，通过配置多 worker 和 gevent 协程的 Gunicorn 实现程序的负载均衡运行；
    - 使用 Shell 脚本实现一键部署。
    - 实现用户管理与论坛基础功能，包括：
      - 用户注册、登录、个人主页、修改密码、上传头像；
      - 板块分区、发布话题、评论、私信、@；
      - 支持 Markdown 语法和代码高亮。

[[回到目录]](#目录)

## 项目部署
```bash
bash deploy.sh
```
  - 使用前请自行建立 database_secret.conf 及 secret.py 文件，以配置 MySQL 和 Flask
```
# database_secret.conf 内容
mysql-server mysql-server/root_password password your_password
mysql-server mysql-server/root_password_again password your_password

# secret.py 内容
database_password = 'your_password'
flask_session_secret_key = 'your_password'
```
[[回到目录]](#目录)

## 项目功能演示
  - 用户登录

[[回到目录]](#目录)

![forum1_login](/readme_gif/forum1_login.gif)

  - 用户修改密码

[[回到目录]](#目录)

![forum2_pw](/readme_gif/forum2_pw.gif)

  - 用户上传头像

[[回到目录]](#目录)

![forum3_avatar](/readme_gif/forum3_avatar.gif)

  - 切换板块分区、发布话题与评论

[[回到目录]](#目录)

![forum4_topic](/readme_gif/forum4_topic.gif)

  - 私信

[[回到目录]](#目录)

![forum5_message](/readme_gif/forum5_message.gif)

  - @

[[回到目录]](#目录)

![forum6_at](/readme_gif/forum6_at.gif)
