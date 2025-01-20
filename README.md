# michaelis-menten-animated
Attempt at practicing numpy, pandas, and plotly to create a visualization of Michaelis-Menten kinetics with an existing dataset

Edit 1: Changed focus from matplotlib to plotly to use the nice properties of javascript integration

## Project Structure 

The project contains the following files:

- **`project_exploration.ipynb`**: This notebook contains the exploratory code used in the production of the interactive plots. (Note: This creates 3 separate interactive plots)
  
- **`michaelis_menten_w_inhibition.ipynb`**: This file is a cleaned up version of the `project_exploration.ipynb`.

- **`combined_dash_app.ipynb`**: This notebook combines the three separate interactive plots into one combined Dash app for deployment.

- **`app.py`**: Script version of `combined_dash_app.ipynb` for Render deployment.

- **`requirements.txt`**: This file contains the dependencies used for creating and running this script. Created for Render deployment.

- **`vmkmki_mmdata.csv`**:
  - Sourced from R package nlstools: https://cran.r-project.org/web/packages/nlstools/nlstools.pdf
  - vmkmki is a data frame with 3 columns (S: concentration of substrate, I: concentration of inhibitor, v: reaction rate)
  - These datasets were provided by the French research unit INRA UMR1233.

- **`README.md`**: This file contains an overview of the project and additional information.

## Process
1. Create visualization of existing data
2. Fit nonlinear model per M-M derivation
3. Create interactive plots of data with different models

![image](https://github.com/user-attachments/assets/3f2d2041-34c7-49cf-be29-99a180a50bf5)

Part of a series of projects trying to replicate what I can do in R with Python (to refamiliarize myself with it)

## Final Output
Found in michaelis_menten_w_inhibition.ipynb. Click the link associated with the repo to see the interactive graphs and outputs in action without having to run the notebook locally.

## Deployment
Deployed on Render using the steps from this repo: https://github.com/thusharabandara/dash-app-render-deployment (very thankful for it)
