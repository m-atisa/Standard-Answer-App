# %%
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
# %%
from django.db import models
from django.views.generic.base import TemplateView
# %%

def AmericanStates(csv_file_path, name):

    states = pd.read_csv(csv_file_path)

    fig = go.Figure(
          data=go.Choropleth(
               locations=states[states.columns[0]],
               z=states[states.columns[1]].astype(float),
               locationmode="USA-states",
               colorscale="Reds",
               colorbar_title="Millions USD",
        )
    )  

    fig.update_layout(
          title_text=name,
          geo=dict(
               scope="usa",
               projection=go.layout.geo.Projection(type="albers usa"),
               showlakes=True,
               lakecolor="rgb(255, 255, 255)",
        ),
    )  

    plot_div = plot(fig, include_plotlyjs=False, output_type="div", show_link=False, link_text="")
    return plot_div
