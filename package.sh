pip install --target ./package -r requirements.txt

zip -r mindmaprest-package.zip mindmap_api *.py

cd package/
zip -ur ../mindmaprest-package.zip *
cd -