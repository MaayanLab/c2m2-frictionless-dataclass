PYTHON=python3
LATEST=https://osf.io/vzgx9/download

c2m2-frictionless/c2m2_frictionless/C2M2/datapackage.json:
	$(PYTHON) -c \
		"import sys, urllib.request; urllib.request.urlretrieve(*sys.argv[1:])" \
			$(LATEST) $@

c2m2-frictionless/c2m2_frictionless/C2M2/__init__.py: c2m2-frictionless/c2m2_frictionless/C2M2/datapackage.json
	PYTHONPATH=frictionless-dataclass $(PYTHON) -m frictionless_dataclass -i $^ -o $@

.PHONY: update
update:
	--rm c2m2-frictionless/c2m2_frictionless/C2M2/datapackage.json
	make PYTHON=$(PYTHON) LATEST=$(LATEST) c2m2-frictionless/c2m2_frictionless/C2M2/__init__.py
