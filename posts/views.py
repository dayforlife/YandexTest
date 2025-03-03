from rest_framework import generics, permissions

from posts.utils import send_telegram_message
from .models import Post, Comment, PostRating
from .serializers import CommentSerializer, PostRatingSerializer, PostSerializer



class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

        # Если у пользователя есть Telegram ID, отправляем сообщение
        if self.request.user.telegram_chat_id:
            message = f"✅ Ваш пост опубликован!\n\n📝 Текст: {post.text[:100]}..."
            send_telegram_message(self.request.user.telegram_chat_id, message)

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Разрешает редактировать/удалять пост только автору или администратору.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.is_staff

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(post_id=post_id)



class IsAdminUser(permissions.BasePermission):
    """
    Разрешает редактировать/удалять комментарии только администраторам.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]


class PostRatingView(generics.CreateAPIView):
    serializer_class = PostRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']  # Берем ID поста из URL
        user = self.request.user
        rating_value = serializer.validated_data['rating']

        rating_obj, created = PostRating.objects.update_or_create(
            post_id=post_id, user=user, defaults={'rating': rating_value}
        )

class PostDetailWithRatingView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        avg_rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        avg_rating = round(avg_rating, 2) if avg_rating else 0  # Округляем до 2 знаков
        response = super().retrieve(request, *args, **kwargs)
        response.data['average_rating'] = avg_rating
        return response
