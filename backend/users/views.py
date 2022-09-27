from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import decorators, response, status
from rest_framework.permissions import IsAuthenticated

from .serializers import FollowsSerializer, FoodgramUserSerializer

User = get_user_model()


class FoodgramUserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = FoodgramUserSerializer
    serializer_class_follow = FollowsSerializer

    @decorators.action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        authors_qs = User.objects.filter(
            id__in=user.follower.all().values_list('author')
        )
        pages = self.paginate_queryset(authors_qs)
        serializer = self.serializer_class_follow(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @decorators.action(
        detail=True,
        methods=['post', ],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        user = request.user
        if author == user:
            return response.Response(
                {'errors': 'Подписка на себя невозможна.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.follows.filter(pk=author.id).exists():
            return response.Response(
                {'errors': 'Вы уже подписаны на {}.'.format(author)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class_follow(
            author,
            context={'request': request}
        )
        user.follows.add(author)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if user.follows.filter(pk=author.id).exists():
            user.follows.remove(author)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {'errors': 'Вы уже отписались от {}.'.format(author)},
            status=status.HTTP_400_BAD_REQUEST
        )
