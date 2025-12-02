ENCODING ?= interCRT_sqfree_mobius
DATASET_TYPE ?= natural
NUM_SAMPLES ?= 1000000
SEED ?= 42
CONDA_ENV ?= DLNT
SHELL := /bin/bash

.PHONY: usage
usage:
	@echo "Encodings:"
	@echo "  - interCRT100                : [n mod p, p, ...] (vec len: 200)"
	@echo "  - CRT100                     : [n mod p, ...] (vec len: 100)"
	@echo "  - CRT100_with_stats          : [n mod p, ..., x, k, parity] (vec len: 103)"
	@echo "  - interCRT_sqfree_mobius     : [n mod p, p, ..., μ²(n), μ(n)] (vec len: 202)"
	@echo ""
	@echo "Dataset Types:"
	@echo "  - natural    : uniform random [1, 10^13] (for train/test split)"
	@echo "  - cheat      : only prime factors within first 100 primes (test only)"
	@echo "  - non_cheat  : at least one prime factor outside first 100 primes (test only)"
	@echo ""
	@echo "Functions:"
	@echo "  - mu         : Möbius function μ(n) ∈ {-1, 0, 1}"
	@echo "  - musq       : Squared Möbius μ²(n) ∈ {0, 1}"
	@echo "  # lambda (Liouville) generation is currently disabled"

.PHONY: data
data:
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=$(DATASET_TYPE) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))
	@if [ "$(DATASET_TYPE)" != "natural" ]; then \
		make -C ../scripts/ good_data ENCODING=$(ENCODING) DATASET_TYPE=natural NUM_SAMPLES=100000 $(if $(SEED),SEED=$(SEED)); \
		make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=natural NUM_SAMPLES=100000 $(if $(SEED),SEED=$(SEED)); \
	fi
	@if [ "$(DATASET_TYPE)" != "cheat" ]; then \
		make -C ../scripts/ good_data ENCODING=$(ENCODING) DATASET_TYPE=cheat NUM_SAMPLES=100000 $(if $(SEED),SEED=$(SEED)); \
		make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=cheat NUM_SAMPLES=100000 $(if $(SEED),SEED=$(SEED)); \
	fi
	@if [ "$(DATASET_TYPE)" != "non_cheat" ]; then \
		make -C ../scripts/ good_data ENCODING=$(ENCODING) DATASET_TYPE=non_cheat NUM_SAMPLES=100000 $(if $(SEED),SEED=$(SEED)); \
		make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=non_cheat NUM_SAMPLES=100000 $(if $(SEED),SEED=$(SEED)); \
	fi

.PHONY: data_all
data_all:
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=natural NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=cheat NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=non_cheat NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))

.PHONY: train
train:
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu.sh $(ENCODING) $(DATASET_TYPE)"

.PHONY: train_all
train_all:
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu.sh $(ENCODING) natural"
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu.sh $(ENCODING) cheat"
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu.sh $(ENCODING) non_cheat"

.PHONY: run
run: data train

.PHONY: run-cpu
run-cpu: data
	bash -c "source /home/ziwen/miniconda3/etc/profile.d/conda.sh && conda activate $(CONDA_ENV) && bash int2int_mu_cpu.sh $(ENCODING) $(DATASET_TYPE)"
