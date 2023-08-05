# Copyright 2022 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
import re
import json
import typing as t
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_context(str_or_path: t.Union[Path, str]):
    def match(s):
        return re.compile(s).match

    literal_loaders = [
        (match(r"py(thon)?:"), load_python_literal),
        (match(r"\s*\{"), load_json_literal),
        (match(r".*\.py:"), load_python_file_symbol),
    ]
    file_loaders = [
        (match(r".*\.py$"), load_python_file),
        (match(r".*\.rst$"), load_rst_file),
        (match(r".*\.md$"), load_md_file),
        (match(r".*\.js(on)?$"), load_json_file),
        (
            match(r"([_A-Za-z][_A-Za-z0-9]*)(\.[_A-Za-z][_A-Za-z0-9]*)*$"),
            load_python_module,
        ),
        (
            match(
                r"([_A-Za-z][_A-Za-z0-9]*)"
                r"(\.[_A-Za-z][_A-Za-z0-9]*)*"
                r":[_A-Za-z][_A-Za-z0-9]*$"
            ),
            load_python_module_symbol,
        ),
    ]

    path = str(str_or_path)
    if os.path.exists(path):
        for tell, loader in file_loaders:
            if tell(path):
                return loader(path)
    else:
        for tell, loader in literal_loaders:
            if tell(path):
                return loader(path)
    raise ValueError("Unrecognized file type {!r}".format(path))


def load_expr(src):
    ns = {}
    code = compile("result_ = ({})".format(src), "<string>", "exec")
    exec(code, ns)
    return ns["result_"]


def load_json_literal(s):
    return json.loads(s)


def load_python_literal(s):
    src = s.split(":", 1)[1]
    return load_expr(src)


def load_python_file(filename):
    with io.open(filename, "r", encoding=None) as f:
        source = f.read()
    ns = {"__file__": filename}
    code = compile(source, f.name, "exec")
    exec(code, ns)
    return ns


def load_python_file_symbol(s):
    filename, symbol = s.rsplit(":", 1)
    data = load_python_file(filename)[symbol]
    if callable(data):
        return data()
    return data


def load_md_file(s):
    import markdown

    md = markdown.Markdown(extensions=["extra", "meta"])

    with Path(s).open("r", encoding="utf-8") as f:
        html = md.convert(f.read())

    return {"html": html, "meta": md.Meta}


def load_rst_file(s):
    """
    See
    https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/core.py#L510
    for an example of how to set up a docutils publisher programatically
    """
    import docutils.core
    import docutils.readers.doctree
    import docutils.io
    from docutils import nodes

    meta = {}
    with Path(s).open("r", encoding="utf-8") as f:
        raw = f.read()

    doctree = docutils.core.publish_doctree(raw)

    def traverse(n, condition_path):

        if not condition_path:
            yield n
            return

        for child in n.traverse(condition_path[0]):
            yield from traverse(child, condition_path[1:])

    def first(n, condition_path, default=None):

        try:
            return next(iter(traverse(n, condition_path)))
        except StopIteration:
            return default

    for node in doctree.traverse(nodes.field):
        try:
            name = first(node, [nodes.field_name, nodes.Text]).astext()
            value = first(node, [nodes.field_body, nodes.Text]).astext().strip()
            meta[name] = value
        except AttributeError:
            pass
    date = first(doctree, [nodes.date, nodes.Text])
    if date is not None:
        meta["date"] = date.astext()

    docinfo = first(doctree, [nodes.docinfo])
    if docinfo is not None:
        doctree.remove(docinfo)

    reader = docutils.readers.doctree.Reader(parser_name="null")
    pub = docutils.core.Publisher(
        reader,
        None,
        writer=None,
        source=docutils.io.DocTreeInput(doctree),
        destination_class=docutils.io.StringOutput,
        settings=None,
    )
    pub.set_writer("html")
    pub.process_programmatic_settings(None, None, None)
    pub.set_destination(None, None)
    pub.publish()
    parts = pub.writer.parts

    return {
        "title": parts["title"],
        "meta": meta,
        "html": parts["html_body"],
        "html_without_title": parts["body"],
        "parts": parts,
    }


def load_json_file(s):
    with Path(s).open("r", encoding="UTF-8") as f:
        content = f.read()
        return json.loads(content)


def load_python_module(s):
    from importlib import import_module

    return vars(import_module(s))


def load_python_module_symbol(s):
    mod, sym = s.rsplit(":", 1)
    return load_python_module(mod)[sym]


def expand_source_paths(
    items: t.Iterable[t.Union[Path, str]],
    base: t.Optional[Path] = None,
) -> t.Iterable[t.Union[t.Tuple[Path, Path], t.Tuple[str, None]]]:
    if base is None:
        relpath = Path(".")
    else:
        relpath = base
    for path in map(Path, items):
        if not path.exists():
            logger.warning(f"Source {path!r} not found")
            continue
        if path.is_dir():
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    yield from expand_source_paths([Path(dirpath) / f], base or path)
        else:
            yield path, relpath
