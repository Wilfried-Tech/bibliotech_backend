from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from bibliotech.mixins import MultipleSerializerMixin
from users.models import User
from users.permissions import IsSelf
from users.serializers import UserListSerializer, UserDetailSerializer, UserPasswordSerializer


class UserViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser | IsSelf]

    def get_permissions(self):
        if self.action == 'create':
            permissions = []
        elif self.action == 'list':
            permissions = [IsAdminUser]
        elif self.action == 'update' or self.action == 'partial_update':
            permissions = [IsSelf]
        else:
            permissions = self.permission_classes
        return [permission() for permission in permissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'change_password':
            return UserPasswordSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(is_staff=False, is_active=True)

    def perform_destroy(self, user):
        user.is_active = False
        user.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def ban(self, request, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'User banned'})

    @ban.mapping.delete
    def unban(self, request, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'User unbanned'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def promote(self, request, **kwargs):
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'message': 'User promoted'})

    @promote.mapping.delete
    def demote(self, request, **kwargs):
        user = self.get_object()
        user.is_staff = False
        user.save()
        return Response({'message': 'User demoted'})

    @action(detail=True, methods=['post'], permission_classes=[IsSelf])
    def change_password(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Password Changed'})

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def inactive(self, request):
        queryset = self.queryset.filter(is_active=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)