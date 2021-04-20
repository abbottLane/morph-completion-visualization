install:
	virtualenv venv;
	. venv/bin/activate; 
	pip install -r requirements.txt; 

cree-tsv: install
	. venv/bin/activate; 
	python words2tsv-hfst.py