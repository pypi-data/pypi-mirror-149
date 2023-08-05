from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ProcTitle',
    version='0.1.6',
    author='Glenn Franxman',
    author_email='gfranxman@gmail.com',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    scripts=[],
    url='http://pypi.python.org/pypi/ProcTitle/',
    license="""ISC License

    Copyright (c) 2015, Glenn Franxman

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
    """,
    description='Context Manager to set/reset the current process name.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "setproctitle >= 1.1.10",
    ],
)
