from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase): #반드시 대문자 T로 시작해야함 (TestCase를 상속받음)

    def setUp(self):
        self.client = Client()
    def test_post_list(self):
        #self.assertEqual(3,3)
        response = self.client.get('/blog/')

        # response 결과가 정상적으로 출력되는지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')

        # navbar가 정상적으로 보이는지
        navbar = soup.nav
        #navbar라고 하는 변수에는 nav로 시작해서 nav로 끝나는 html문서의 일부가 들어감 (전체 html문서가 아니라)
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # post가 정상적으로 보이는지
        # 맨 처음엔 Post가 없음
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id="main-area")
        # id가 main-area인 div태그를 찾겠다
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 2. Post가 추가
        post_001 = Post.objects.create(title="첫번째 포스트", content = "첫번째 포스트 입니다.")
        post_002 = Post.objects.create(title="두번째 포스트", content = "두번째 포스트 입니다.")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/', follow = True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)