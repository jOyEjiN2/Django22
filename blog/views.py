from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#로그인 사용자가 글을 입력할 수 있도록
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

# Create your views here.

class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category'] #, 'tag'
    template_name = 'blog/post_update_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self,form):
        response = super(PostUpdate,self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tag_list = tags_str.split(';')
            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate,self).get_context_data()
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):  #CreateView,LoginRequiredMixin들을 상속받는다
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category'] # ,'tags'
    #모델명_form.html => 템플릿이 자동으로 호출

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
        #superuser인지 staff인지 보고 둘중 하나만 맞아도 됨

    # 이 폼이 올바른가
    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):  #true면 로그인된 인증된 유저인 것
            form.instance.author = current_user
            response = super(PostCreate,self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';')
                tag_list = tags_str.split(';')
                for t in tag_list :
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

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