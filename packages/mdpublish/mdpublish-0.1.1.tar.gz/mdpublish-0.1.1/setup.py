from distutils.core import setup
setup(
    name = 'mdpublish',
    packages = [],
    version = '0.1.1',
    license = 'MIT',
    description = 'This tool creates pretty websites from markdown journal projects',
    author = 'Alex Lugo',
    author_email = 'alugocp@gmail.com',
    url = 'https://github.com/alugocp/mdpublish',
    download_url = 'https://github.com/alugocp/mdpublish/archive/v_0_1_1.tar.gz',
    keywords = ['markdown', 'readme', 'publish'],
    install_requires = [
        'gitignore_parser',
        'markdown-it-py',
        'pylint',
        'jinja2'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)