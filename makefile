run:
	python -m uvicorn src.app:app --reload

lint:
	python -m isort . --profile black
	python -m black .
	python -m pylint src