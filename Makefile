# Some simple testing tasks (sorry, UNIX only).

flake:
	flake8 aiohttp_mako tests

test:
	nosetests -s -v ./tests/

cov cover coverage:
	nosetests -s --with-cover --cover-html --cover-branches \
            --cover-html-dir ./coverage --cover-package=aiohttp_mako ./tests/
	@echo "open file://`pwd`/coverage/index.html"

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf cover

doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

.PHONY: all build venv flake test vtest testloop cov clean doc
