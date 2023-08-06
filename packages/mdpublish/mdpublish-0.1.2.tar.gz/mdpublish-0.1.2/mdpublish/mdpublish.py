"""
This tool converts a markdown project into a website
that can be easily published on the web.
"""
import re
import os
import shutil
from typing import List
from jinja2 import Template
from markdown_it import MarkdownIt
from gitignore_parser import parse_gitignore
PATH_REGEX = '(\.|\.\.|[\w\s\d])(/[\w\s\d])*'

builtin_styles = {
    'charcoal': {
        'summary': 'a simple, sleek color palette',
        'main': '#323232',
        'background': '#f5f5f5',
        'text': '#323232',
        'link': '#0079ff'
    },
    'tangerine': {
        'summary': 'similar to charcoal but with warmer colors',
        'main': '#e79500',
        'background': '#f5f5f5',
        'text': '#423f3a',
        'link': '#e79500'
    },
    'pine': {
        'summary': 'charcoal but in greens',
        'main': '#1e5e22',
        'background': '#e8e8e8',
        'text': '#323232',
        'link': '#37943e'
    },
    'dusk': {
        'summary': 'a basic dark mode palette',
        'main': '#82aaed',
        'background': '#343434',
        'text': '#e3e3e3',
        'link': '#82aaed'
    },
    'midnight': {
        'summary': 'the darker version of dusk',
        'main': '#5293d9',
        'background': '#1a1a1a',
        'text': '#cccccc',
        'link': '#82aaed'
    },
    'dolphin': {
        'summary': 'just a fun blue palette',
        'main': '#f3f3f3',
        'background': '#435e8a',
        'text': '#f3f3f3',
        'link': '#ade1ff'
    },
    'navy': {
        'summary': 'like a darker dolphin',
        'main': '#b3d0e6',
        'background': '#1f3240',
        'text': '#e3e3e3',
        'link': '#a9c0d1'
    }
}

def get_files(target: str) -> List[str]:
    """
    This function recursively grabs markdown files,
    except for those matched by .gitignore files.
    """
    files = []
    dirs = [target]
    gitignores = {}
    while len(dirs) > 0:
        path = dirs.pop(0)
        if is_dir(path):
            children = list_dir(path)
            if '.gitignore' in children:
                gitignores[path] = parse_gitignore(os.path.join(path, '.gitignore'))
            dirs += list(map(lambda x: os.path.join(path, x), children))
        elif re.search('\.md$', path):
            ignore = False
            for folder, matches in gitignores.items():
                if re.search(f'^{folder}', path) and matches(path):
                    ignore = True
                    break
            if not ignore:
                files.append(path)
    return files

def list_dir(path: str) -> List[str]:
    """
    Returns a list of files in the given directory
    """
    return os.listdir(path)

def is_dir(path: str) -> bool:
    """
    Returns tue if the given path is a directory
    """
    return os.path.isdir(path)

def make_dir(path: str) -> None:
    """
    Creates a directory somewhere for the generated files
    """
    os.makedirs(path, exist_ok = True)

def read_file(filepath: str) -> str:
    """
    Reads the contents of a file
    """
    with open(filepath, 'r', encoding = 'utf8') as file:
        return file.read()

def write_file(filepath: str, body: str) -> None:
    """
    Writes some content to a file
    """
    with open(filepath, 'w', encoding = 'utf8') as file:
        file.write(body)
        file.flush()

def log(msg: str) -> None:
    """
    This function logs the tool's progress
    """
    print(msg)

def print_help() -> None:
    """
    This function prints tool usage info
    """
    log('Usage: tool <src> <dst> [stylesheet]')
    log('  src and dst should be project paths')
    log('  stylesheets:')
    for style, details in builtin_styles.items():
        summary = details['summary']
        log(f'    - {style} ({summary})')

def main(args: List[str]) -> int:
    """
    This is the tool's main function. It holds the logic
    for converting markdown files into a website.
    """
    src = args[1] if len(args) > 1 else None
    dst = args[2] if len(args) > 2 else None
    style = args[3] if len(args) > 3 else 'charcoal'
    if not (src and dst and re.search(PATH_REGEX, src) and re.search(PATH_REGEX, dst)):
        print_help()
        return 1
    md = MarkdownIt()
    targets = get_files(src)
    log('Found 1 markdown file to convert' if len(targets) == 1 else
        f'Found {len(targets)} markdown files to convert')
    relative = lambda x: os.path.join(os.path.dirname(__file__), x)
    html_template = Template(read_file(relative('templates/page.html')))
    css_template = Template(read_file(relative('templates/style.css')))

    # Add the stylesheet
    make_dir(dst)
    outpath = f'{dst}/style.css'
    if os.path.exists(style):
        shutil.copyfile(style, outpath)
        log(f'Stylized after \'{style}\'')
    elif style in builtin_styles:
        write_file(outpath, css_template.render(style = builtin_styles[style]))
        log(f'Using style \'{style}\'')
    else:
        log(f'Unknown style \'{style}\'')
        return 1

    # Run conversion loop
    for file in targets:
        body = md.render(read_file(file))
        root = '/'.join(file[len(src):].split('/')[:-1])
        if len(root) > 0 and root[0] == '/':
            root = root[1:]
        if len(root) > 0 and root[-1] == '/':
            root = root[:-1]
        if root == '':
            root = '.'
        html = html_template.render(body = body, style = style, root = root)
        outpath = re.sub('\.md$', '.html', file)
        outpath = re.sub(f'^{src}', dst, outpath)
        log(f'Converted {file} -> {outpath}')
        parent = os.path.dirname(outpath)
        make_dir(parent)
        write_file(outpath, html)
    return 0
