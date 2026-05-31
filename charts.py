import plotly.graph_objects as go
import pandas as pd

# Light-theme palette (Bloomberg-style)
COLORS = {
    "teal":   "#2F6FD6",   # cobalt blue — primary accent
    "amber":  "#C2872F",   # amber — secondary series
    "up":     "#1E9E73",   # green — positive / good
    "red":    "#D6454D",   # red — negative / bad
    "bg":     "#ECEEF3",   # page background
    "card":   "#FFFFFF",   # card surface
    "text":   "#1B2536",   # primary text
    "muted":  "#697587",   # secondary text
    "grid":   "#E4E8EF",   # gridlines
    "hair":   "#DCE1E9",   # borders
    # legacy aliases used in app.py
    "blue":   "#2F6FD6",
    "orange": "#C2872F",
    "purple": "#1E9E73",
}


def _base_layout(unit: str = "") -> dict:
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["muted"], family="Inter, sans-serif", size=12),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            showgrid=True,
            zeroline=False,
            tickfont=dict(color=COLORS["muted"], size=11),
            showspikes=True,
            spikecolor="#AEB7C5",
            spikethickness=1,
            spikedash="dot",
            spikemode="across",
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            showgrid=True,
            zeroline=False,
            ticksuffix=f" {unit}" if unit else "",
            tickfont=dict(color=COLORS["muted"], size=11),
        ),
        margin=dict(l=58, r=24, t=10, b=38),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=COLORS["grid"],
            font=dict(
                family="JetBrains Mono, monospace",
                color=COLORS["text"],
                size=12,
            ),
        ),
        showlegend=False,
    )


def area_chart(
    df: pd.DataFrame,
    title: str,
    unit: str,
    color: str,
    step: bool = False,
    annotations: list[dict] | None = None,
) -> go.Figure:
    fig = go.Figure()
    rgb = _hex_to_rgb(color)
    shape = "hv" if step else "spline"
    smoothing = 0.0 if step else 0.6

    fig.add_trace(go.Scatter(
        x=df["tarih"],
        y=df["deger"],
        mode="lines",
        fill="tozeroy",
        fillcolor=f"rgba({rgb}, 0.13)",
        line=dict(color=color, width=2, shape=shape, smoothing=smoothing),
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

    fig.update_layout(**_base_layout(unit))
    return fig


def dual_area_chart(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    name1: str,
    name2: str,
    unit: str,
    color1: str,
    color2: str,
) -> go.Figure:
    """Two overlapping area series on one chart (FX tab)."""
    fig = go.Figure()
    rgb1, rgb2 = _hex_to_rgb(color1), _hex_to_rgb(color2)

    fig.add_trace(go.Scatter(
        x=df1["tarih"], y=df1["deger"],
        mode="lines", fill="tozeroy",
        fillcolor=f"rgba({rgb1}, 0.12)",
        line=dict(color=color1, width=2, shape="spline", smoothing=0.6),
        name=name1,
        hovertemplate=f"%{{x|%d.%m.%Y}}  <b>%{{y:.4f}}</b> ₺<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df2["tarih"], y=df2["deger"],
        mode="lines", fill="tozeroy",
        fillcolor=f"rgba({rgb2}, 0.09)",
        line=dict(color=color2, width=2, shape="spline", smoothing=0.6),
        name=name2,
        hovertemplate=f"%{{x|%d.%m.%Y}}  <b>%{{y:.4f}}</b> ₺<extra></extra>",
    ))

    layout = _base_layout("")
    layout["showlegend"] = True
    layout["legend"] = dict(
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor=COLORS["hair"],
        borderwidth=1,
        font=dict(color=COLORS["muted"], size=12),
        x=0.01, y=0.99,
        xanchor="left", yanchor="top",
    )
    layout["yaxis"]["tickprefix"] = "₺"
    fig.update_layout(**layout)
    return fig


def bar_chart(df: pd.DataFrame, title: str, unit: str) -> go.Figure:
    colors = [COLORS["red"] if v < 0 else COLORS["up"] for v in df["deger"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["tarih"],
        y=df["deger"],
        marker_color=colors,
        marker_line_width=0,
        name=title,
        hovertemplate=f"%{{x|%d.%m.%Y}}  <b>%{{y:.2f}}</b> {unit}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(unit))
    return fig


def correlation_heatmap(corr_df) -> go.Figure:
    labels = list(corr_df.columns)
    z = corr_df.values.tolist()
    text = [[f"{v:.2f}" for v in row] for row in corr_df.values]

    fig = go.Figure(go.Heatmap(
        z=z,
        x=labels,
        y=labels,
        text=text,
        texttemplate="%{text}",
        textfont=dict(
            size=12,
            family="JetBrains Mono, monospace",
            color=COLORS["text"],
        ),
        colorscale=[
            [0.0, COLORS["red"]],
            [0.5, "#EDEFF3"],
            [1.0, COLORS["up"]],
        ],
        zmin=-1, zmax=1,
        xgap=3, ygap=3,
        showscale=True,
        colorbar=dict(
            thickness=10,
            len=0.8,
            outlinewidth=0,
            tickfont=dict(color=COLORS["muted"], size=10),
        ),
        hovertemplate="%{y} ↔ %{x}: <b>ρ = %{text}</b><extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["muted"], family="Inter, sans-serif", size=12),
        xaxis=dict(tickfont=dict(color=COLORS["muted"], size=11), side="bottom"),
        yaxis=dict(tickfont=dict(color=COLORS["muted"], size=11), autorange="reversed"),
        margin=dict(l=70, r=24, t=10, b=50),
        hovermode="closest",
    )
    return fig


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r}, {g}, {b}"
