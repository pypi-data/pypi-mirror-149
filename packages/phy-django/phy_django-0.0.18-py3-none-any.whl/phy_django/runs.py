import os
import sys
from pathlib import Path


def init_run(application_name='application'):
    """在外部脚本中调用可以开启django运行环境

    Args:
        application_name: 项目名称，也就是装有 ``settings.py`` 的那个包的名称
    """
    sys.path.insert(0, str(Path(__file__).parent.parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{application_name}.settings')
    import django
    django.setup()
