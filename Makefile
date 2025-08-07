
OS := $(shell uname -s)
ifeq ($(OS),Windows_NT)
	include Makefile.windows.mk
else
	include Makefile.linux.mk
endif

run:
	@make init

env:
	@make venv

require:
	@make req