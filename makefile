install:
	pip install --upgrade pip &&\
		pip install -U -r requirements.txt

format:
	black *.py src/*.py test/*.py

lint:
	pylint --disable=R,C *.py


