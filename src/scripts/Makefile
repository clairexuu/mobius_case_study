PYTHON = python3
ENCODING ?= interCRT100
DATASET_TYPE ?= natural
FUNCTION ?= mobius
NUM_SAMPLES ?= 1000000
SEED ?= 42

.PHONY: usage
usage:
	@echo "USAGE"
	@echo "  good_data [ENCODING=interCRT100] [DATASET_TYPE=natural] [FUNCTION=mobius] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  all_datasets [ENCODING=interCRT100] [FUNCTION=mobius] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  corrupted_data [FUNCTION=mobius]"
	@echo "  shuffle [ENCODING=interCRT100] [DATASET_TYPE=natural]"
	@echo "  shuffle_all [ENCODING=interCRT100]"
	@echo "  clean"
	@echo ""
	@echo "Available functions:"
	@echo "  - mobius     : Möbius function μ(n) ∈ {-1, 0, 1}"
	@echo "  - liouville  : Liouville function λ(n) ∈ {-1, 1}"
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
	@echo "  - lambda_*.txt  : Liouville function λ(n) ∈ {-1, 1}"
	@echo ""
	@echo "Examples:"
	@echo "  make good_data ENCODING=interCRT100 DATASET_TYPE=natural FUNCTION=mobius"
	@echo "  make good_data ENCODING=CRT100 DATASET_TYPE=cheat FUNCTION=liouville NUM_SAMPLES=100000"
	@echo "  make all_datasets ENCODING=CRT100_with_stats FUNCTION=liouville NUM_SAMPLES=1000000"
	@echo "  make corrupted_data FUNCTION=liouville"


.PHONY: compile
compile:
	make -C ../mobius_code all

good_data_$(ENCODING)_$(DATASET_TYPE)_$(FUNCTION): compile
	mkdir -p ../../input
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type $(DATASET_TYPE) --function $(FUNCTION) --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	touch good_data_$(ENCODING)_$(DATASET_TYPE)_$(FUNCTION)

.PHONY: good_data
good_data: good_data_$(ENCODING)_$(DATASET_TYPE)_$(FUNCTION)

.PHONY: all_datasets
all_datasets: compile
	@echo "Generating all dataset types for encoding: $(ENCODING), function: $(FUNCTION)"
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type natural --function $(FUNCTION) --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type cheat --function $(FUNCTION) --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	$(PYTHON) generate_datafiles.py --encoding $(ENCODING) --dataset_type non_cheat --function $(FUNCTION) --num_samples $(NUM_SAMPLES) $(if $(SEED),--seed $(SEED))
	@echo "Done generating all datasets for $(ENCODING), $(FUNCTION)"

corrupted_data_$(FUNCTION): compile
	mkdir -p ../../input
	$(PYTHON) generate_corrupted_datafiles.py --function $(FUNCTION)
	touch corrupted_data_$(FUNCTION)

.PHONY: corrupted_data
corrupted_data: corrupted_data_$(FUNCTION)

shuffle: good_data_$(ENCODING)_$(DATASET_TYPE)_$(FUNCTION)
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type $(DATASET_TYPE) --function $(FUNCTION)
	touch shuffle_$(ENCODING)_$(DATASET_TYPE)_$(FUNCTION)

.PHONY: shuffle_all
shuffle_all:
	@echo "Shuffling all dataset types for encoding: $(ENCODING), function: $(FUNCTION)"
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type natural --function $(FUNCTION)
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type cheat --function $(FUNCTION)
	$(PYTHON) shuffle_datafiles.py --encoding $(ENCODING) --dataset_type non_cheat --function $(FUNCTION)
	@echo "Done shuffling all datasets for $(ENCODING), $(FUNCTION)"

.PHONY: clean
clean:
	rm -f good_data*
	rm -f corrupted_data*
	rm -f shuffle*
	rm -rf __pycache__/
