import os
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import is_zipfile
from zipfile import ZipFile

from .utils import get_content
from .utils import get_subdir_name
from .utils import is_url
from .utils import match


def handle_dir(
    dir,
    dst,
    files_patterns,
    to_render,
    exclude_patterns,
    project_name
):
    if match(dir, exclude_patterns):
        return None

    if dir.match('project_name'):
        dst = dst.with_name(project_name)

    new = handle_tree(
        dir,
        dst,
        project_name,
        files_patterns
    )
    to_render.extend(new)


def handle_file(
    file,
    dst,
    patterns,
    to_render
):
    if match(file, patterns):
        dst = dst.with_name(dst.name.replace('-tpl', ''))
        to_render.append(dst)
    shutil.copyfile(file, dst)


def handle_template(
    project_name,
    target,
    template,
    files_patterns,
    exclude_patterns,
    context
):
    args = [
        template,
        target,
        project_name,
        files_patterns,
        exclude_patterns
    ]
    if is_url(template):
        files = handle_url(*args)
    elif is_zipfile(template):
        files = handle_zip(*args)
    else:
        files = handle_tree(*args)

    for file in files:
        content = get_content(file, context)
        file.write_text(content)


def handle_tree(
    path,
    target,
    project_name,
    files_patterns,
    exclude_patterns
):
    path = Path(path).resolve()
    to_render = []
    os.makedirs(target, exist_ok=True)

    for entity in path.iterdir():
        dst = target / entity.name

        if entity.is_file():
            handle_file(
                entity,
                dst,
                files_patterns,
                to_render
            )
        if entity.is_dir():
            handle_dir(
                entity,
                dst,
                files_patterns,
                to_render,
                exclude_patterns,
                project_name
            )

    return to_render


def handle_url(
    url,
    target,
    project_name,
    files_patterns,
    exclude_patterns
):
    content, _ = urlretrieve(url)

    with ZipFile(content) as archive:
        archive.extractall()

    # There is subdir in the GitHub repository zip archive
    # like this: django-start-tool-main -- '{repo}-{branch}'.
    # It is necessary to extract all the contents and delete this subdir.
    subdir_name = get_subdir_name(url)
    files = handle_tree(
        subdir_name,
        target,
        project_name,
        files_patterns,
        exclude_patterns
    )
    shutil.rmtree(subdir_name)
    return files


def handle_zip(
    path,
    target,
    project_name,
    files_patterns,
    exclude_patterns
):
    tmp = target / 'tmp'

    with ZipFile(path) as archive:
        archive.extractall(tmp)

    files = handle_tree(
        tmp,
        target,
        project_name,
        files_patterns,
        exclude_patterns
    )
    shutil.rmtree(tmp)
    return files
