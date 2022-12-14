from collections import abc

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tlab_analysis.photo_luminescence as pl


def create_figure(wrs: abc.Iterable[pl.WavelengthResolved], log_y: bool) -> go.Figure:
    df = pd.concat([wr.df for wr in wrs])
    range_y = np.array(
        [df["intensity"][np.isclose(df["time"], 0.0)].min(), df["intensity"].max()]
    )
    fig = (
        px.line(
            df,
            x="time",
            y="intensity",
            color="name",
            color_discrete_sequence=px.colors.qualitative.Set1,
            log_y=log_y,
        )
        .update_traces(
            hovertemplate=""
            "Time: %{x:.3g} ns<br>"
            "Intensity: %{y:.4g}<br>"
            "<extra></extra>"
        )
        .update_layout(
            legend=dict(font=dict(size=14), yanchor="top", y=-0.15, xanchor="left", x=0)
        )
        .update_xaxes(
            title_text="<b>Time (ns)</b>",
        )
        .update_yaxes(
            title_text="<b>Intensity (arb. units)</b>",
            range=(np.log10(range_y) if log_y else range_y) * [1.0, 1.05],
        )
    )
    return fig


def add_fitting_curve(
    fig: go.Figure, wrs: abc.Iterable[pl.WavelengthResolved]
) -> go.Figure:
    return fig.add_traces(
        [
            go.Scatter(
                x=wr.df["time"],
                y=wr.df["fit"],
                line=dict(color="black"),
                name=f"Double Exponential Approximation "
                f"a : b = {wr.df.attrs['fit']['a']}:{wr.df.attrs['fit']['b']}, "
                f"τ₁ = {wr.df.attrs['fit']['tau1']:.3g} ns, "
                f"τ₂ = {wr.df.attrs['fit']['tau2']:.3g} ns",
            )
            for wr in wrs
            if "fit" in wr.df.attrs
        ]
    )
