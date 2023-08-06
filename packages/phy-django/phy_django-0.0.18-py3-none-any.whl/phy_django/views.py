import django.contrib
import django.contrib.auth
import django.contrib.messages
import django.core.exceptions
import django.http
import django.urls
import guardian.mixins
from django.views.generic import TemplateView as DjangoTemplateView, FormView as DjangoFormView
from django.views.generic.base import RedirectView as DjangoRedirectView
from django.views.generic.detail import DetailView as DjangoDetailView, SingleObjectMixin as DjangoSingleObjectMixin
from guardian.shortcuts import assign_perm

__keep = (django.urls.reverse_lazy, django.urls.reverse, assign_perm)


class PermissionRequiredMixin(guardian.mixins.PermissionRequiredMixin):
    return_403 = True


class PhyDjangoMixin:
    """一些符合我的开发习惯的配置

    - request的类型提示
    - 可以获取用户对象，同样支持类型提示
    - 将发送信息作为一个方法提供
    """
    request: django.http.HttpRequest

    @property
    def user(self) -> django.contrib.auth.get_user_model():
        return self.request.user

    def message_user(self, message: str, level=django.contrib.messages.INFO):
        django.contrib.messages.add_message(self.request, level, message)


class ContextMixin(PhyDjangoMixin, django.views.generic.base.ContextMixin):
    """
    包含一些全局配置项
    """

    site_name = '我的网站'
    page_title = '首页'
    page_description = ''

    def get_page_description(self):
        if isinstance(self.page_description, str):
            return self.page_description
        if isinstance(self.page_description, (list, tuple)):
            return ''.join([f'<p>{line}</p>' for line in self.page_description])
        raise django.core.exceptions.ImproperlyConfigured(f'page description error: {type(self.page_description)}')

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        [kwargs.setdefault(k, v) for k, v in {
            'user': self.user,
            'site_name': self.site_name,
            'page_title': self.page_title,
            'page_description': self.get_page_description(),
        }.items()]
        return kwargs


class TemplateView(ContextMixin, DjangoTemplateView):
    pass


class DetailView(ContextMixin, DjangoDetailView):
    pass


class FormView(ContextMixin, DjangoFormView):
    template_name = 'phy_django/form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class SingleObjectMixin(DjangoSingleObjectMixin):
    pass


class RedirectView(PhyDjangoMixin, DjangoRedirectView):
    pass
