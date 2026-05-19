import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "red":    "#E63946",
    "blue":   "#457B9D",
    "teal":   "#2A9D8F",
    "orange": "#F4A261",
    "purple": "#A8DADC",
    "bg":     "#1D1D2E",
    "grid":   "#2E2E42",
    "text":   "#F1FAEE",
    "muted":  "#8D99AE",
}


def _base_layout(title: str, unit: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(color=COLORS["text"], size=15)),
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["text"], family="Inter, sans-serif"),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            showgrid=True,
            zeroline=False,
            tickfont=dict(color=COLORS["muted"]),
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            showgrid=True,
            zeroline=False,
            ticksuffix=f" {unit}" if unit else "",
            tickfont=dict(color=COLORS["muted"]),
        ),
        margin=dict(l=50, r=20, t=50, b=40),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )


def area_chart(
    df: pd.DataFrame,
    title: str,
    unit: str,
    color: str,
    annotations: list[dict] | None = None,
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["tarih"],
        y=df["deger"],
        mode="lines",
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(color)}, 0.12)",
        line=dict(color=color, width=2),
        name=title,
        hovertemplate=f"%{{x|%d.%m.%Y}}  <b>%{{y:.2f}}</b> {unit}<extra></extra>",
    ))

    if annotations:
        for ann in annotations:
            fig.add_vline(
                x=ann["date"],
                line=dict(color=COLORS["muted"], width=1, dash="dot"),
                annotation_text=ann["label"],
                annotation_font=dict(color=COLORS["muted"], size=10),
                annotation_position="top left",
            )

    fig.update_layout(**_base_layout(title, unit))
    return fig


def bar_chart(df: pd.DataFrame, title: str, unit: str) -> go.Figure:
    colors = [COLORS["red"] if v < 0 else COLORS["teal"] for v in df["deger"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["tarih"],
        y=df["deger"],
        marker_color=colors,
        name=title,
        hovertemplate=f"%{{x|%d.%m.%Y}}  <b>%{{y:.2f}}</b> {unit}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(title, unit))
    return fig


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r}, {g}, {b}"
