.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = hit-predictor
PROFILE = hit_predictor
PROJECT_NAME = hit_predictor
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Get Zipcodes
zipcodes: 
	$(PYTHON_INTERPRETER) src/scraper/get_zipcodes.py ${options}

## Scrape Proxies and Data
proxies: 
	$(PYTHON_INTERPRETER) src/scraper/get_proxies.py $(options)

## Starts Scraper
## Example Format make scraper target="hot100" scrapetype="iterator" scrapespeed="regular" options="'./data/iterators/hot100.csv'"
scraper: 
	$(PYTHON_INTERPRETER) src/scraper/scrape_data.py $(target) $(scrapetype) $(scrapespeed) $(batch) $(batch_size) $(iter_filepath)

iterator: 
	$(PYTHON_INTERPRETER) src/scraper/get_iterator.py $(target) $(reps) $(options)

# Create Environment
environment:
	conda env create -f environment.yml

# Pull Existing Dataset
data: requirements
	aws s3 sync s3://$(BUCKET)/data/ data/

## Make Dataset
new_data: requirements
	# Get a fresh set of proxies
	# make proxies
	# Create an Iterator for the Billboard Hot 100 Charts starting in 1958 to 2019 ($target) ($reps - optional)
	# make iterator target='week_saturday' reps=1 
	# Scrape Hot 100 Charts from Billboard.com
	# make scraper target='hot100' scrapetype='iterator' scrapespeed='fast' batch=False batch_size=50 iter_filepath='./data/iterators/week_saturday.csv'
	# Get Spotify Ids for Hot 100 ($reps - must be at least number of files from scrape above)
	make iterator target='spotify_ids_hot100' reps=1
	# spotify_ids_hot100.csv -> hot100_spotify_ids_iterator.csv
	$(PYTHON_INTERPRETER) src/data/make_hot100_unique_iterator.py
	# Get Analysis / Features from Spotify ()
	make scraper target='spotify_analysis_api' scrapetype='api' scrapespeed='fast' batch=True batch_size=50 iter_filepath='./data/iterators/spotify_ids_hot100_uniq.csv'

	# MAKE SURE TO RUN THE WRANGLING NOTEBOOK "_Step 2 Wrangling (Hot 100 and Spotify Sample)" BEFORE YOU PROCEED TO THIS STEP 
	make scraper target='comparison_data_analysis_api' scrapetype='api' scrapespeed='lightning' batch=True batch_size=50 iter_filepath='./data/iterators/spotify_songs_ids_iterator.csv'
	
	# Get Features for Hot 100 Songs
	# $(PYTHON_INTERPRETER) src/data/make_spotify_features.py
	# $(PYTHON_INTERPRETER) src/data/make_dataset.py

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already intalled.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
