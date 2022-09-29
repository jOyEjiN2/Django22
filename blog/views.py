from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'
    # 템플릿은 모델명_list.html => post_list.html
    #blog.html을 post_list.html로 바꿔줌

class PostDetail(DetailView):
    model = Post
    #템플릿은 모델명_detail.html => post_detail.html
    #single_post_page.html을 post_detail.html로 바꿔줌



#def index(request):      # all => 다가져오겠다
#    posts = Post.objects.all().order_by('-pk') #pk=primary key /-pk 거꾸로 정렬(최신 게시글 순서대로)
#    return render(request, 'blog/index.html',{'posts':posts})

#def single_post_page(request,pk):
#    post = Post.objects.get(pk=pk)
                        #get => 특정한 값을 가지고 오겠다
#    return render(request, 'blog/single_post_page.html', {'post':post})