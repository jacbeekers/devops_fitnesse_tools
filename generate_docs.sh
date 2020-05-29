deactivate
source venv/bin/activate
pip3 install pdoc3
#
pdoc3 --force --output-dir docs/markdown create_fitnesse_artifact
pdoc3 --force --html --output-dir docs/html create_fitnesse_artifact

