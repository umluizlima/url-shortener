.PHONY: environment
environment:
	pyenv install -s 3.10.0
	pyenv uninstall --force url-shortener
	pyenv virtualenv 3.10.0 --force url-shortener
	pyenv local url-shortener
