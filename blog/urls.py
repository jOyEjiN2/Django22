from django.urls import path
from . import views

urlpatterns = [ #IP주소/blog/
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view())
    #path('',views.index), #IP주소/blog/ , 목록 페이지?  (추가하려면 뒤에 꼭 , 넣어야함)
    #path('<int:pk>/',views.single_post_page)  #int 숫자가 옴
]