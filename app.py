from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import json
from datetime import datetime
import uuid
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于session和flash消息

# 文件上传配置
UPLOAD_FOLDER = 'uploads'  # 相对于static目录
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
UPLOAD_PATH = os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
os.makedirs(UPLOAD_PATH, exist_ok=True)

# 博客文章存储路径
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'posts.json')

# 确保data目录存在
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# 如果文件不存在，创建一个空的博客文章列表
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# 检查允许的文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 读取博客文章
def get_posts():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# 保存博客文章
def save_posts(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

# 管理员登录验证装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('请先登录', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html', title='Python Web App')

@app.route('/about')
def about():
    return render_template('about.html', title='关于我们')

# 博客列表页面
@app.route('/blog')
def blog():
    posts = get_posts()
    return render_template('blog.html', title='博客', posts=posts)

# 博客文章详情页面
@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    posts = get_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return render_template('blog_detail.html', title=post['title'], post=post)
    return render_template('404.html', title='文章未找到'), 404

# 管理员登录页面
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 简单的用户验证，实际应用中应使用加密密码
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            flash('登录成功!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    return render_template('admin_login.html', title='管理员登录')

# 管理员登出
@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('已退出登录', 'info')
    return redirect(url_for('home'))

# 管理员控制面板
@app.route('/admin')
@admin_required
def admin_dashboard():
    posts = get_posts()
    return render_template('admin_dashboard.html', title='管理面板', posts=posts)

# 新增博客文章
@app.route('/admin/post/new', methods=['GET', 'POST'])
@admin_required
def admin_new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return render_template('admin_post_form.html', title='新建文章')
        
        posts = get_posts()
        new_id = 1 if not posts else max(post['id'] for post in posts) + 1
        
        # 处理图片上传
        image_path = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename != '' and allowed_file(image_file.filename):
                # 生成唯一的文件名防止冲突
                filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
                save_path = os.path.join(UPLOAD_PATH, filename)
                image_file.save(save_path)
                # 存储相对路径，用于模板中访问
                image_path = f"{UPLOAD_FOLDER}/{filename}"
        
        new_post = {
            'id': new_id,
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'image_path': image_path
        }
        
        posts.append(new_post)
        save_posts(posts)
        
        flash('文章创建成功!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin_post_form.html', title='新建文章')

# 编辑博客文章
@app.route('/admin/post/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(post_id):
    posts = get_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if not post:
        flash('文章不存在', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('标题和内容不能为空', 'error')
            return render_template('admin_post_form.html', title='编辑文章', post=post)
        
        # 处理图片上传
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename != '' and allowed_file(image_file.filename):
                # 如果原来有图片，删除旧图片文件
                if post.get('image_path'):
                    old_image_path = os.path.join(STATIC_FOLDER, post['image_path'])
                    if os.path.exists(old_image_path):
                        try:
                            os.remove(old_image_path)
                        except:
                            pass  # 如果删除失败，继续执行
                
                # 生成唯一的文件名防止冲突
                filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
                save_path = os.path.join(UPLOAD_PATH, filename)
                image_file.save(save_path)
                # 更新图片路径
                post['image_path'] = f"{UPLOAD_FOLDER}/{filename}"
        
        post['title'] = title
        post['content'] = content
        post['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        save_posts(posts)
        
        flash('文章更新成功!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin_post_form.html', title='编辑文章', post=post)

# 删除博客文章
@app.route('/admin/post/delete/<int:post_id>', methods=['POST'])
@admin_required
def admin_delete_post(post_id):
    posts = get_posts()
    post_to_delete = next((p for p in posts if p['id'] == post_id), None)
    
    if post_to_delete:
        # 如果文章有图片，删除图片文件
        if post_to_delete.get('image_path'):
            image_path = os.path.join(STATIC_FOLDER, post_to_delete['image_path'])
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass  # 如果删除失败，继续执行
        
        # 从列表中过滤掉要删除的文章
        filtered_posts = [p for p in posts if p['id'] != post_id]
        save_posts(filtered_posts)
        flash('文章删除成功!', 'success')
    else:
        flash('文章不存在', 'error')
        
    return redirect(url_for('admin_dashboard'))

# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='页面未找到'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
