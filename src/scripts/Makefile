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
	@echo "  - interCRT100                : [n mod p, p, ...] (vec len: 200)"
	@echo "  - CRT100                     : [n mod p, ...] (vec len: 100)"
	@echo "  - interCRT100_with_n         : [n mod p, p, ..., n] (vec len: 201)"
	@echo "  - CRT100_with_stats          : [n mod p, ..., x, k, parity] (vec len: 103)"
	@echo "  - interCRT_sqfree            : [n mod p, p, ..., sqfree] (vec len: 201)"
	@echo ""
	@echo "Available dataset types:"
	@echo "  - natural    : uniform random [1, 10^13] (for train/test split)"
	@echo "  - cheat      : only prime factors within first 100 primes (test only)"
	@echo "  - non_cheat  : at least one prime factor outside first 100 primes (test only)"
	@echo ""
	@echo "Output files generated:"
	@echo "  - mu_*.txt      : Möbius function μ(n) ∈ {-1, 0, 1}"
	@echo "  - musq_*.txt    : Squared Möbius μ²(n) ∈ {0, 1} (square-free indicator)"
	@echo "  # lambda_*.txt generation is currently disabled"
	@echo ""
	@echo "Examples:"
	@echo "  make good_data ENCODING=interCRT100 DATASET_TYPE=natural"
	@echo "  make good_data ENCODING=CRT100 DATASET_TYPE=cheat NUM_SAMPLES=100000 SEED=42"
	@echo "  make good_data ENCODING=interCRT_sqfree DATASET_TYPE=natural SEED=42"
	@echo "  make all_datasets ENCODING=CRT100_with_stats NUM_SAMPLES=1000000"
	@echo "  make shuffle ENCODING=interCRT_sqfree DATASET_TYPE=natural"
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

.PHONY: all_datasets
all_datasets: mobius
	@echo "Generating all dataset types for encoding: $(ENCODING)"
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type natural --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type cheat --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type non_cheat --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	@echo "Done generating all datasets for $(ENCODING)"

.PHONY: shuffle_all
shuffle_all:
	@echo "Shuffling all dataset types for encoding: $(ENCODING)"
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type natural
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type cheat
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type non_cheat
	@echo "Done shuffling all datasets for $(ENCODING)"

corrupted_data: mobius
	mkdir -p ../../input
	$(PYTHON) generate_corrupted_datafiles.py
	touch corrupted_data

shuffle: good_data_$(ENCODING)_$(DATASET_TYPE)
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type $(DATASET_TYPE)
	touch shuffle_$(ENCODING)_$(DATASET_TYPE)

.PHONY: clean
clean:
	rm -f good_data*
	rm -f corrupted_data
	rm -f shuffle*
	rm -rf __pycache__/
