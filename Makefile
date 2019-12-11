.PHONY: clean clean-build clean-pyc clean-test clean-docs lint test test-all coverage coverage github docs builddocs servedocs release dist install develop register requirements sync build compile

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER 		:= python -c "$$BROWSER_PYSCRIPT"
DOCSBUILDDIR	= docs/_build
DOCSSOURCEDIR	= docs/source

help:
	@echo "clean       		remove all build, test, coverage and Python artifacts"
	@echo "clean-build 		remove build artifacts"
	@echo "clean-pyc   		remove Python file artifacts"
	@echo "clean-test  		remove test and coverage artifacts"
	@echo "clean-docs  		remove autogenerated docs files"
	@echo "test        		run tests quickly with the default Python"
	@echo "test-all    		run tests on every Python version with tox"
	@echo "coverage    		check code coverage quickly with the default Python"
	@echo "github      		generate github's docs (i.e. README)"
	@echo "docs        		generate Sphinx HTML documentation, including API docs"
	@echo "servedocs   		semi-live edit docs"
	@echo "release     		package and upload a release"
	@echo "dist        		package"
	@echo "install     		install the package to the active Python's site-packages"
	@echo "develop     		install package in edit mode"
	@echo "register    		update pypi"
	@echo "requirements		update and install requirements"
	@echo "sync        		sync requirements with pip"

.coco.py: 
	coconut -jsys -t38 $<

clean: clean-build clean-pyc clean-test

clean-build:
	rm -f glioma/option.py
	rm -f glioma/containers.py
	rm -f glioma/either.py
	rm -f glioma/__init__.py
	rm -fr $(DOCSBUILDDIR)/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr ./htmlcov/

clean-docs:
	rm -f $(DOCSSOURCEDIR)/json_config.rst
	rm -f $(DOCSSOURCEDIR)/modules.rst
	#$(MAKE) -C docs clean

test: compile
	tox -e py38

test-all: compile
	tox

coverage:
	coverage run setup.py test
	coverage report
	coverage html -d ./htmlcov --include=glioma/* --omit=glioma/__*
	$(BROWSER) ./htmlcov/index.html

github:
	#python docs/github_docs.py
	#rst-lint README.rst

docs: clean-docs builddocs github

builddocs:
	# add --no-headings if you're adding them manually
	sphinx-apidoc \
		--private \
		--no-toc \
		--module-first \
		--output-dir=$(DOCSSOURCEDIR)/ json_config
	$(MAKE) -C docs html

servedocs: docs
	$(BROWSER) $(DOCSBUILDDIR)/html/index.html
	watchmedo shell-command \
		--pattern '*.rst;*.py' \
		--command '$(MAKE) builddocs' \
		--ignore-pattern '$(DOCSBUILDDIR)/*;$(DOCSSOURCEDIR)/json_config.rst' \
		--ignore-directories \
		--recursive

release: clean docs compile
	python setup.py sdist upload
	python setup.py bdist_wheel upload

#dist: clean docs compile
dist: clean compile
	python setup.py bdist_wheel

install: clean
	python setup.py install

develop: clean
	python setup.py develop

register:
	python setup.py register

compile: 
	coconut -jsys .

requirements:
	pip install --quiet --upgrade setuptools pip wheel pip-tools
	pip-compile requirements_dev.in > /dev/null
	pip-compile requirements.in > /dev/null
	pip-sync requirements_dev.txt > /dev/null
	git diff requirements.txt requirements_dev.txt 2>&1 | tee .requirements.diff

sync:
	pip install --quiet --upgrade pip-tools
	pip-sync requirements_dev.txt > /dev/null
