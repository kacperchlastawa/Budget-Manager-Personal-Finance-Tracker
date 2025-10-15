import pandas as pd
def style_dataframe(df: pd.DataFrame):
    df = df.rename(columns={
        "amount": "Amount (zł)",
        "t_date": "Date",
        "category": "Category",
        "description": "Description",
        "type": "Type"
    })

    def color_amount_by_type(row):
        if row['Type'] == 'income':
            return ['color: #059669; font-weight: 600' if col == 'Amount (zł)' else '' for col in row.index]
        elif row['Type'] == 'expense':
            return ['color: #DC2626; font-weight: 600' if col == 'Amount (zł)' else '' for col in row.index]
        else:
            return ['' for _ in row.index]

    styled = (
        df.style
        .format({
            "Amount (zł)": "{:.2f}",
            "Date": lambda x: pd.to_datetime(x).strftime("%Y-%m-%d") if pd.notnull(x) else "-"
        })
        .set_properties(**{
            "background-color": "#FFFFFF",
            "color": "#334155",
            "border-color": "#E2E8F0",
            "border-width": "0 0 1px 0",
            "border-style": "solid",
            "font-size": "14px",
            "text-align": "left",
            "padding": "14px 18px",
            "font-family": "'Inter', 'Segoe UI', sans-serif"
        })
        .set_table_styles([
            {"selector": "thead th", "props": [
                ("background", "linear-gradient(135deg, #667EEA 0%, #764BA2 100%)"),
                ("color", "#FFFFFF"),
                ("font-weight", "600"),
                ("text-align", "left"),
                ("padding", "16px 18px"),
                ("border", "none"),
                ("font-size", "13px"),
                ("letter-spacing", "0.3px")
            ]},
            {"selector": "tbody tr:nth-child(even)", "props": [
                ("background-color", "#F8FAFC")
            ]},
            {"selector": "tbody tr:hover", "props": [
                ("background-color", "#EEF2FF"),
                ("box-shadow", "inset 3px 0 0 #667EEA")
            ]},
            {"selector": "", "props": [
                ("border-collapse", "separate"),
                ("border-spacing", "0"),
                ("border-radius", "8px"),
                ("overflow", "hidden"),
                ("box-shadow", "0 4px 6px rgba(0,0,0,0.07)")
            ]}
        ])
        .apply(color_amount_by_type, axis=1)
    )
    return styled