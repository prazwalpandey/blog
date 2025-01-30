from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
]
