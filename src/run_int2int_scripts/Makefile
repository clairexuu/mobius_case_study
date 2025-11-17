ENCODING ?= interCRT100_with_n
DATASET_TYPE ?= natural
NUM_SAMPLES ?= 1000000
SEED ?= 42
CONDA_ENV ?= DLNT
SHELL := /bin/bash

.PHONY: usage
usage:
	@echo "USAGE"
	@echo "  make data [ENCODING=interCRT100] [DATASET_TYPE=natural] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  make data_all [ENCODING=interCRT100] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  make run [ENCODING=interCRT100]"
	@echo "  make run-cpu [ENCODING=interCRT100]"
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
	@echo "  make data ENCODING=interCRT100 DATASET_TYPE=natural SEED=42"
	@echo "  make data_all ENCODING=CRT100_with_stats NUM_SAMPLES=1000000 SEED=42"
	@echo "  make run ENCODING=CRT100"
	@echo "  make run ENCODING=CRT100_with_stats SEED=42"

.PHONY: data
data:
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=$(DATASET_TYPE) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))

.PHONY: data_all
data_all:
	make -C ../scripts/ other_datasets ENCODING=$(ENCODING) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))
	make -C ../scripts/ shuffle_all ENCODING=$(ENCODING)

.PHONY: run
run: data
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu.sh $(ENCODING) $(DATASET_TYPE)"
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_musq.sh $(ENCODING) $(DATASET_TYPE)"

.PHONY: run-cpu
run-cpu: data
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu_cpu.sh $(ENCODING) $(DATASET_TYPE)"
