<img src="./img/tags/GAMECHANGER-NoPentagon_RGB@3x.png" align="right"
     alt="Mission Vision Icons" width="300" >

<h1>
<img src="./img/icons/RPA.png" alt="Data Engineering" width="70" aling="left"  >
     Data Engineering
</h1> 

`gamechanger-parser` focuses on the parsing work of gamechanger. To see all repositories [gamechanger](https://github.com/dod-advana/gamechanger)

The aim of this repository is to provide an effective tool for the extraction of text and metadata from documents for further use in the gamechanger tool.

After setting up the environment using one of the two setup options below you can use the example.py or example.ipynb files to run an example parsing job. You can also view the inputs and outputs of this job in the folders example_input and example_output respectively.

## Docker setup
Follow `config/dockerConf/README.md`

## Conda env setup
Follow `config/venvSetup.md` 


## TODO:
1. Refactor files into a more succinct form
2. Add more granular error handling for each of the specific types of errors for a document and how many succeed/fail in a batch
3. Add pytests to protect code
4. Make overall package pip installable

## License
See LICENSE.md