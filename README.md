# Anki embedded browser

### Running the tests
To run the tests, install `pytest-anki`.
```
pip install pytest-anki
pytest test.py
```

### Installing the addon

To enable addon in Anki, add a symbolic link to the add-on folder in the Anki add-ons directory.
```
REPO_DIR=~/repos/anki-addon
ANKI_ADDONS_DIR=~/Library/Application\ Support/Anki2/addons21
ln -s ${REPO_DIR}/src ${ANKI_ADDONS_DIR}/myaddon
```
You can check what the add-ons directory of your Anki installation is under `Tools > Add-ons > View Files`.

### Todo

- Add dedicated dictionary lookup
- Add legend with shortcuts
