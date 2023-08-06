import django.contrib.auth
import django.db.models
import django.http
import django_admin_object_button
import django_json_widget.widgets
import guardian.admin
import import_export.admin
from django.contrib.admin import *
from django.contrib.admin import ModelAdmin as _DjangoModelAdmin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import resolve, include, path
from django_admin_object_button import object_button

import phy_django.models
from phy_django.models import Configuration

__keep = (
    object_button, redirect, register, display, action, resolve, PermissionDenied,
    path, include, TemplateResponse,  # 用于添加自定义的View
)


class SuperuserPermissionMixin(_DjangoModelAdmin):
    """添加了一个管理员的权限"""

    @staticmethod
    def has_superuser_permission(request):
        return request.user.is_superuser


class AdminCanModifyObjectLevelPermissionMixin(SuperuserPermissionMixin, guardian.admin.GuardedModelAdmin):
    """仅允许管理员修改对象级别的权限"""

    only_admin_can_manage_object_level_permissions = True
    """是否启用这项功能，如果启用，则仅有管理员才有权限修改对象级别的权限"""

    def has_manage_object_perms_permission(self, request):
        if self.only_admin_can_manage_object_level_permissions and not self.has_superuser_permission(request):
            return False
        return True

    def obj_perms_manage_view(self, request, object_pk):
        if not self.has_manage_object_perms_permission(request):
            raise PermissionDenied
        return super().obj_perms_manage_view(request, object_pk)

    def obj_perms_manage_group_view(self, request, object_pk, group_id):
        if not self.has_manage_object_perms_permission(request):
            raise PermissionDenied
        return super().obj_perms_manage_group_view(request, object_pk, group_id)

    def obj_perms_manage_user_view(self, request, object_pk, user_id):
        if not self.has_manage_object_perms_permission(request):
            raise PermissionDenied
        return super().obj_perms_manage_user_view(request, object_pk, user_id)

    change_form_template = 'admin/change_form.html'


class UseInitialDataMixin(_DjangoModelAdmin):
    """如果在创建新对象时，某个字段为空值，且这个字段设置了初始值，则使用这个初始值。"""

    def save_model(self, request, obj, form, change: bool):
        if not change:
            [getattr(obj, k, None) is None and setattr(obj, k, v)
             for k, v in self.get_changeform_initial_data(request).items()]

        return super().save_model(request, obj, form, change)


class OnlyAdminCanChangeOwnerMixin(guardian.admin.GuardedModelAdmin):
    """仅有管理员可以更改对象的所有权"""
    only_admin_can_change_owner = True
    """如果为真，则仅有所有者有权更改对象所有权字段"""

    def get_readonly_fields(self, request, obj=None):
        result = super().get_readonly_fields(request, obj)

        # 如果仅允许管理员控制所有权，则所有者字段将对非管理员禁用
        if self.only_admin_can_change_owner and self.user_can_access_owned_objects_only \
                and not request.user.is_superuser:
            result = (*result, self.user_owned_objects_field)

        return result


class SetCurrentUserDefaultOwnerMixin(guardian.admin.GuardedModelAdmin):
    """如果启用了guardian的权限管理，则将当前用户设置为表单的初始值"""

    def get_changeform_initial_data(self, request: django.http.HttpRequest):
        result = super().get_changeform_initial_data(request)

        # 如果启用了权限管理，将所有者字段的默认值设置为当前用户
        if self.user_can_access_owned_objects_only:
            result.setdefault(self.user_owned_objects_field, request.user)

        return result


class OnlyAdminCanEditFieldsMixin(_DjangoModelAdmin):
    """仅管理员可以更改的字段"""

    only_admin_editable_fields: tuple[str, ...] = ()
    """仅管理员可以更改的字段"""

    def get_readonly_fields(self, request, obj=None):
        result = super().get_readonly_fields(request, obj)

        # 配置仅管理员才可以更改的字段
        if not request.user.is_superuser:
            result = (*result, *self.only_admin_editable_fields)

        return result


class ModelAdmin(
    OnlyAdminCanEditFieldsMixin,
    SetCurrentUserDefaultOwnerMixin,
    OnlyAdminCanChangeOwnerMixin,
    UseInitialDataMixin,
    AdminCanModifyObjectLevelPermissionMixin,
    import_export.admin.ImportExportMixin,
    SuperuserPermissionMixin,
    django_admin_object_button.ObjectButtonMixin,
    guardian.admin.GuardedModelAdmin,
    _DjangoModelAdmin,
):
    """整合一系列功能的后台管理基类"""

    @staticmethod
    def get_action_name(request: django.http.HttpRequest):
        return resolve(request.path).url_name.rsplit('_', maxsplit=1)[1]

    list_per_page = 50
    user_can_access_owned_objects_only = True

    formfield_overrides = {
        django.db.models.JSONField: {
            'widget': django_json_widget.widgets.JSONEditorWidget,
        },
        phy_django.models.JSONField: {
            'widget': django_json_widget.widgets.JSONEditorWidget,
        },
    }
    """对于不同类型的字段使用不同的对象进行显示"""

    def has_import_permission(self, request: django.http.HttpRequest):
        """导入导出的权限不支持对象级别的权限"""
        codename = django.contrib.auth.get_permission_codename('import', self.opts)
        return request.user.has_perm("%s.%s" % (self.opts.app_label, codename))

    def has_export_permission(self, request):
        """导入导出的权限不支持对象级别的权限"""
        codename = django.contrib.auth.get_permission_codename('export', self.opts)
        return request.user.has_perm("%s.%s" % (self.opts.app_label, codename))

    def has_module_permission(self, request):
        """鉴权以判断是否显示在主界面"""
        # 检查应用级权限：如果用户登录且拥用应用中的任何一个表的任何一种权限，则可见
        if super().has_module_permission(request):
            return True

        # 检查行级权限：如果用户有权访问后台且可以操作其中的一个对象，则可见
        return request.user.is_staff and self.get_queryset(request).exists()


@register(Configuration)
class ConfigurationAdmin(ModelAdmin):
    """键值对配置项的管理后台"""
    list_display = ('id', 'user', 'key', 'value')
    user_can_access_owned_objects_only = True
