#!/bin/bash

workdir=$(mktemp -d --tmpdir=/tmp neodym-build.XXXXXX)
projectdir="$workdir/NeoDym"
sourcedir="$projectdir/neodym"

if grep / <(echo $0) &>/dev/null; then
    echo 'Please run this script from its directory.'
fi

if [[ -z $1 ]]; then
    echo "Please provide version tag, e.g. '$0 0.1.0'"
fi

read -n 1 -p "Can haz package: NeoDym-$1 [y|N]: " answer
echo
if [[ ! "$answer" == y ]]; then
    echo "Bailing out by user request."
    exit 0
fi

cleanup() {
    rm -rf "$workdir"
}

# bootstrap working directory
#trap cleanup INT TERM QUIT
mkdir -p "$sourcedir"

# copy source to working directory
cp ../*.py "$sourcedir"

# copy meta-files to working directory
cp *.txt "$projectdir"
cp *.in "$projectdir"

# copy readme to working directory
cp ../readme.md "$projectdir/README.txt"

# create setup.py
setup_stanza="from distutils.core import setup

setup(
    name='NeoDym',
    version='$1',
    author='Brian Wiborg',
    author_email='baccenfutter@c-base.org',
    packages=['neodym'],
    scripts=[],
    url='http://pypi.python.org/pypi/NeoDym/',
    license='LICENSE.txt',
    description='A thin message-bus wrapper around asyncore.',
    long_description=open('README.txt').read(),
    install_requires=[],
)
"

echo "$setup_stanza" > "$projectdir/setup.py"

# run setup.py
cd "$projectdir"
python setup.py sdist
echo python setup.py sdist upload
