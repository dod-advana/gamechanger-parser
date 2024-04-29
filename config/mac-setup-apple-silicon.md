# Apple Silicon Mac Setup
### We use x86 emulation with the mac builtin rosetta to ensure packages build correctly.

1. Download a version of conda (miniconda is the smallest) https://docs.anaconda.com/free/miniconda/ \
check install worked with ```conda --version```

2. Create x64 environment with the correct version of python \
    ```CONDA_SUBDIR=osx-64 conda create -n gamechanger-rosetta python=3.8.10```

3. Activate environment \
    ```conda activate gamechanger-rosetta```

4. Add defaults x64 channel \
    ```conda config --prepend channels defaults/osx-64```

5. add conda-forge x64 channel \
    ```conda config --prepend channels conda-forge/osx-64```

7. Install tesseract and lxml with conda \
    ```conda install tesseract=4.1.1 lxml==4.9.4``` \
    verify with ```tesseract --version```

8. Install requirements with pip \
    ```pip install -r ./config/requirements.txt```
