install:
	virtualenv venv;
	. venv/bin/activate; 
	pip install -r requirements.txt; 

cree-tsv: install
	. venv/bin/activate; 
	python words2tsv-hfst.py

viz: install
	. venv/bin/activate; 
	python visualize_morph_data.py

explore:
	. venv/bin/activate;
	python explore_query.py