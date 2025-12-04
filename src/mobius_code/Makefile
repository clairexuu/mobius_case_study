PYTHON = python3

mobius.so: mobius.cpp
	g++ --std=c++17 -O3 -shared -o mobius.so -fPIC mobius.cpp

liouville.so: liouville.cpp
	g++ --std=c++17 -O3 -shared -o liouville.so -fPIC liouville.cpp

.PHONY: all
all: mobius.so liouville.so

.PHONY: test
test: mobius.so
	$(PYTHON) -m unittest mobius_test.py

.PHONY: test_liouville
test_liouville: liouville.so
	$(PYTHON) -m unittest liouville_test.py

.PHONY: test_all
test_all: mobius.so liouville.so
	$(PYTHON) -m unittest mobius_test.py liouville_test.py

.PHONY: clean
clean:
	rm -f mobius.so liouville.so
	rm -rf __pycache__/
