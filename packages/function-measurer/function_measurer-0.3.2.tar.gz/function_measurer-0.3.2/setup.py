from setuptools import setup
import os

def read(path: str):
    with open(path, "r", encoding = "utf-8") as file:
        return file.read()

__version__ = "0.3.2"

scriptFolder = os.path.split(__file__)[0]
ReadmePath = os.path.join(scriptFolder, "README.md")

projectUrls = {
    "Homepage": "https://github.com/InternetStalker/function_measurer",
}

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]

setup(name = 'function_measurer',
    version = __version__,
    description = 'Python utility for compairing functions and other callable objects.',
    packages = ['measurer'],
    author = "InternetStalker",
    author_email = 'internetstalcker@yandex.ru',
    include_package_data = True,
    zip_safe = False,
    long_description = read(ReadmePath),
    long_description_content_type = 'text/markdown',
    project_urls = projectUrls,
    keywords = 'test tests testing runtime memory',
    classifiers = classifiers,
    license = 'MIT',
    install_requires = [
        "simple_file_user"
    ]
)