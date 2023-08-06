###Copyright owned by HOStudio[@hopy]$ author (QQ Name)
###Copyright owned by HOStudio123 author (Github Name)
###Copyright owned by HOStudioHonghong author (Pypi Name)
import setuptools
import readline
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name = 'HOPYBOX',
    version = '0.9.6',
    author = 'ChenJinLin',
    author_email = 'hostudio.hopybox@foxmail.com',
    description = 'This is an open source, practical command Python box',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/HOStudio123/HOPYBOX',
    packages = setuptools.find_packages(),
    license = 'GPL-3.0-or-later',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
            "console_scripts":[
                "hopybox=hopybox:pattern",
                ]
            },
    python_requires = '>=3.8',
    install_requires = ['wget','bs4','requests','lxml>=4.6.0','filetype','yagmail','rich','readline>=1.0.0']
)