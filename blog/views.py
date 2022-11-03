from django.shortcuts import render
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView

# Create your views here.

class PostList(ListView):
    model = Post  #model이라는 변수에 이용할 이름을 적어줌
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context
    # 템플릿은 모델명_list.html => post_list.html
    # blog.html을 post_list.html로 바꿔줌
    # 전달하는 매개변수 모델명_list : post_list

class PostDetail(DetailView):
    model = Post
    # 템플릿은 모델명_detail.html => post_detail.html
    # single_post_page.html을 post_detail.html로 바꿔줌
    # 매개변수 모델명 : post

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


def category_page(request,slug):
    if slug == 'no_cateogry':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request,'blog/post_list.html',{
        'category' : category,
        'post_list' : Post.objects.filter(category=category),
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })

def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    # 해당되는 tag값만 있는 POST만 전달해줌
    return render(request, 'blog/post_list.html',{
        'tag':tag,
        'post_list':post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })


#def index(request):      # all => 다가져오겠다
#    posts = Post.objects.all().order_by('-pk') #pk=primary key /-pk 거꾸로 정렬(최신 게시글 순서대로)
#    return render(request, 'blog/index.html',{'posts':posts})

#def single_post_page(request,pk):
#    post = Post.objects.get(pk=pk)
                        #get => 특정한 값을 가지고 오겠다
#    return render(request, 'blog/single_post_page.html', {'post':post})