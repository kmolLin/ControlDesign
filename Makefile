all: build

# into package folder
build:
ifeq ($(OS),Windows_NT)
	python setup.py build_ext --inplace
else
	python3 setup.py build_ext --inplace
endif

clean:
ifeq ($(OS),Windows_NT)
	-del *.pyd /q
	-rd build /s /q
	-del Adesign\*.c /q
	-del Adesign\*.cpp /q
else
	-find . -name '*.so' -delete
	-find . -name '*.c' -delete
	-find . -name '*.cpp' -delete
	-rm -fr build
endif
