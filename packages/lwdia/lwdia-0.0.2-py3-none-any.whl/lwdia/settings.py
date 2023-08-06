import os
import sys

app_name = "lwdia"
app_version = "0.0.2"
app_author = "larryw3i"
app_author_email = "larryw3i@163.com"
app_maintainer = app_author
app_maintainer_email = app_author_email
app_description = ""
app_url = "https://github.com/larryw3i/lwdia"
app_contributors = [
    app_author,
    "",
]

app_sponsors = [""]

install_prefix = "python -m pip install "
requirements = [
    # product
    [  # ('requirement_name','version','project_url','License','license_url')
        (
            "appdirs",
            "",
            "https://github.com/ActiveState/appdirs",
            "MIT",
            "https://github.com/ActiveState/appdirs/blob/master/LICENSE.txt",
        ),
    ],
]


def get_requirements_product():
    install_requires = []
    for r in requirements[0]:
        install_requires.append(r[0] + r[1])
    return install_requires


def install_requirements_product():
    requirements_product = get_requirements_product()
    os.system(install_prefix + requirements_product)
