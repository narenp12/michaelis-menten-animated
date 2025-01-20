# %%
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import statsmodels.api as sm
import statsmodels.formula.api as smf

# %%
data = pd.read_csv("vmkmki_mmdata.csv")
data = data.rename(columns={"S": "s", "I": "i"})


# %%
def noncompetitive_inhibition(vmax, s, m_const, i, i_const):
    alpha = 1 + i / i_const
    return ((vmax / alpha) * s) / (s + m_const)


def competitive_inhibition(vmax, s, m_const, i, i_const):
    alpha = 1 + i / i_const
    return (vmax * s) / (alpha * m_const + s)


def uncompetitive_inhibition(vmax, s, m_const, i, i_const):
    alpha = 1 + i / i_const
    return ((vmax / alpha) * s) / ((m_const / alpha) + s)


# %%
def km_solve(df):
    v = 1 / df["v"]
    v = v.replace({np.inf: 0})
    s = 1 / df["s"]
    s = s.replace({np.inf: 0})

    linmod = sm.OLS(v, s).fit()
    return linmod.params.iloc[0] * df["v"]


# %%
m_const = km_solve(data)
i_const = m_const * (data["i"] / (m_const - 1))

# %%
data = data.eval(
    """ 
k_m = @m_const
k_i = @i_const
"""
)
obs = data[data["s"] > 0]

# %%
ni_v = noncompetitive_inhibition(obs["v"], obs["s"], obs["k_m"], obs["i"], obs["k_i"])
nc_obs = obs.eval("ni_v = @ni_v").dropna()

# %%
ci_v = competitive_inhibition(obs["v"], obs["s"], obs["k_m"], obs["i"], obs["k_i"])
c_obs = obs.eval("ci_v = @ci_v").dropna()

# %%
ui_v = uncompetitive_inhibition(obs["v"], obs["s"], obs["k_m"], obs["i"], obs["k_i"])
u_obs = obs.eval("ui_v = @ui_v").dropna()

# %%
app_combined = Dash(__name__)
server = app_combined.server

app_combined.layout = html.Div(
    [
        html.H1("Michaelis-Menten Kinetics with Different Inhibition Types"),
        dcc.Tabs(
            id="tabs",
            value="tab-1",  # Default selected tab
            children=[
                dcc.Tab(
                    label="Noncompetitive Inhibition",
                    value="tab-1",
                    children=[
                        html.Label("Select concentration of inhibitor:"),
                        dcc.Dropdown(
                            id="i-dropdown-nc",
                            options=[
                                {"label": val, "value": val}
                                for val in nc_obs["i"].unique()
                            ],
                            value=nc_obs["i"].unique()[0],
                        ),
                        dcc.Graph(id="scatter-plot-nc"),
                    ],
                ),
                dcc.Tab(
                    label="Competitive Inhibition",
                    value="tab-2",
                    children=[
                        html.Label("Select concentration of inhibitor:"),
                        dcc.Dropdown(
                            id="i-dropdown-c",
                            options=[
                                {"label": val, "value": val}
                                for val in c_obs["i"].unique()
                            ],
                            value=c_obs["i"].unique()[0],
                        ),
                        dcc.Graph(id="scatter-plot-c"),
                    ],
                ),
                dcc.Tab(
                    label="Uncompetitive Inhibition",
                    value="tab-3",
                    children=[
                        html.Label("Select concentration of inhibitor:"),
                        dcc.Dropdown(
                            id="i-dropdown-u",
                            options=[
                                {"label": val, "value": val}
                                for val in u_obs["i"].unique()
                            ],
                            value=u_obs["i"].unique()[0],
                        ),
                        dcc.Graph(id="scatter-plot-u"),
                    ],
                ),
            ],
        ),
    ]
)


# Callbacks to update the plots for each inhibition type
@app_combined.callback(
    Output("scatter-plot-nc", "figure"), [Input("i-dropdown-nc", "value")]
)
def update_plot_nc(selected_i):
    filtered_data = nc_obs[nc_obs["i"] == selected_i]
    fig = px.scatter(
        filtered_data,
        x=np.log(filtered_data["s"]),
        y="ni_v",
        color="s",
        title=f"Scatter plot for inhibitor concentration = {selected_i}",
        labels={
            "ni_v": "Reaction velocity (v)",
            "x": "Log of substrate concentration",
            "s": "Substrate concentration (s)",
        },
        trendline="ols",
        trendline_options=dict(log_x=True),
    )
    return fig


@app_combined.callback(
    Output("scatter-plot-c", "figure"), [Input("i-dropdown-c", "value")]
)
def update_plot_c(selected_i):
    filtered_data = c_obs[c_obs["i"] == selected_i]
    fig = px.scatter(
        filtered_data,
        x=np.log(filtered_data["s"]),
        y="ci_v",
        color="s",
        title=f"Scatter plot for inhibitor concentration = {selected_i}",
        labels={
            "ci_v": "Reaction velocity (v)",
            "x": "Log of substrate concentration",
            "s": "Substrate concentration (s)",
        },
        trendline="ols",
        trendline_options=dict(log_x=True),
    )
    return fig


@app_combined.callback(
    Output("scatter-plot-u", "figure"), [Input("i-dropdown-u", "value")]
)
def update_plot_u(selected_i):
    filtered_data = u_obs[u_obs["i"] == selected_i]
    fig = px.scatter(
        filtered_data,
        x=np.log(filtered_data["s"]),
        y="ui_v",
        color="s",
        title=f"Scatter plot for inhibitor concentration = {selected_i}",
        labels={
            "ui_v": "Reaction velocity (v)",
            "x": "Log of substrate concentration",
            "s": "Substrate concentration (s)",
        },
        trendline="ols",
        trendline_options=dict(log_x=True),
    )
    return fig


# Run the combined app
if __name__ == "__main__":
    app_combined.run_server(debug=True)
