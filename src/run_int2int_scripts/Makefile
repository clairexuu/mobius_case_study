ENCODING ?= CRT100_with_stats
NUM_SAMPLES ?= 1000000
SEED ?=

.PHONY: usage
usage:
	@echo "USAGE"
	@echo "  make data [ENCODING=interCRT100] [NUM_SAMPLES=1000000] [SEED=42]"
	@echo "  make run [ENCODING=interCRT100]"
	@echo "  make run-cpu [ENCODING=interCRT100]"
	@echo ""
	@echo "Available encodings:"
	@echo "  - interCRT100          : [n mod p, p, ...] (vec len: 200)"
	@echo "  - CRT100               : [n mod p, ...] (vec len: 100)"
	@echo "  - interCRT100_with_n   : [n mod p, p, ..., n] (vec len: 201)"
	@echo "  - CRT100_with_stats    : [n mod p, ..., x, k, parity] (vec len: 103)"
	@echo ""
	@echo "Examples:"
	@echo "  make data ENCODING=interCRT100 SEED=42"
	@echo "  make run ENCODING=CRT100"
	@echo "  make run ENCODING=CRT100_with_stats SEED=42"

.PHONY: data
data:
	make -C ../scripts/ shuffle ENCODING=$(ENCODING) NUM_SAMPLES=$(NUM_SAMPLES) $(if $(SEED),SEED=$(SEED))

.PHONY: run
run: data
	bash int2int_mu.sh $(ENCODING)
	bash int2int_musq.sh $(ENCODING)

.PHONY: run-cpu
run-cpu: data
	bash int2int_mu_cpu.sh $(ENCODING)
