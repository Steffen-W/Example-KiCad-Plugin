#!/bin/bash

rm Example-KiCad-Plugin.zip
mv metadata.json metadata_.json
jq --arg today "$(date +%Y.%m.%d)" '.versions[0].version |= $today' metadata_.json > metadata.json

git ls-files  -- 'metadata.json' 'resources*.png' 'plugins*.png' 'plugins*.py' 'plugins/plugin.json' 'plugins/requirements.txt' 'plugins/kicad_advanced' | xargs zip Example-KiCad-Plugin.zip

mv metadata_.json metadata.json
