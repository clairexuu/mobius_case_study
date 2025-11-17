PYTHON = python3
ENCODING ?= interCRT100
DATASET_TYPE ?= natural
NUM_SAMPLES ?= 1000000
SEED ?= 42

.PHONY: usage
usage:
	@echo "USAGE"
	@echo "  good_data [ENCODING=interCRT100] [DATASET_TYPE=natural] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  all_datasets [ENCODING=interCRT100] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  corrupted_data"
	@echo "  shuffle [ENCODING=interCRT100] [DATASET_TYPE=natural]"
	@echo "  shuffle_all [ENCODING=interCRT100]"
	@echo "  clean"
	@echo ""
	@echo "Available encodings:"
	@echo "  - interCRT100          : [n mod p, p, ...] (vec len: 200)"
	@echo "  - CRT100               : [n mod p, ...] (vec len: 100)"
	@echo "  - interCRT100_with_n   : [n mod p, p, ..., n] (vec len: 201)"
	@echo "  - CRT100_with_stats    : [n mod p, ..., x, k, parity] (vec len: 103)"
	@echo ""
	@echo "Available dataset types:"
	@echo "  - natural    : uniform random [1, 10^13] (for train/test split)"
	@echo "  - cheat      : only prime factors within first 100 primes (test only)"
	@echo "  - non_cheat  : at least one prime factor outside first 100 primes (test only)"
	@echo ""
	@echo "Examples:"
	@echo "  make good_data ENCODING=interCRT100 DATASET_TYPE=natural"
	@echo "  make good_data ENCODING=CRT100 DATASET_TYPE=cheat NUM_SAMPLES=100000 SEED=42"
	@echo "  make all_datasets ENCODING=CRT100_with_stats NUM_SAMPLES=1000000"
	@echo "  make shuffle ENCODING=CRT100_with_stats DATASET_TYPE=natural"
	@echo "  make shuffle_all ENCODING=CRT100_with_stats"


.PHONY: mobius
mobius:
	make -C ../mobius_code mobius.so

good_data_$(ENCODING)_$(DATASET_TYPE): mobius
	mkdir -p ../../input
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type $(DATASET_TYPE) --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	touch good_data_$(ENCODING)_$(DATASET_TYPE)

.PHONY: good_data
good_data: good_data_$(ENCODING)_$(DATASET_TYPE)

.PHONY: other_datasets
other_datasets: mobius
	@echo "Generating cheat and non_cheat dataset types..."
	$(MAKE) good_data DATASET_TYPE=cheat NUM_SAMPLES=100000
	$(MAKE) good_data DATASET_TYPE=non_cheat NUM_SAMPLES=100000

corrupted_data: mobius
	mkdir -p ../../input
	$(PYTHON) generate_corrupted_datafiles.py
	touch corrupted_data

shuffle: good_data_$(ENCODING)_$(DATASET_TYPE)
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type $(DATASET_TYPE)
	touch shuffle_$(ENCODING)_$(DATASET_TYPE)

.PHONY: shuffle_all
shuffle_all:
	@echo "Shuffling cheat and non_cheat dataset types..."
	$(MAKE) shuffle DATASET_TYPE=cheat
	$(MAKE) shuffle DATASET_TYPE=non_cheat

.PHONY: clean
clean:
	rm -f good_data*
	rm -f corrupted_data
	rm -f shuffle*
	rm -rf __pycache__/
