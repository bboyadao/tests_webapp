.PHONY: tests cov cov_show

tests:
	pytest

cov:
	cd tests && coverage run -m pytest .
	cd tests && coverage report -m
	cd tests && coverage html


cov_show:
	xdg-open tests/htmlcov/index.html
