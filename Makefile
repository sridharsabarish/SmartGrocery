run: test
	cd src && python3 -m groceryEstimator.py

.PHONY: run test

test:
	python3 -m pytest -vv