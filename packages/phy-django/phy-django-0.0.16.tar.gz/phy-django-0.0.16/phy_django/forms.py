import crispy_forms.helper
import crispy_forms.layout

from django.forms import *


class CommonFormMixin(Form):
    """常用表单基类

    显示一个提交按钮
    """

    submit_button_name = '提交'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = crispy_forms.helper.FormHelper()
        if self.submit_button_name:
            self.helper.add_input(
                crispy_forms.layout.Submit('submit', self.submit_button_name, css_class='btn-primary'))
        self.helper.form_method = 'POST'


class CommonForm(CommonFormMixin, Form):
    pass
