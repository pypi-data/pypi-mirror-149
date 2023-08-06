"""
为 ``Django`` 自带的数据类型添加一些符合我的开发习惯的默认值，并添加了一些新的数据类型。
"""
import functools
import typing

import django.contrib
import django.contrib.auth
import django.core.exceptions
import django.db.models
import django.db.models.fields.files
import django.utils.timezone
from django.db.models import *
from django.db.models import Model as _Model
from django.db.transaction import atomic
from django.utils.functional import classproperty
from djmoney.models.fields import MoneyField

__keep = (atomic,)

if typing.TYPE_CHECKING:
    pass

user_model = django.contrib.auth.get_user_model()


class ForeignKey(ForeignKey):
    """继承自 ``ForeignKey``

    - 不进行数据库的外键约束
    - 禁止删除有外键的条目
    """

    @functools.wraps(ForeignKey.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('on_delete', PROTECT)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class FloatField(FloatField):
    """继承自 ``FloatField``

    - 设置默认值为0
    """

    @functools.wraps(FloatField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        super().__init__(*args, **kwargs)


class FieldFile(django.db.models.fields.files.FieldFile):
    """
    :meta private:
    """
    pass


class FileField(FileField):
    """继承自 ``FileField``

    - 允许空值
    """
    attr_class = FieldFile

    @functools.wraps(FileField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        super().__init__(*args, **kwargs)


class SmallIntegerField(SmallIntegerField):
    """继承自小整数字段

    - 默认值为 ``0``
    """

    @functools.wraps(SmallIntegerField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        super().__init__(*args, **kwargs)


class ShortStringField(CharField):
    """短字符串，继承自 ``CharField``

    - 最长 ``100`` 个字符
    - 默认值为空字符串
    - 允许在 ``admin`` 中传入空值
    """

    @functools.wraps(CharField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('default', '')
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class LongStringField(CharField):
    """长字符串，继承自 ``CharField``

    - 最长 ``1000`` 个字符
    - 默认值为空字符串
    - 允许在 ``admin`` 中传入空值
    """

    @functools.wraps(CharField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 1000)
        kwargs.setdefault('default', '')
        super().__init__(*args, **kwargs)


class MoneyField(MoneyField):
    """钱字段，继承自 ``MoneyField``

    - 设置默认值为 ``0``
    - 设置默认单位为人民币
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        kwargs.setdefault('max_digits', 14)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('default_currency', 'CNY')
        super().__init__(*args, **kwargs)


class UserField(ForeignKey):
    """用户字段

    - 指向 ``auth.get_user_model()``
    - 允许空值
    - 删除保护

    """

    @functools.wraps(ForeignKey.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', '用户')
        kwargs.setdefault('to', django.contrib.auth.get_user_model())
        kwargs.setdefault('on_delete', PROTECT)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class TextField(TextField):
    """文本字段，继承自 ``TextField``

    - 允许空值
    - 设置默认值为空字符串
    """

    @functools.wraps(TextField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', '')
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class BooleanField(BooleanField):
    """布尔字段，继承自 ``BooleanField``

    - 设置默认值为否
    """

    @functools.wraps(BooleanField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', False)
        super().__init__(*args, **kwargs)


DEFAULT_DATETIME = django.utils.timezone.datetime(1970, 1, 1, tzinfo=django.utils.timezone.get_current_timezone())


class DateTimeField(DateTimeField):
    """日期时间字段，继承自 ``DateTimeField``

    - 设置默认时间值为当前时区内的 ``1970.1.1``
    """

    @functools.wraps(DateTimeField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', DEFAULT_DATETIME)
        super().__init__(*args, **kwargs)


class DateField(DateField):
    """日期字段，继承自 ``DateField``

    - 设置默认时间值为当前时区内的 ``1970.1.1``
    """

    @functools.wraps(DateField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', DEFAULT_DATETIME.date())
        super().__init__(*args, **kwargs)


class JSONField(JSONField):
    """Json字段，继承自 ``JsonField``

    - 设置默认值为空字典
    """

    @functools.wraps(JSONField.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', dict)
        super().__init__(*args, **kwargs)


class DatetimeMixin(_Model):
    """
    添加数据入库时间和数据更新时间两个自动字段
    """

    class Meta:
        abstract = True

    created_datetime = django.db.models.DateTimeField(
        verbose_name='数据库入库时间', auto_now_add=True,
    )
    updated_datetime = django.db.models.DateTimeField(
        verbose_name='数据库更新时间', auto_now=True,
    )


class Model(DatetimeMixin, _Model):
    """
    优化的模型基类，默认包括入库时间和更新时间字段，并自动将复数名称重定义到单数名称。

    在使用的时候，需要同时继承 ``Model`` 和 ``Model.Meta`` 。
    """

    class BaseMeta:
        abstract = False
        verbose_name = '未定义模型名称'

        # noinspection PyMethodParameters
        @django.utils.functional.classproperty
        def verbose_name_plural(cls):
            return cls.verbose_name

    class Meta(BaseMeta):
        abstract = True


class _MappableIntegerChoiceMeta(django.db.models.enums.ChoicesMeta):
    # noinspection PyMethodParameters
    def __new__(mcs, classname, bases, classdict, **kwds):
        has_meta = 'Meta' in classdict
        if has_meta:
            meta_class = classdict.pop('Meta')
            # noinspection PyProtectedMember
            classdict._member_names.remove('Meta')
        else:
            meta_class = None
        result = super().__new__(mcs, classname, bases, classdict, **kwds)
        if has_meta:
            result.Meta = meta_class
        return result


class MappableIntegerChoice(IntegerChoices, metaclass=_MappableIntegerChoiceMeta):
    """
    可以直接生成 ``Django`` 的 ``IntegerChoiceField`` ，包含选项。

    同时，支持设置默认值，支持定义值到 ``Enum`` 的映射以用于解析。

    Examples:
        .. code-block:: python

            class ExpenseType(MappableIntegerChoice):
                class Meta(MappableIntegerChoice.Meta):
                    default_value = 0
                    mapping = {'Active': 1, 'Inactive': 2}
                default = -1, '未设置'
                other = 0, "其他"
                choices_1 = 1, "选项1"
                choices_2 = 2, "选项2"
    """

    class Meta:
        """
        可以定义默认值和预定义的映射
        """
        default_value = 1
        """默认值

        Examples:
            .. code-block:: python

                class ExpenseType(MappableIntegerChoice):
                    class Meta(MappableIntegerChoice.Meta):
                        default_value = 0
        """

        mapping: dict[str, typing.Any] = {}
        """映射
        
        Examples:
            .. code-block:: python
                
                class ExpenseType(MappableIntegerChoice):
                    class Meta(MappableIntegerChoice.Meta):
                        default_value = 0
                        mapping = {'Active': 1, 'Inactive': 2}
        """

    @classmethod
    def parse(cls, value: str):
        """基于预定义的映射进行数据的转换，用于将本数据库中的值与其他的值进行同步

        映射中的定义值不应当用于界面显示，因为显示在界面中的字符串是可以通过 ``label`` 进行定义的。

        Examples:
            .. code-block:: python

                class MyModel(Model):
                    expense_type = ExpenseType.as_field(verbose_name='费用类型', help_text=__h)
        """
        return cls(cls.Meta.mapping.get(value, cls.Meta.default_value))

    @classmethod
    def as_field(cls, verbose_name: str = '', help_text='', negative=False, default=None):
        """作为一个 ``Django`` 的 ``Model`` 中的一个 ``Field`` 直接插入进去

        Examples:
            .. code-block:: python

                deemed_reseller_category = DeemedResellerCategory.as_field('转销类型')

        """
        klass = SmallIntegerField if negative else PositiveSmallIntegerField
        default = cls.Meta.default_value if default is None else default
        return klass(verbose_name=verbose_name, choices=cls.choices, default=default, help_text=help_text)


class IntegerStringField(PositiveBigIntegerField):
    """
    这个类对 ``String`` 进行了一层封装，可以直接用作 ``Model`` 的属性，在调用时将自动进行属性的转换。

    Examples:
        .. code-block:: python

            class MyModel(Model):
                name = IntegerStringField(default=1, verbose_name=verbose_name)
    """

    def to_python(self, value):
        if isinstance(value, int):
            return String.int_to_string(value)
        elif isinstance(value, str) or value is None:
            return value
        else:
            raise django.core.exceptions.ValidationError(f'Unknown type: {type(value)} of "{value}')

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def from_db_value(self, value, expression, connection):
        return None if value is None else String.int_to_string(value)

    def value_to_string(self, obj):
        return self.to_python(obj)

    def get_prep_value(self, value):
        return value if value is None else String.string_to_int(value)


class String(Model):
    """
    为字符串建立映射，存入一个总的字符串库。

    对于一些重复性较高的字符串，而又没必要新建一张表来存储，使用此方法可以有效地降低其数据库占用量。
    例如，在对接接口时，对方可能会通过字符串提供5种以上的状态值，而这些状态值我们预先并不能完全定义，就可以采用这种方法进行处理。

    Notes:
        字段将在启动时进行缓存，而每次写入时也会再次检查是否有重复。
        这种方法不适用于大量的字符串，不过对于常规需求（几万个字符串）来说都是可以轻松满足的（MB级内存占用）。
    """

    class Meta:
        indexes = (
            Index(fields=['value']),
        )

    value = CharField(
        max_length=255, unique=True,
    )

    def __str__(self):
        return self.value

    _default: int = 1
    _string_to_int_cache: dict[str, int] = {}
    _int_to_string_cache: dict[int, str] = {}

    @classmethod
    def __init_cache(cls):
        objs = [(o.id, o.value) for o in cls.objects.all()]
        cls._string_to_int_cache = {value: pk for pk, value in objs}
        cls._int_to_string_cache = {pk: value for pk, value in objs}

    @classmethod
    def string_to_int(cls, value: typing.Optional[str]) -> int:
        """字符串转整型的过程是一个写入的过程，从缓存中读取编号，或者写入编号"""
        if not cls._string_to_int_cache:
            cls.__init_cache()
        if value is None:
            return cls._default
        if value in cls._string_to_int_cache:
            return cls._string_to_int_cache[value]
        pk = cls.objects.get_or_create(value=value)[0].id
        cls._string_to_int_cache[value] = pk
        return pk

    @classmethod
    def int_to_string(cls, value: typing.Optional[int]) -> str:
        """整型转字符串的过程是一个读取的过程，从数据库中查询字符串的编号所对应的值"""
        if not cls._int_to_string_cache:
            cls.__init_cache()
        return cls._int_to_string_cache.get(value if value else cls._default)


class Configuration(Model):
    """键值对的配置，支持逐用户级别的配置

    在使用时不需要直接调用这个类，而是直接使用类方法 ``get`` 和 ``set`` 就可以了。

    用户可以设置为空值。
    """

    class Meta(Model.Meta):
        verbose_name = '配置'
        abstract = False

    user = UserField()
    key = ShortStringField(verbose_name='键')
    value = JSONField(verbose_name='值')

    @staticmethod
    def get(key: str, user=None, default: dict = None):
        """从数据库获取一个值。

        用户可以指定为空，则表示获取全局配置项。
        """
        obj, created = Configuration.objects.get_or_create(key=key, user=user)
        if created and default is not None:
            obj.value = default
            obj.save()
        return obj.value

    @staticmethod
    def set(key: str, value: dict, user=None):
        """设置一个值到数据库

        用户可以设置为空，则表示设置全局配置项。
        """
        obj, created = Configuration.objects.get_or_create(key=key, user=user)
        obj.value = value
        obj.save()
