### 安装

```shell

uv add django

```

### 创建django项目

```shell
django-admin startproject config .

# 这样就有了manage.py
```

### 启动

```shell

python manage.py runserver

```

### 计划

1. Django基础APP创建
2. RestFramework APP创建
3. 结合HTMX使用

#### 基础APP

```shell
(learn-django) wangjian@WJPC:~/py/learn-django$ python manage.py startapp users
...
 └ users
     ├ models.py
     ├ views.py
     ├ admin.py
     └ migrations
```

注册APP

```python
# config/settings.py

INSTALLED_APPS = [
    ...
    'users' 
]
```

```python
# models.py

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
```

数据库迁移：

Model
 ↓
Migration 生成ORM变更
 ↓
Database Table 生成SQL执行

```shell
(learn-django) wangjian@WJPC:~/py/learn-django$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying users.0001_initial... OK
```

注册到后台管理：

```python
from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)
```

    任何模块都有admin，django会统一扫描所有模块的admin并合并


创建超级用户：

```shell
python manage.py createsuperuser

```
本质是在 内置用户表 中创建一个管理员账号。

`Django` 内置了一个认证系统：

`django.contrib.auth`

它自带：

数据库表：
```txt
auth_user
auth_group
auth_permission
```
超级用户就是：
```
is_superuser = True
```
所以你就可以访问：
```
/admin
```
并管理所有数据。


访问：/admin
```
浏览器
 ↓
Django Admin
 ↓
登录认证
 ↓
auth_user 表
 ↓
权限检查
 ↓
后台管理页面
```
创建 View

users/views.py
```python
from django.shortcuts import render
from .models import User

def user_list(request):
    users = User.objects.all()
    return render(request, "users/list.html", {"users": users})
```
配置 URL

创建：

users/urls.py
```py
from django.urls import path
from .views import user_list

urlpatterns = [
    path("", user_list),
]
```

主路由：

config/urls.py
```py
from django.urls import path, include

urlpatterns = [
    path("users/", include("users.urls")),
]
```
创建模板

users/templates/users/list.html
```html
<h1>用户列表</h1>

<ul>
{% for user in users %}
<li>{{ user.username }} - {{ user.email }}</li>
{% endfor %}
</ul>
```
访问：
```shell
http://127.0.0.1:8000/users
```
#### Rest API

安装：
```shell
uv add djangorestframework
```
注册：
```
INSTALLED_APPS += ["rest_framework"]
```
1 创建 Serializer
```py
# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
```
2 创建 API View
```py
# users/api.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

@api_view(["GET"])
def user_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
```
3 API 路由
```py
# users/urls.py
from .api import user_list_api

urlpatterns = [
    path("", user_list),
    path("api/", user_list_api),
]
```

访问：
```shell
http://127.0.0.1:8000/users/api
```
返回：
```json
[
  {
    "id":1,
    "username":"tom",
    "email":"tom@test.com"
  }
]

```

#### HTMX

引入 HTMX。

模板添加：
```html
<script src="https://unpkg.com/htmx.org"></script>
```
1 创建搜索接口

views.py
```py
def user_search(request):
    keyword = request.GET.get("q", "")
    users = User.objects.filter(username__icontains=keyword)

    return render(request, "users/table.html", {"users": users})
```
2 表格模板
users/templates/users/table.html
```html
<table>
<tr>
<th>ID</th>
<th>用户名</th>
</tr>

{% for u in users %}
<tr>
<td>{{u.id}}</td>
<td>{{u.username}}</td>
</tr>
{% endfor %}
</table>
```
3 HTMX 搜索
list.html

```html

<input
    type="text"
    name="q"
    hx-get="/users/search"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#result"
/>

<div id="result"></div>
```
效果：
```
输入字符
   ↓
HTMX发送请求
   ↓
Django返回HTML片段
   ↓
局部更新表格
```