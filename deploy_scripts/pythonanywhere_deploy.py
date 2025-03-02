import os
import requests
import sys

def deploy_to_pythonanywhere():
    """
    将应用部署到PythonAnywhere
    需要环境变量：
    - PA_API_TOKEN: PythonAnywhere API令牌
    - PA_USERNAME: PythonAnywhere用户名
    - PA_DOMAIN: 应用域名（通常是 {username}.pythonanywhere.com）
    """
    print("开始部署到PythonAnywhere...")
    
    # 获取环境变量
    api_token = os.environ.get('PA_API_TOKEN')
    username = os.environ.get('PA_USERNAME')
    domain = os.environ.get('PA_DOMAIN')
    
    if not api_token or not username:
        raise ValueError("缺少环境变量：PA_API_TOKEN 或 PA_USERNAME")
    
    if not domain:
        domain = f"{username}.pythonanywhere.com"
    
    # API基本URL和头部
    base_url = f"https://www.pythonanywhere.com/api/v0/user/{username}/"
    headers = {'Authorization': f'Token {api_token}'}
    
    try:
        # 1. 执行git pull命令（需要预先在PythonAnywhere上克隆仓库）
        print("执行git pull...")
        response = requests.post(
            f"{base_url}consoles/",
            headers=headers,
            json={"executable": "bash", "arguments": "-c 'cd /home/{}/python-hello-world && git pull'".format(username)}
        )
        
        if response.status_code != 201:
            print(f"git pull失败：{response.text}")
            return False
        
        console_id = response.json().get('id')
        print(f"git pull任务已启动，console_id: {console_id}")
        
        # 2. 安装/更新依赖
        print("安装依赖...")
        response = requests.post(
            f"{base_url}consoles/",
            headers=headers,
            json={"executable": "bash", "arguments": "-c 'cd /home/{}/python-hello-world && pip install -r requirements.txt'".format(username)}
        )
        
        if response.status_code != 201:
            print(f"安装依赖失败：{response.text}")
            return False
        
        # 3. 重新加载应用（使用PythonAnywhere API）
        print("重新加载Web应用...")
        response = requests.post(
            f"{base_url}webapps/{domain}/reload/",
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"部署成功！应用网址：https://{domain}/")
            return True
        else:
            print(f"重新加载Web应用失败：{response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print(f"部署失败：{str(e)}")
        return False

if __name__ == "__main__":
    success = deploy_to_pythonanywhere()
    if not success:
        sys.exit(1)