#!/bin/bash
pip install --target ./dependencies -r requirements.txt

zip -r mindmaprest-package.zip mindmap_api *.py

# Dependencies need to be in the root of the zip file
cd dependencies/
zip -ur ../mindmaprest-package.zip *
cd -

# Exit with success code
exit 0