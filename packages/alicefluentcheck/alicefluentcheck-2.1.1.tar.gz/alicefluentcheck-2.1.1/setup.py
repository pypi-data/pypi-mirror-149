import os
import re

from setuptools import find_namespace_packages, setup

package_version = os.environ.get("VERSION", "0.0.0.dev0")

if not re.match(r"\d+\.\d+\.\d(\..*)?", package_version):
    package_version = "0.0.0-dev"
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

title = "alicefluentcheck"
author = "a.krapivin"
email = "krapivin_andrey@mail.ru"
url = "https://github.com/KrapivinAndrey/YaAlice_FluentTesting"

requires = ["fluentcheck"]
requires_test = ["pytest", "pytest-cov", "pytest-runner"]
requires_dev = requires_test + ["black", "flake8"]

setup(
    name=title,
    version=package_version,
    description="Подготовка запросов для тестирования навыков Яндекс.Алисы",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=requires,
    setup_requires=requires_dev,
    tests_require=requires_test,
    url=url,
    packages=["alicefluentcheck"],
    include_package_data=True,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
