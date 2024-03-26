1) Create whl
```python setup.py bdist_wheel```
- Builds package, compiling any extension if neccesary
- Bundle the compiled versions and other necessary files into a '.whl' file
- Store the wheel file in a 'dist' directory project

2) Update table for version control
3) Upload to s3

## Whl tester
```python -m venv venv```
```source venv/Scripts/activate```

```
shell
pip install –upgrade pip
pip install setuptools
tar -xzvf setuptools-60.5.0.tar.gz
cd setuptools-60.5.0
python3 setup.py install

```

<!-- TODO: Test .whl -->
```pip install ./whl_creation_output/dist/gc_parser_2024_03_25T15_46-1.0.0-py3-none-any.whl```

## Common Errors

Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst