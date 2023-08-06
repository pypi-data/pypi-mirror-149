from functools import cached_property

import djmoney.money
import import_export.resources
import import_export.widgets
from import_export.resources import *

from phy_django import models


class IntegerChoiceWidget(import_export.widgets.Widget):
    def __init__(self, *args, choices, **kwargs):
        super().__init__(*args, **kwargs)
        self._choices = choices

    @cached_property
    def _choices_name_to_value(self):
        return {name: value for value, name in self._choices}

    @cached_property
    def _choices_value_to_name(self):
        return {value: name for value, name in self._choices}

    def clean(self, value, row=None, *args, **kwargs):
        return self._choices_name_to_value[value]

    def render(self, value, obj=None):
        return self._choices_value_to_name[value]


class MoneyWidget(import_export.widgets.Widget):
    """用于进行 MoneyField 的导出功能"""

    def render(self, value: djmoney.money.Money, obj=None):
        return super(MoneyWidget, self).render(value.amount, obj)


class ModelResource(import_export.resources.ModelResource):
    """优化后的基类

    对一些字段进行了重定义。
    """

    @classmethod
    def widget_from_django_field(cls, f, default=widgets.Widget):
        result = super().widget_from_django_field(f, default)
        if result != default:
            return result
        for klass_name, widget in cls.WIDGETS_MAP.items():
            klass = getattr(models, klass_name)
            if isinstance(f, klass):
                if isinstance(widget, str):
                    widget = getattr(cls, widget)(f)
                return widget
        return default

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        widget = cls.widget_from_django_field(django_field)
        widget_kwargs = cls.widget_kwargs_for_field(field_name)
        if isinstance(django_field, models.IntegerField) and django_field.choices:
            widget = IntegerChoiceWidget
            widget_kwargs.setdefault('choices', django_field.choices)
        if isinstance(django_field, models.MoneyField):
            widget = MoneyWidget
        field = cls.DEFAULT_RESOURCE_FIELD(
            attribute=field_name,
            column_name=django_field.verbose_name,
            widget=widget(**widget_kwargs),
            readonly=readonly,
            default=django_field.default,
        )
        return field
