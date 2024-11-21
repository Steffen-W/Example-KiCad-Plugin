#!/bin/bash

rm Example-KiCad-Plugin.zip
mv metadata.json metadata_.json
jq --arg today "$(date +%Y.%m.%d)" '.versions[0].version |= $today' metadata_.json > metadata.json

git ls-files  -- 'metadata.json' 'resources/*.png'  | xargs zip Example-KiCad-Plugin.zip

mkdir -p plugins
git ls-files -- 'example/*.png' 'example/*.py' "__init__.py" | cpio -pdm plugins
zip -r Example-KiCad-Plugin.zip plugins
rm -r plugins

mv metadata_.json metadata.json
