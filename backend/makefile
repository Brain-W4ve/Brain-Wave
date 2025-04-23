# Makefile

PYTHON=python
PYTEST=pytest
ALLURE_DIR=allure-results
ALLURE_CMD=allure

.PHONY: test report clean

# Run tests (optionally with marker): `make test` or `make test MARKER=unit`
test:
	@echo "Running tests$(if $(MARKER), with marker: $(MARKER),)..."
	$(PYTHON) -m $(PYTEST) $(if $(MARKER),-m "$(MARKER)",) --alluredir=$(ALLURE_DIR)

# Open the Allure report
report:
	@echo "Opening Allure report..."
	$(ALLURE_CMD) serve $(ALLURE_DIR)

# Clean Allure results
clean:
	@echo "Cleaning Allure results..."
	rm -rf $(ALLURE_DIR)
