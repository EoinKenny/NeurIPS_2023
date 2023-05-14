# ICML_2023
For Reviewers

Hello,

This repo contains all the code from our experiments.

You will need to download the relevant datasets.

However, to help reproduce some results faster, we did upload the CSV data files for the Breast Cancer dataset and the German Credit dataset.

All you need to do is:

```
conda create --name semifactual
conda activate semifactual
conda install -c anaconda pandas
conda install -c anaconda seaborn
conda install -c anaconda scikit-learn
conda install -c conda-forge tqdm
conda install -c conda-forge jsonschema
conda install -c conda-forge imbalanced-learn
conda install pytorch::pytorch torchvision torchaudio -c pytorch
conda install -c conda-forge tensorboard
conda install -c conda-forge cvxpy
```

Then change into either the breast cancer folder of the german credit folder and run
```
python main.py
```
And the results will reproduce. 

You need to make a figs and DiCE_Xps folder in each dataset directory before running the main.py file.

You can view them in the Figs folder, but note they will be lineplots instead of the type in the paper.


