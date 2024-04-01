1) Create whl
```python setup.py bdist_wheel```
- Builds package, compiling any extension if neccesary
- Bundle the compiled versions and other necessary files into a '.whl' file
- Store the wheel file in a 'dist' directory project

2) Update table for version control
3) Upload to s3

## Whl tester

Databricks is using 3.8.10 as of 1 Apr 2024
https://www.python.org/downloads/release/python-3810/

```py -m venv dbksVenv```
```source dbksVenv/Scripts/activate```
```pip install --upgrade pip```

<!-- TODO: Test .whl -->
```pip install ./whl_creation_output/dist/[file-name].whl```

## Common Errors

Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst