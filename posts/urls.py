from django.urls import path
from .views import (CommentCreateView, 
                    CommentDetailView, 
                    CommentListView, 
                    
                    PostDetailView, 
                    PostDetailWithRatingView, 
                    PostListView, 
                    PostCreateView, 
                    PostRatingView
)
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('add/', PostCreateView.as_view(), name='post-add'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comment/', CommentListView.as_view(), name='comment-list'),
    path('<int:post_id>/comment/add/', CommentCreateView.as_view(), name='comment-add'),
    path('<int:post_id>/comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:post_id>/mark_add/', PostRatingView.as_view(), name='post-mark-add'),
    path('<int:pk>/', PostDetailWithRatingView.as_view(), name='post-detail'),
]