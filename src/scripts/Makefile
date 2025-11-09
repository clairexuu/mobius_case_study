PYTHON = python3
ENCODING ?= interCRT100
NUM_SAMPLES ?= 1000000
SEED ?=

.PHONY: usage
usage:
	@echo "USAGE"
	@echo "  good_data [ENCODING=interCRT100] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  corrupted_data"
	@echo "  shuffle [ENCODING=interCRT100]"
	@echo "  clean"
	@echo ""
	@echo "Available encodings:"
	@echo "  - interCRT100          : [n mod p, p, ...] (vec len: 200)"
	@echo "  - CRT100               : [n mod p, ...] (vec len: 100)"
	@echo "  - interCRT100_with_n   : [n mod p, p, ..., n] (vec len: 201)"
	@echo "  - CRT100_with_stats    : [n mod p, ..., x, k, parity] (vec len: 103)"
	@echo ""
	@echo "Examples:"
	@echo "  make good_data ENCODING=interCRT100"
	@echo "  make good_data ENCODING=CRT100 NUM_SAMPLES=500000 SEED=42"
	@echo "  make shuffle ENCODING=CRT100_with_stats"


.PHONY: mobius
mobius:
	make -C ../mobius_code mobius.so

good_data: mobius
	mkdir -p ../../input
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	touch good_data_$(ENCODING)

corrupted_data: mobius
	mkdir -p ../../input
	$(PYTHON) generate_corrupted_datafiles.py
	touch corrupted_data

shuffle: good_data_$(ENCODING)
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING)
	touch shuffle_$(ENCODING)

.PHONY: clean
clean:
	rm -f good_data*
	rm -f corrupted_data
	rm -f shuffle*
	rm -rf __pycache__/
