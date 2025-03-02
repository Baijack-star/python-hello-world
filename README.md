# Python Web 应用示例

[![Python Flask CI/CD Pipeline](https://github.com/[您的用户名]/python-hello-world/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/[您的用户名]/python-hello-world/actions/workflows/ci-cd.yml)

这是一个使用Flask框架创建的简单Web应用示例。

## 功能介绍

- 主页展示
- 关于页面
- 博客系统
- 管理后台
- 响应式设计

## 安装与运行

### 前提条件

- Python 3.7+
- pip

### 安装步骤

1. 克隆此仓库
```bash
git clone https://github.com/[您的用户名]/python-hello-world.git
cd python-hello-world
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
python app.py
```

4. 在浏览器中访问 `http://localhost:5000`

## CI/CD流程

本项目配置了自动化CI/CD流程：

1. 当提交代码到main或master分支时，会自动触发GitHub Actions
2. 执行代码测试和语法检查
3. 测试通过后，自动部署到PythonAnywhere
