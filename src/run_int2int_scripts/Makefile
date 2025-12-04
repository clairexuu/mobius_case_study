ENCODING ?= interCRT_sqfree
DATASET_TYPE ?= natural
FUNCTION ?= mobius
NUM_SAMPLES ?= 1000000
SEED ?= 42
VENV_PATH ?= ../../venv
SHELL := /bin/bash

.PHONY: usage
usage:
	@echo "USAGE"
	@echo "  make data [ENCODING=interCRT100] [DATASET_TYPE=natural] [FUNCTION=mobius] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  make data_all [ENCODING=interCRT100] [FUNCTION=mobius] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  make run [ENCODING=interCRT100] [FUNCTION=mobius]"
	@echo "  make run-cpu [ENCODING=interCRT100] [FUNCTION=mobius]"
	@echo ""
	@echo "Encodings:"
	@echo "  - interCRT100                : [n mod p, p, ...] (vec len: 200)"
	@echo "  - CRT100                     : [n mod p, ...] (vec len: 100)"
	@echo "  - CRT100_with_stats          : [n mod p, ..., x, k, parity] (vec len: 103)"
	@echo "  - interCRT_sqfree            : [n mod p, p, ..., μ²(n)] (vec len: 201)"
	@echo ""
	@echo "Dataset Types:"
	@echo "  - natural    : uniform random [1, 10^13] (for train/test split)"
	@echo "  - cheat      : only prime factors within first 100 primes (test only)"
	@echo "  - non_cheat  : at least one prime factor outside first 100 primes (test only)"
	@echo ""
	@echo "Available functions:"
	@echo "  - mobius     : Möbius function μ(n) ∈ {-1, 0, 1}"
	@echo "  - liouville  : Liouville function λ(n) ∈ {-1, 1}"
	@echo ""
	@echo "Examples:"
	@echo "  make data ENCODING=interCRT100 DATASET_TYPE=natural FUNCTION=mobius SEED=42"
	@echo "  make data_all ENCODING=CRT100_with_stats FUNCTION=liouville NUM_SAMPLES=1000000 SEED=42"
	@echo "  make run ENCODING=CRT100 FUNCTION=liouville"
	@echo "  make run ENCODING=CRT100_with_stats FUNCTION=mobius SEED=42"

.PHONY: data
data:
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=$(DATASET_TYPE) FUNCTION=$(FUNCTION) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))

.PHONY: data_all
data_all:
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=natural FUNCTION=$(FUNCTION) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=cheat FUNCTION=$(FUNCTION) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) DATASET_TYPE=non_cheat FUNCTION=$(FUNCTION) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))

.PHONY: train
train:
	bash -c "source $(VENV_PATH)/bin/activate && bash int2int_mu.sh $(ENCODING) $(DATASET_TYPE) $(FUNCTION)"

.PHONY: train_all
train_all:
	bash -c "source $(VENV_PATH)/bin/activate && bash int2int_mu.sh $(ENCODING) natural $(FUNCTION)"
	bash -c "source $(VENV_PATH)/bin/activate && bash int2int_mu.sh $(ENCODING) cheat $(FUNCTION)"
	bash -c "source $(VENV_PATH)/bin/activate && bash int2int_mu.sh $(ENCODING) non_cheat $(FUNCTION)"

.PHONY: run
run: data train

.PHONY: run-cpu
run-cpu: data
	bash -c "source $(VENV_PATH)/bin/activate && bash int2int_mu_cpu.sh $(ENCODING) $(DATASET_TYPE) $(FUNCTION)"
