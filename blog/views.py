from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request):      # all => 다가져오겠다
    posts = Post.objects.all().order_by('-pk') #pk=primary key /-pk 거꾸로 정렬(최신 게시글 순서대로)
    return render(request, 'blog/index.html',{'posts':posts})

def single_post_page(request,pk):
    post = Post.objects.get(pk=pk)
                        #get => 특정한 값을 가지고 오겠다
    return render(request, 'blog/single_post_page.html', {'post':post})