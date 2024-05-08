<img src="./img/tags/GAMECHANGER-NoPentagon_RGB@3x.png" align="right"
     alt="Mission Vision Icons" width="300" >

<h1>
<img src="./img/icons/RPA.png" alt="Data Engineering" width="70" aling="left"  >
     Data Engineering
</h1> 

`gamechanger-parser` is an isolated feature of the `gamechanger-data` ingestion pipeline. This parser was created to be a stand alone sharable tool; to be set up as a Docker container, python venv or importable package across Advana Databricks. 

To see all repositories [gamechanger](https://github.com/dod-advana/gamechanger)

The aim of this repository is to provide an effective tool for the extraction of text and metadata from documents for; general text extraction, gamechanger-policy specific usage, or a foundation for other platforms with the ability to use your own Machine Learning Model.

In the example script/notebook you will find an example run of our parser. Defining your data input and deciding wether to use the 
- general text extractor: `writer`
- GAMECHANGER Policy's parse + additional embeddings: `policy_text_pipeline`

After setting up your environment using one of the two setup options below, you can use the example.py or example.ipynb files to run an example parsing job. You can also view the inputs and outputs of this job in the folders example_input and example_output respectively.

## Docker setup
Follow `config/dockerConf/README.md`

## Conda env setup
Follow `config/venvSetup.md` 


## Unfinished:
1. Getting the gc-parser wheel uploaded to Advana's Mirror and providing an example of how to import the parser on Databricks

## License
See LICENSE.md