# gout_project

### 1.项目介绍

该项目为**痛风图像分割系统**，技术栈为`python+vue+deep learning`

`front-end`为前端源码

`back-end`为后端源码

#### 系统功能模块图

![](./assets/系统功能模块图.png)

#### 系统架构图

![](./assets/系统架构图.png)

#### 系统用例图

![](./assets/系统用例图.png)

#### 系统主页面

![](./assets/系统主页面.png)

### 2.运行方法

预训练权重`checkpoint`下载链接为：https://drive.google.com/drive/folders/1SH0Q4VNbQGaTu8ryDdgf4fex8wurumUk?usp=sharing

数据库文件在项目sql文件夹中，`graduation_project.sql`

找到`back-end/DbConfig.py`，修改其中的`user`和`password`

```
conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='******',
        database='graduation_project'
    )
```

分别运行`front-end`和`back-end`即可



遇到问题可以留言

联系方式：1543001738@qq.com
