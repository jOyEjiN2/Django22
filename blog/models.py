from django.db import models
import os

# Create your models here.
# model이 변경되면 migrations을 해야한다
#함수 추가할 경우에는 migration할 필요 없음 , Field가 추가될 때는 migration 해줘야함

class Post(models.Model): # post라고 하는 이름의 테이블을 만들겠다고 선언
    title = models.CharField(max_length=30)        # title이라고 하는 필드가 만들어짐, charfield 문자열 글자 수 제한, 최대 30글자까지
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
                                                                      #사진이 안채워져있어도 가능하도록
    # %Y 2022(네글자 연도), %y 22 (두글자 연도)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True) #첨부파일 업로드

    created_at = models.DateTimeField(auto_now_add=True)
                                      # 자동으로 시간에 대한 부분이 추가됨
    update_at= models.DateTimeField(auto_now=True)  #수정시간을 넣어줌


    # author 나중에 추가


    def __str__(self):
        return f'[{self.pk}]{self.title}  {self.created_at}' # 화면에 어떻게 출력되는지
                   # pk = primary key   타이틀   시간          순으로 포스트 제목 출력

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):    #함수 선언
        return os.path.basename(self.file_upload.name) #base이름은 빼고 파일 이름만 남게 함

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #a.text => a   text (.을 기준으로 나뉘어진다)
                                            # 제일 마지막에 해당되는 배열번호