import setuptools

import phy_django

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phy-django",
    version=phy_django.version,
    author=phy_django.author,
    author_email=phy_django.author_email,
    description=phy_django.description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=phy_django.url,
    packages=setuptools.find_packages(include=['phy_django*']),
    include_package_data=True,
    install_requires=[
        'django',
        'django-rest-framework',
        'django-q',
        'django-dump-load-utf8',
        'django-admin-object-button',
        'django-silk',
        'django-money',
        'django-registration',
        'django-crispy-forms',
        'django-guardian',
        'django-extensions',
        'django-import-export',
        'django-nested-admin',
        'django-json-widget',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
