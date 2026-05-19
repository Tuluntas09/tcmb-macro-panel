import plotly.graph_objects as go
import pandas as pd


COLORS = {
    "primary": "#E63946",
    "secondary": "#457B9D",
    "bg": "#1D1D2E",
    "grid": "#2E2E42",
    "text": "#F1FAEE",
}


def _base_layout(title: str, unit: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(color=COLORS["text"], size=16)),
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["text"]),
        xaxis=dict(gridcolor=COLORS["grid"], showgrid=True),
        yaxis=dict(gridcolor=COLORS["grid"], showgrid=True, ticksuffix=f" {unit}"),
        margin=dict(l=40, r=20, t=50, b=40),
        hovermode="x unified",
    )


def line_chart(df: pd.DataFrame, title: str, unit: str, color: str = None) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["tarih"],
        y=df["deger"],
        mode="lines",
        line=dict(color=color or COLORS["primary"], width=2),
        name=title,
        hovertemplate=f"%{{y:.2f}} {unit}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(title, unit))
    return fig
