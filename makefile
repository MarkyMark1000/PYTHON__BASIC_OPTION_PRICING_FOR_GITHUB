#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: help

help:
	@echo ""
	@echo "PROJECT HELP:"
	@echo "make               		- this prints out the help for this makefile."
	@echo "make help          		- this prints out the help for this makefile."
	@echo "Setup:"
	@echo "make venv	    		- this deletes and recreates the venv virtual environment from requirements.txt"
	@echo "make venv-docs	    		- delete and re-creates the html file in the docs directory using index.rst file"
	@echo "Run:"
	@echo "make run-bs-int      		- runs black scholes vs intrinsic price comparison."
	@echo "make run-bs-monte      		- runs black scholes vs monte carlo comparison."
	@echo "make run-th-graphs      	- runs black scholes vs threaded monte carlo graph comparison (no actual threading)."
	@echo "make run-thread      		- runs threaded time comparison for straddle"
	@echo "Docker:   (need to install and run docker)"
	@echo "make doc-prune-all		- DANGER: removes all stopped containers, images without containers etc"
	@echo "make doc-test-img-ub     	- builds docker image for tests using ubuntu image."
	@echo "make doc-test-run-ub     	- runs docker image as an interactive container for tests using ubuntu."
	@echo "make doc-test-img-py     	- builds docker image for tests using python image."
	@echo "make doc-test-run-py     	- runs docker image as an interactive container for tests using python."
	@echo "Tests:"
	@echo "make venv-test   		- Run the Test in the virtual environment."
	@echo "make venv-cov-report		- Run the Test in the virtual environment using coverage and then display coverage report"
	@echo "make venv-cov-html		- Run the Test in the virtual environment using coverage and build an html report"
	@echo "Code Standard:"
	@echo "make pystat   			- Code standards for ebdjango and apps directories."
	@echo "Clean:"
	@echo "make venv-clean    		- Remove __pycache__ etc"
	@echo "make clean-venv    		- Remove venv virtual environment."
	@echo "Distribution:"
	@echo "make venv-build-req    		- Rebuilds the requirements file from the venv virtual environment."
	@echo ""

venv:
	@echo ""
	@echo "Remove the venv virtual environment and then re-create it. using the requirements.txt file."
	@echo ""
	rm -rf venv
	@echo ""
	python3.7 -m venv venv
	@echo ""
	( source venv/bin/activate; pip install -r requirements.txt; )
	@echo ""
	@echo "  Now install the package (assume not in requirements)"
	@echo ""
	( source venv/bin/activate; pip install -e .; )
	@echo ""

venv-docs:
	@echo ""
	@echo "Remove the documents and then recreate it using index.rst"
	@echo ""
	@echo ""
	rm -rf ./docs/*.html
	@echo ""
	(source venv/bin/activate; rst2html5.py ./docs/index.rst ./docs/index.html; )
	@echo ""

run-bs-int:
	@echo ""
	@echo "Running application using venv virtual environment."
	@echo ""
	( source venv/bin/activate; python3.7 ./run/run_0_BlackScholesvsIntrinsic.py; )
	@echo ""

run-bs-monte:
	@echo ""
	@echo "Running application using venv virtual environment."
	@echo ""
	( source venv/bin/activate; python3.7 ./run/run_1_BlackScholesvsMonteCarlo.py; )
	@echo ""

run-th-graphs:
	@echo ""
	@echo "Running application using venv virtual environment."
	@echo ""
	( source venv/bin/activate; python3.7 ./run/run_2_ThreadOptionGraphs.py; )
	@echo ""

run-thread:
	@echo ""
	@echo "Running application using venv virtual environment."
	@echo ""
	( source venv/bin/activate; python3.7 ./run/run_3_ThreadedOption.py; )
	@echo ""

doc-prune-all:
	@echo ""
	@echo "DANGER: removing stopped docker containers and images"
	@echo ""
	@echo " removing all stopped containers, images without containers etc"
	@echo ""
	docker system prune -a
	@echo ""

doc-test-img-ub:
	@echo ""
	@echo "Building docker image for tests using ubuntu image"
	@echo ""
	docker build -f ./docker/DockerfileUB -t mark/optionpricing_tests_ub .
	@echo ""

doc-test-run-ub:
	@echo ""
	@echo "Running docker image as an interactive container for tests, using ubuntu"
	@echo ""
	docker run -it mark/optionpricing_tests_ub
	@echo ""

doc-test-img-py:
	@echo ""
	@echo "Building docker image for tests using python image."
	@echo ""
	docker build -f ./docker/DockerfilePY -t mark/optionpricing_tests_py .
	@echo ""

doc-test-run-py:
	@echo ""
	@echo "Running docker image as an interactive container for tests, using python "
	@echo ""
	docker run -it mark/optionpricing_tests_py
	@echo ""

venv-test:
	@echo ""
	@echo "Running test in venv virtual environment."
	@echo ""
	( source venv/bin/activate; python3.7 -m unittest; )
	@echo ""

venv-cov-report:
	@echo ""
	@echo "Running test using coverage and then display report in venv virtual environment."
	@echo ""
	( source venv/bin/activate; coverage run -m unittest discover; coverage report;)
	@echo ""

venv-cov-html:
	@echo ""
	@echo "Running test using coverage and then display report in venv virtual environment."
	@echo ""
	( source venv/bin/activate; coverage run -m unittest discover; coverage html;)
	@echo ""

pystat:
	@echo ""
	@echo "Code standards for ./analytics and ./run"
	@echo ""
	@echo " **** code standards - analytics ****"
	@echo ""
	( source venv/bin/activate; pycodestyle --statistics ./analytics/*.py; )
	@echo ""
	@echo " **** code standards - run ****"
	@echo ""
	( source venv/bin/activate; pycodestyle --statistics ./run/*.py; )
	@echo ""
	@echo " **** code standards - test ****"
	@echo ""
	( source venv/bin/activate; pycodestyle --statistics ./test/*.py; )
	@echo ""
	
venv-clean:
	@echo ""
	@echo "Remove __pycache__, etc"
	@echo ""
	rm -rf ./*/__pycache__*
	rm -rf *.egg*
	@echo ""

clean-venv:
	@echo ""
	@echo "Remove venv virtual environment directory"
	@echo ""
	rm -rf venv
	@echo ""

venv-build-req:
	@echo ""
	@echo "Rebuild requirements.txt from the venv virutal environment."
	@echo ""
	rm -rf requirements.txt
	@echo ""
	( source venv/bin/activate; pip freeze | sed -e '/^-e/d' -e '/^#/d' > requirements.txt; )
	@echo " (sed command removes the installation of this project, which begins with -e ... and comments #..)"
	@echo ""
