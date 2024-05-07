As of April 1, 2024, Databricks is using Python 3.8.10. To ensure compatibility, create a virtual environment using the same Python version and test the wheel file within this environment.

# Apple Silicon Mac Setup
### We use x86 emulation with the mac builtin rosetta to ensure packages build correctly.

1. Download a version of conda (miniconda is the smallest) https://docs.anaconda.com/free/miniconda/ \
check install worked with ```conda --version```

2. Create x64 environment with the correct version of python \
    ```CONDA_SUBDIR=osx-64 conda create -n gamechanger-parser python=3.8.10```

3. Activate environment \
    ```conda activate gamechanger-parser```

4. Add defaults x64 channel \
    ```conda config --prepend channels defaults/osx-64```

5. add conda-forge x64 channel \
    ```conda config --prepend channels conda-forge/osx-64```

6. Install tesseract and lxml with conda \
    ```conda install tesseract=4.1.1 lxml==4.9.4``` \
    verify with ```tesseract --version```

7. Run 
<br><br>
# Windows Setup

```bash
py -m venv gamechanger-parser
source gamechanger-parser/Scripts/activate
pip install --upgrade pip
```

---
# Install req.txt
```python -m pip install -r ./requirements.txt``` <br>

## To Use GAMECHANGER Specific Parser and Topic Models
```python -m pip install boto3```<br><br>
(must have s3 access to advana-data-zone)<br>
```python get_topic_model.py```

## Run Root Scripts
python script with venv <br>
or notebook with jup set up

### Windows Common Errors During Test Execution
---
- If you get an `OSError` indicating that the Tesseract library cannot be loaded, ensure that Tesseract is installed on your computer. Tesseract is a dependency of `ocrmypdf`. Installation instructions can be found on the [Tesseract GitHub page](https://github.com/UB-Mannheim/tesseract/wiki).

- After installing Tesseract, verify its installation by running `tesseract --version` in your command prompt or terminal. Ensure that Leptonica is also listed in the output.

- If there are issues related to Leptonica, verify that the following files are present in the Tesseract installation directory (e.g., `C:\Users\[user]\AppData\Local\Programs\Tesseract-OCR`):
  - `liblept-5.dll` (Windows)
  - `liblept*.dylib` (macOS)
  - `liblept*.so` (Linux/BSD)

- Refer to the `example-leptonica.py` script for an example of how to set the Leptonica path. You may need to adjust the path in `gamechanger-parser/devTools/whl/dbksVenv/Lib/site-packages/ocrmypdf/leptonica.py` accordingly.
