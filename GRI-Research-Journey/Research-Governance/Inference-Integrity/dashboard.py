"""Standalone GRI research dashboard. Synthetic telemetry only; no production wiring."""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
import random
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from governance import GRIGovernanceMLPlatform, replay

def build_telemetry(count: int = 250, seed: int = 20261025) -> pd.DataFrame:
    rng = random.Random(seed)
    platform = GRIGovernanceMLPlatform({"race_ethnicity": ["zip_code"]})
    rows = []
    for i in range(count):
        dti = round(rng.uniform(0.1, 0.7), 3)
        score = round(rng.uniform(0.1, 0.95), 3)
        features = {"debt_to_income": dti, "zip_code": "SYNTHETIC"}
        model = lambda _features, value=score: value
        result = platform.evaluate(f"SYNTHETIC-{i:05d}", features, model, "mock-v1",
                                   {"zip_code": -0.30 if i % 5 == 0 else 0.01})
        record = platform.ledger.snapshot()[-1]
        rows.append({
            "prediction_id": result.prediction_id,
            "timestamp": (datetime(2026, 10, 25, tzinfo=timezone.utc) -
                          timedelta(minutes=i * 3)).isoformat(),
            "decision": result.decision,
            "replay_status": replay(record, model, "mock-v1"),
            "policy_note": "; ".join(result.reasons) or "None",
            "proxy_screen": "; ".join(result.proxy_review_flags) or "No screening flag",
            "human_review": "NOT_IMPLEMENTED",
            "risk_score": result.raw_score,
            "block_index": record.index,
            "ledger_hash": record.record_hash,
        })
    df = pd.DataFrame(rows)
    df.attrs["chain_verified"] = platform.ledger.verify(rows[-1]["ledger_hash"])
    return df

def make_app() -> Dash:
    df = build_telemetry()
    app = Dash(__name__, title="GRI | ML Governance Research")
    dark = {"backgroundColor": "#0f172a", "color": "#f8fafc", "padding": "24px",
            "fontFamily": "Arial, sans-serif"}
    card = {"backgroundColor": "#1e293b", "padding": "16px", "borderRadius": "8px"}
    metrics = [
        ("Synthetic records", str(len(df))),
        ("Score replay passes", str((df.replay_status == "PASS_SCORE_REPLAY_ONLY").sum())),
        ("Policy blocks", str((df.decision == "BLOCKED_BY_POLICY").sum())),
        ("Human reviews", "Not implemented"),
        ("Chain verification", "Passed" if df.attrs["chain_verified"] else "Failed"),
        ("Compliance certification", "Not assessed"),
    ]
    pie = px.pie(df, names="decision", hole=0.45, title="Synthetic policy outcomes")
    bars = px.histogram(df, x="risk_score", nbins=20, title="Synthetic risk score distribution")
    for fig in (pie, bars):
        fig.update_layout(paper_bgcolor="#1e293b", plot_bgcolor="#1e293b",
                          font_color="#f8fafc")
    app.layout = html.Div(style=dark, children=[
        html.H1("GRI | Inference Integrity and Institutional Accountability"),
        html.P("RESEARCH DEMONSTRATION · SYNTHETIC DATA · NOT LIVE TELEMETRY",
               style={"color": "#fbbf24", "fontWeight": "bold"}),
        html.P("Score replay is not full model reproducibility. Hash chaining is not immutable storage. No compliance rating is asserted."),
        html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(170px, 1fr))",
                        "gap": "12px"}, children=[
            html.Div(style=card, children=[html.P(name), html.H2(value)]) for name, value in metrics
        ]),
        html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
                        "gap": "12px", "marginTop": "16px"}, children=[
            html.Div(style=card, children=dcc.Graph(figure=pie)),
            html.Div(style=card, children=dcc.Graph(figure=bars)),
        ]),
        html.H2("Synthetic inference evidence"),
        dash_table.DataTable(
            data=df.drop(columns=["ledger_hash"]).to_dict("records"),
            columns=[{"name": c.replace("_", " ").title(), "id": c}
                     for c in df.columns if c != "ledger_hash"],
            page_size=10, sort_action="native", filter_action="native",
            style_table={"overflowX": "auto"},
            style_header={"backgroundColor": "#334155", "color": "white"},
            style_cell={"backgroundColor": "#1e293b", "color": "white",
                        "textAlign": "left", "padding": "8px", "maxWidth": "260px",
                        "overflow": "hidden", "textOverflow": "ellipsis"},
        ),
    ])
    return app

app = make_app()
server = app.server

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
