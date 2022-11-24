from django.urls import path
from . import views

urlpatterns = [ #IP주소/blog/
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()), #게시물 수정
    path('category/<str:slug>/', views.category_page),  # IP주소/blog/category/slug/
    path('tag/<str:slug>/', views.tag_page),   # IP주소/blog/tag/slug/
    path('<int:pk>/new_comment/', views.new_comment), #댓글
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), #댓글 수정
    path('search/<str:q>/', views.PostSearch.as_view()), #검색어

    #path('',views.index), #IP주소/blog/ , 목록 페이지?  (추가하려면 뒤에 꼭 , 넣어야함)
    #path('<int:pk>/',views.single_post_page)  #int 숫자가 옴
]