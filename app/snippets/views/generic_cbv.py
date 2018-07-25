from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from utils.pagination import SnippetListPagination
from ..models import Snippet
from snippets.serializer import SnippetListSerializer, UserListSerializer, SnippetDetailSerializer
from ..permissions import IsOwnerOrReadOnly


__all__ = (
    'SnippetList',
    'SnippetDetail',
    'UserList',
    'UserDetail',
)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = SnippetListPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SnippetListSerializer
        elif self.request.method == 'POST':
            return SnippetDetailSerializer

    def perform_create(self, serializer):
        # SnippetListSerializer 로 전달받은 데이터와
        # 'owner'항목에 self.request.user 데이터를 추가한 후
        # save() 호출, DB에 저장 및 인스턴스 반환
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetListSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly,
    )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
