# avalanche-ds
This repository contains the code and files related to the Data Science exercise developed as part of the job interview process for Avalanche Insights.

## Requirements
* Interpreter: Python 3.8
* Have Conda installed locally (see [here](https://docs.conda.io/en/latest/) for installation instructions)
* Have Jupyter Lab installed locally (see [here](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) for installation instructions)


## Folder structure

````
├── README.md
├── artifacts
│   ├── X.joblib
│   ├── lda_model.joblib
│   └── vectorizer.joblib
├── data
│   └── coded_response_dataframe.pkl
├── images
│   └── architecture.png
├── requirements.txt
├── src
│   ├── 1-exploratory_data_analysis.ipynb
│   ├── 2-topic_modeling.ipynb
│   ├── 3-sentiment_analysis.ipynb
│   ├── ml_utils.py
│   ├── nlp_pipeline.py
│   └── utils.py
└── workplan
    └── workplan.md
````

## Instructions

To properly run this notebook, please follow these steps:

1. Clone this repository and navigate to the root folder. Once there, set up a conda environment named `ds-interview`

````
$  conda create -n ds-interview python=3.8
````

2. Activate the virtual environment
````
$ conda activate ds-interview
````

3. Install all packages in `requirements.txt` (make sure you are at the root folder)

````
$ python3 -m pip install -r requirements.txt
````

4. Install the `ipykernel` module, which provides the IPython kernel for Jupyter

````
$ python3 -m pip install ipykernel
````

5. Add the enviornment `ds-interview` into Jupyer Notebooks

````
$ python3 -m ipykernel install --user --name=ds-interview
````

6. Start a jupyter lab server and connect to the jupyter notebook instance on your browser

````
$ jupyter lab
````

7. Select the `ds-interview` kernel at the top right hand corner in the Jupyter Lab interface.

8. Open the notebook you want to explore by navigating to the `src` directory.
