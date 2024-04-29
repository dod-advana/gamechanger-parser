
# Project Setup and Testing Instructions

## 1. Creating the Wheel File

To create a `.whl` file for the project, run the following command:

```bash
python setup.py bdist_wheel
```

This command will:

- Build the package.
- Download dependencies specified in `config/requirements.txt`.
- Include the `parsers/` folder within the package.

## 2. Testing the Wheel File

As of April 1, 2024, Databricks is using Python 3.8.10. To ensure compatibility, create a virtual environment using the same Python version and test the wheel file within this environment.

### Setting up the Virtual Environment

Download Python 3.8.10 from the [official Python release page](https://www.python.org/downloads/release/python-3810/).

Create and activate a virtual environment:

```bash
py -m venv dbksVenv
source dbksVenv/Scripts/activate
pip install --upgrade pip
```

### Installing the Wheel File

Install the wheel file using pip:

```bash
pip install ./whl_creation_output/dist/[file-name].whl
```

### Common Errors During Installation

- If you encounter an error stating that Microsoft Visual C++ 14.0 or greater is required, refer to [this Stack Overflow post](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst) for a solution.

## Running the Test Script

Execute the test script to ensure everything is set up correctly:

```bash
py testVenv.py
```

### Common Errors During Test Execution

- If you get an `OSError` indicating that the Tesseract library cannot be loaded, ensure that Tesseract is installed on your computer. Tesseract is a dependency of `ocrmypdf`. Installation instructions can be found on the [Tesseract GitHub page](https://github.com/UB-Mannheim/tesseract/wiki).

- After installing Tesseract, verify its installation by running `tesseract --version` in your command prompt or terminal. Ensure that Leptonica is also listed in the output.

- If there are issues related to Leptonica, verify that the following files are present in the Tesseract installation directory (e.g., `C:\Users\[user]\AppData\Local\Programs\Tesseract-OCR`):
  - `liblept-5.dll` (Windows)
  - `liblept*.dylib` (macOS)
  - `liblept*.so` (Linux/BSD)

- Refer to the `example-leptonica.py` script for an example of how to set the Leptonica path. You may need to adjust the path in `gamechanger-parser/devTools/whl/dbksVenv/Lib/site-packages/ocrmypdf/leptonica.py` accordingly.
