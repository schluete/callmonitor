
run:
	LOCATION=lenauweg venv/bin/python3 -m flask run --host=0.0.0.0

build:
	docker build --tag callmonitor .
