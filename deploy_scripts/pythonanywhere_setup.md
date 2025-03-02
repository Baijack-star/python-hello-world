# PythonAnywhere 部署指南

本文档介绍如何在PythonAnywhere上初始设置Flask应用并配置持续集成/持续部署(CI/CD)。

## 初始设置

### 1. 注册PythonAnywhere账号

1. 访问 [PythonAnywhere](https://www.pythonanywhere.com/) 并注册一个免费账号。
2. 完成注册后登录到控制面板。

### 2. 设置Web应用

1. 在PythonAnywhere控制面板中，点击"Web"选项卡。
2. 点击"Add a new web app"按钮。
3. 选择你的域名（免费账户将是`yourusername.pythonanywhere.com`）。
4. 选择"Manual configuration"（不选择Flask框架）。
5. 选择Python版本（推荐Python 3.9或更高版本）。

### 3. 创建GitHub个人访问令牌

由于GitHub不再支持密码认证，你需要创建个人访问令牌：

1. 登录到你的GitHub账户。
2. 点击右上角头像 -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic)。
3. 点击"Generate new token"，选择"Generate new token (classic)"。
4. 给令牌命名，例如"PythonAnywhere访问"。
5. 选择作用域（至少需要包含`repo`权限）。
6. 点击"Generate token"按钮。
7. **复制并保存生成的令牌！** 这是你唯一能看到它的机会。

### 4. 克隆仓库

1. 在PythonAnywhere控制面板中，点击"Consoles"选项卡。
2. 开启一个新的Bash控制台。
3. 使用个人访问令牌克隆你的GitHub仓库：

```bash
cd ~
# 使用以下格式替换URL中的用户名和仓库名
git clone https://YOUR_USERNAME:YOUR_PERSONAL_ACCESS_TOKEN@github.com/YOUR_USERNAME/python-hello-world.git
cd python-hello-world
pip3 install --user -r requirements.txt
```

#### 克隆仓库的另一种方法（如果你有SSH密钥）

如果你更喜欢使用SSH克隆仓库：

1. 在PythonAnywhere上生成SSH密钥：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
```

2. 将输出的公钥添加到你的GitHub账户（Settings -> SSH and GPG keys -> New SSH key）。

3. 使用SSH URL克隆仓库：
```bash
git clone git@github.com:YOUR_USERNAME/python-hello-world.git
```

### 5. 配置WSGI文件

1. 返回"Web"选项卡。
2. 点击WSGI配置文件链接（例如：`/var/www/yourusername_pythonanywhere_com_wsgi.py`）。
3. 将文件内容替换为以下代码：

```python
import sys
import os

# 添加应用目录到路径
path = '/home/yourusername/python-hello-world'
if path not in sys.path:
    sys.path.append(path)

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 导入应用
from app import app as application
```

4. 保存文件。

### 6. 配置静态文件

1. 在"Web"选项卡中，找到"Static files"部分。
2. 添加以下条目：
   - URL: `/static/`
   - Directory: `/home/yourusername/python-hello-world/static/`

### 7. 生成API令牌

1. 点击"Account"选项卡。
2. 找到"API token"部分，点击"Create new API token"按钮。
3. 复制生成的令牌，你将在GitHub Actions中使用它。

## 配置GitHub Actions

### 1. 设置GitHub Secrets

在GitHub仓库中，添加以下secrets：

1. 转到你的GitHub仓库 -> Settings -> Secrets and variables -> Actions
2. 添加以下repository secrets:
   - `PA_API_TOKEN`: PythonAnywhere API令牌
   - `PA_USERNAME`: PythonAnywhere用户名
   - `PA_DOMAIN`: （可选）你的PythonAnywhere域名，通常是 `yourusername.pythonanywhere.com`

### 2. 重新加载Web应用

首次配置完成后，回到PythonAnywhere的"Web"选项卡，点击"Reload"按钮启动你的应用。

## 访问你的应用

配置完成后，你可以通过 `https://yourusername.pythonanywhere.com/` 访问你的应用。

## 注意

- 免费账户每天有一定的CPU时间限制。
- 免费账户只能通过HTTPS访问。
- 做任何更改后，记得点击"Reload"按钮以应用更改。