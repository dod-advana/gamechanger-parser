# Project Setup and Testing Instructions
### Creating venv steps are in root config/ folder ! Just stop before req.txt download and follow these steps instead

## 1. Creating the Wheel File

To create a `.whl` file for the project, run the following command:

```bash
python setup.py bdist_wheel
```

This command will:

- Build the package.
- Package dependencies specified in root `config/requirements.txt`.
- Include the root `policy_analytics_parser/` folder within the package.

## 2. Installing the Wheel File

Install the wheel file using pip:

```python -m pip install ./whl_creation_output/dist/[file-name].whl ```

### (Windows) Common Errors During Installation

- If you encounter an error stating that Microsoft Visual C++ 14.0 or greater is required, refer to [this Stack Overflow post](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst) for a solution.

## To Use GAMECHANGER Specific Parser and Topic Models
```python -m pip install boto3```<br><br>
(must have s3 access to advana-data-zone)<br>
```python ../../config/get_topic_model.py```


## That's it! Can return to root and run the parser python script!

 <br><br>
# UploadWhls3

 - Once whl_creation_output/ is created, can run ```python whlLocalExract.py``` to copy wheel to a local folder to share with cyber team and save publically.