# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
    
requirements:    
	pip install -r requirements.txt
	wget https://github.com/quarto-dev/quarto-cli/releases/download/v0.9.345/quarto-0.9.345-linux-amd64.deb
	sudo dpkg -i quarto-0.9.345-linux-amd64.deb
	rm quarto-0.9.345-linux-amd64.deb
    
submodules:
	git submodule update --init --recursive
	git submodule update --recursive --remote
    
serve:
	docker run -p 80:80 -v $(PWD)/build/html:/usr/share/nginx/html nginx:alpine
