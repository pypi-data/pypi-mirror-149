#!/bin/bash

# checks
[ $# -ne 1 ] && echo "usage: $(basename "$0") <some-repo-containing-setup.py>" 1>&2 && exit 1
[ ! -d "$1" ] && echo "$1: is not a directory" 1>&2 && exit 1
[ ! -f "$1/setup.py" ] && echo "$1: doesn't contain setup.py" 1>&2 && exit 1

# some vars
tmpdir="$(mktemp -d /tmp/venv-XXXX)"
reponame="$(cd "$1" && basename "$(pwd)")"

# copy repo to a temporary directory
cp -a "$1" "$tmpdir/$reponame"

# create virtualenv
virtualenv "$tmpdir"
export IT4I_FACTORY_PREBUILD=1

# run virtualenv and try installing the package inside of it (everything runs
# under a special Bash session)
bash --init-file <(echo "cd $tmpdir && . ./bin/activate ;
                         cd \"$reponame\" && python setup.py sdist")

# remove temporary files
echo -n "Removing $tmpdir..."
rm -rf "$tmpdir"
echo "done."
