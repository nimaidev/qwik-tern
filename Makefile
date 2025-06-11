run:
	@uv run main.py

clean:
	@rm -R dist

build:
	@py -m build

release:
	twine upload dist/* --verbose

test:
	@python -m coverage run --source=./ -m unittest discover tests/ -v
	@python -m coverage report -m
