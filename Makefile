
.PHONY: requirements
requirements:
	pip install -r test-requirements.txt

.PHONY: test
test:
	python setup.py test

.PHONY: dist
dist:
	python setup.py sdist

.PHYONY: clean
clean:
	rm -rf build
	rm -rf dist
	find . -name "*.pyc" -exec rm -f {} \;
