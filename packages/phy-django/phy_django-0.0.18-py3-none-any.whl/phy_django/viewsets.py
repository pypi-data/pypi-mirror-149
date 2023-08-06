from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, CursorPagination, \
    LimitOffsetPagination as __LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet as __ModelViewSet

__keep = (
    action, atomic,
    PageNumberPagination, CursorPagination,
)


class LimitOffsetPagination(__LimitOffsetPagination):
    pass


class ModelViewSet(__ModelViewSet):
    """符合我的开发习惯的配置"""
    pagination_class = LimitOffsetPagination
