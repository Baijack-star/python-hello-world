import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_home_page(self):
        """测试首页是否可以正常访问"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_page(self):
        """测试关于页面是否可以访问"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
    
    def test_blog_page(self):
        """测试博客页面是否可以访问"""
        response = self.client.get('/blog')
        self.assertEqual(response.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()