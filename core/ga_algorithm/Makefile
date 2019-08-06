all: build

# into package folder
build:
ifeq ($(OS),Windows_NT)
	-rename __init__.py .__init__.py
	python setup.py build_ext --inplace
	-rename .__init__.py __init__.py
else
	-mv __init__.py .__init__.py
	python3 setup.py build_ext --inplace
	-mv .__init__.py __init__.py
endif

clean:
ifeq ($(OS),Windows_NT)
	-rename .__init__.py __init__.py
	-del *.pyd /q
	-rd build /s /q
	-del Adesign\*.c /q
	-del Adesign\*.cpp /q
else
	-mv .__init__.py __init__.py
	-find . -name '*.so' -delete
	-find . -name '*.c' -delete
	-find . -name '*.cpp' -delete
	-rm -fr build
endif
