#!/bin/bash

if ! git diff-index --quiet HEAD; then
    echo "Can not process, there's uncommited changes."
    exit 1
fi

if echo "$@" | grep -q -- '--version'; then
    VERSION=$(echo "$@" | grep -oh -- '--version=.*' | cut -d '=' -f 2 | cut -d ' ' -f 1)
fi

if echo "$@" | grep -q -- '--identity'; then
    IDENTITY=$(echo "$@" | grep -oh -- '--identity=.*' | cut -d '=' -f 2 | cut -d ' ' -f 1)
fi
[[ -z "$IDENTITY" ]] && IDENTITY=EC451D66

CURRENT_VERSION=$(sed -n "s/__version__ = '\(.*\)'/\1/p" setup.py)
if [[ -z "$VERSION" ]]; then
    echo "Usage: $(basename $0) --version=VERSION [--identity=IDENTITY]"
    echo " - Current version: $CURRENT_VERSION"
    exit 1
fi

DATE=$(date +%Y-%m-%d)
CHANGELOG=$(mktemp -t tmp)
echo "v$VERSION, ${DATE}" > $CHANGELOG
CHANGELOG_FILTER="bump version and update changelog|\."
echo "$(git log v${CURRENT_VERSION}..HEAD --oneline | grep -Ev "^\w+ ($CHANGELOG_FILTER)$")" | while read LINE; do
    echo -e "    $LINE" >> $CHANGELOG
done
cat CHANGES.txt >> $CHANGELOG
cat $CHANGELOG > CHANGES.txt
$EDITOR CHANGES.txt

sed -i "s/__version__ = '.*'/__version__ = '$VERSION'/" setup.py
sed -i "s/__version__ = '.*'/__version__ = '$VERSION'/" cacheable/__init__.py

git commit -am "bump version and update changelog"
git push
git tag v$VERSION
git push --tags

rm -rf dist build *.egg-info
python setup.py sdist upload --sign --identity $IDENTITY
