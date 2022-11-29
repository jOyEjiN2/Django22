from django.db import models
from django.contrib.auth.models import User  # 이미 선언된 유저클래스 사용 가능
import os

# Create your models here.
# model이 변경되면 migrations을 해야한다
#함수 추가할 경우에는 migration할 필요 없음 , Field가 추가될 때는 migration 해줘야함

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

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


    # author 나중에 추가 => 10/20일 추가
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 데이터베이스가 바뀌었으니 make migration 해야함
    # CASCADE => 동시에 지워짐 (user가 지워지면 포스트도 지워짐)
    # SET_NULL => 포스트는 남겨짐
    # makemigration 실행

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
                 # 다대다 관계

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author} :  {self.created_at}' # 화면에 어떻게 출력되는지
                   # pk = primary key   타이틀  (author추가) 시간          순으로 포스트 제목 출력

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):    #함수 선언
        return os.path.basename(self.file_upload.name) #base이름은 빼고 파일 이름만 남게 함

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #a.text => a   text (.을 기준으로 나뉘어진다)
                                            # 제일 마지막에 해당되는 배열번호

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # on_delete =>사용자가 지워지면 댓글도 지워지도록
    #다대일 FOREIGN 다대다 manytomany?
    author = models.ForeignKey(User, on_delete=models.CASCADE) #댓글다는 사람 정보, 여러개의 댓글 달 수 있음
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True) #댓글 수정

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'