TEST_PATH=./

.PHONY: requirements
requirements:
	pip install -r test-requirements.txt

.PHONY: test
test:
	python setup.py test
