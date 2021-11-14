# Anki embedded browser addon

To run the tests, install `pytest-anki`.
```
pip install pytest-anki
pytest test.py
```

To enable addon in Anki, check the add-ons directory of your Anki installation (Tools > Add-ons > View Files).
Add a symbolic link that links the myaddon module directory with a directory in the add-ons directory.
```
REPO_DIR=~/repos/anki-addon
ANKI_ADDONS_DIR=~/Library/Application\ Support/Anki2/addons21
ln -s ${REPO_DIR}/myaddon ${ANKI_ADDONS_DIR}/myaddon
```
