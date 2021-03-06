# Build spacetime Python extension (even when the timestamp is clean):
#   make
# Run Python tests:
#   make pytest
# Run Google tests:
#   make gtest
# Run all tests:
#   make test
# Build verbosely:
#   make VERBOSE=1
# Build with clang-tidy
#   make USE_CLANG_TIDY=ON

HIDE_SYMBOL ?= OFF
DEBUG_SYMBOL ?= ON
USE_CLANG_TIDY ?= OFF
CMAKE_BUILD_TYPE ?= Release
SPACETIME_ROOT ?= $(shell pwd)
MODMESH_ROOT ?= $(SPACETIME_ROOT)/build/modmesh
NB_ARGS ?=
CMAKE_ARGS ?=
VERBOSE ?=
GDB ?=
ifeq ($(CMAKE_BUILD_TYPE), Debug)
	BUILD_PATH ?= build/dbg37
else
	BUILD_PATH ?= build/dev37
endif

PYTHON ?= $(shell which python3)

PYTEST ?= $(shell which py.test-3)
ifeq ($(PYTEST),)
	PYTEST := $(PYTHON) -m pytest
endif

PYTEST_OPTS ?=
ifneq ($(VERBOSE),)
	PYTEST_OPTS := $(PYTEST_OPTS) -v -s
endif

ifneq ($(GDB),)
	PYTEST := gdb --args $(PYTEST)
endif

pyextsuffix := $(shell python3-config --extension-suffix)

.PHONY: default
default: buildext

.PHONY: clean
clean:
	make -C $(BUILD_PATH) clean

.PHONY: cmakeclean
cmakeclean:
	rm -rf $(BUILD_PATH)

.PHONY: test
test: gtest pytest

.PHONY: gtest
gtest: $(BUILD_PATH)/gtests/libst_gtests
	$(BUILD_PATH)/gtests/libst_gtests

.PHONY: pytest
pytest: $(SPACETIME_ROOT)/libst/_libst$(pyextsuffix)
	env PYTHONPATH=$(SPACETIME_ROOT):$(MODMESH_ROOT) $(PYTEST) $(PYTEST_OPTS) tests/

.PHONY: cmake
cmake: $(BUILD_PATH)/Makefile

$(BUILD_PATH)/gtests/libst_gtests: $(BUILD_PATH)/Makefile
	make -C $(BUILD_PATH) VERBOSE=$(VERBOSE) libst_gtests
	touch $@

$(BUILD_PATH)/_libst$(pyextsuffix): $(BUILD_PATH)/Makefile
	make -C $(BUILD_PATH) VERBOSE=$(VERBOSE) _libst
	touch $@

$(SPACETIME_ROOT)/libst/_libst$(pyextsuffix): $(BUILD_PATH)/_libst$(pyextsuffix)
	make -C $(BUILD_PATH) VERBOSE=$(VERBOSE) _libst_py
	touch $@

.PHONY: buildext
buildext: $(SPACETIME_ROOT)/libst/_libst$(pyextsuffix)

.PHONE: notebook
notebook: buildext
	cd .. && env PYTHONPATH=$(SPACETIME_ROOT):$(MODMESH_ROOT) jupyter notebook $(NB_ARGS)

$(BUILD_PATH)/Makefile: CMakeLists.txt Makefile
	mkdir -p $(BUILD_PATH) ; \
	cd $(BUILD_PATH) ; \
	cmake $(SPACETIME_ROOT) \
		-DCMAKE_INSTALL_PREFIX=$(SPACETIME_ROOT) \
		-DCMAKE_BUILD_TYPE=$(CMAKE_BUILD_TYPE) \
		-DHIDE_SYMBOL=$(HIDE_SYMBOL) \
		-DDEBUG_SYMBOL=$(DEBUG_SYMBOL) \
		-DUSE_CLANG_TIDY=$(USE_CLANG_TIDY) \
		-DLINT_AS_ERRORS=ON \
		$(CMAKE_ARGS)
