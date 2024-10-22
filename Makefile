run:
	@python main.py

clean:
	@rm -R dist

build:
	@py -m build

release:
	twine upload dist/* --verbose


