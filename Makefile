.PHONY: clean run test all

all:
	@make test 
	@make run
	@make clean

clean:
	@find . -maxdepth 1 -type f -name "*.pyc" -delete
	@find . -maxdepth 1 -type f -name "*.pyo" -delete
	@rm -r __pycache__

run:
	@python sliding_and_jumping.py

test:
	@python -m unittest tests.py

