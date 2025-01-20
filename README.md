# michaelis-menten-animated
Attempt at practicing numpy, pandas, and plotly to create a visualization of Michaelis-Menten kinetics with an existing dataset

Edit 1: Changed focus from matplotlib to plotly to use the nice properties of javascript integration

## Process
1. Create visualization of existing data
2. Fit nonlinear model per M-M derivation
3. Create interactive plots of data with different models

![image](https://github.com/user-attachments/assets/3f2d2041-34c7-49cf-be29-99a180a50bf5)

Part of a series of projects trying to replicate what I can do in R with Python (to refamiliarize myself with it)

## Dataset information
Sourced from R package nlstools: https://cran.r-project.org/web/packages/nlstools/nlstools.pdf

Labeled in repository as "vmkmki_mmdata.csv"

### Per them:

vmkmki is a data frame with 3 columns (S: concentration of substrat, I: concentration of inhibitor, v: reaction rate)

#### Source:
These datasets were provided by the French research unit INRA UMR1233.

## Final Output
Found in michaelis_menten_w_inhibition.ipynb. Click the link associated with the repo to see the interactive graphs and outputs in action without having to run the notebook locally.

## Deployment
Deployed on Render using the steps from this repo: https://github.com/thusharabandara/dash-app-render-deployment (very thankful for it)
