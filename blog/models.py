from django.db import models

# Create your models here.
class Post(models.Model): # post라고 하는 이름의 테이블을 만들겠다고 선언
    title = models.CharField(max_length=30)        # title이라고 하는 필드가 만들어짐, charfield 문자열, 최대 30글자까지
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
                                      # 자동으로 시간에 대한 부분이 추가됨
    update_at= models.DateTimeField(auto_now=True)  #수정시간을 넣어줌


    # author 나중에 추가

    def __str__(self):
        return f'[{self.pk}]{self.title}  {self.created_at}' # 화면에 어떻게 출력되는지
                   # pk = primary key   타이틀   시간          순으로 포스트 제목 출력

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'