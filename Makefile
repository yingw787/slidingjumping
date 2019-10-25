clean:
	find . -maxdepth 1 -type f -name "*.pyc" -delete
	find . -maxdepth 1 -type f -name "*.pyo" -delete

run:
    python sliding_and_jumping.py

test:
	python -m unittest tests.py

