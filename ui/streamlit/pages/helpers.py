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

def style_savings_goals(df: pd.DataFrame):
    df = df.rename(columns={
        "name": "Goal Name",
        "goal_amount": "Target Amount",
        "amount": "Current Amount",
        "description": "Description"
    })
    df["Remaining"] = df["Target Amount"] - df["Current Amount"]
    def highlight_progress(row):
        """Koloruje wiersz bazując na procentowym postępie."""
        progress = row.get('Progress (%)', 0)
        styles = [''] * len(row)
        
        if progress >= 100:
            # Cel osiągnięty - zielone tło
            styles = ['background-color: #D1FAE5' if col != 'Progress (%)' else 'background-color: #D1FAE5; color: #065F46; font-weight: 700' for col in row.index]
        elif progress >= 75:
            # Blisko celu - jasny zielony
            styles = ['background-color: #ECFDF5' if col != 'Progress (%)' else 'background-color: #ECFDF5; color: #059669; font-weight: 600' for col in row.index]
        elif progress >= 50:
            # W połowie drogi - żółty
            styles = ['background-color: #FEF9C3' if col != 'Progress (%)' else 'background-color: #FEF9C3; color: #CA8A04; font-weight: 600' for col in row.index]
        elif progress >= 25:
            # Początek - pomarańczowy
            styles = ['background-color: #FED7AA' if col != 'Progress (%)' else 'background-color: #FED7AA; color: #C2410C; font-weight: 600' for col in row.index]
        else:
            # Mało postępu - czerwony akcent
            styles = ['background-color: #FEE2E2' if col != 'Progress (%)' else 'background-color: #FEE2E2; color: #DC2626; font-weight: 600' for col in row.index]
        
        return styles
    
    def format_currency(val):
        """Formatuje wartości walutowe."""
        try:
            return f"{float(val):.2f} zł"
        except:
            return val
    
    def format_percentage(val):
        """Formatuje wartości procentowe."""
        try:
            return f"{float(val):.1f}%"
        except:
            return val
    
    styled = (
        df.style
        .format({
            "Target Amount": format_currency,
            "Current Amount": format_currency,
            "Remaining": format_currency,
            "Progress (%)": format_percentage
        })
        .set_properties(**{
            "color": "#1F2937",
            "border-color": "#E5E7EB",
            "border-width": "0 0 1px 0",
            "border-style": "solid",
            "font-size": "14px",
            "text-align": "center",
            "padding": "14px 18px",
            "font-family": "'Inter', 'Segoe UI', sans-serif"
        })
        .set_properties(subset=['Goal Name'], **{
            "text-align": "left",
            "font-weight": "600"
        })
        .set_table_styles([
            {"selector": "thead th", "props": [
                ("background", "linear-gradient(135deg, #667EEA 0%, #764BA2 100%)"),
                ("color", "#FFFFFF"),
                ("font-weight", "600"),
                ("text-align", "center"),
                ("padding", "16px 18px"),
                ("border", "none"),
                ("font-size", "13px"),
                ("letter-spacing", "0.5px"),
                ("text-transform", "uppercase")
            ]},
            {"selector": "tbody tr:hover", "props": [
                ("transform", "scale(1.01)"),
                ("box-shadow", "0 4px 12px rgba(102, 126, 234, 0.15)"),
                ("transition", "all 0.2s ease")
            ]},
            {"selector": "", "props": [
                ("border-collapse", "separate"),
                ("border-spacing", "0"),
                ("border-radius", "12px"),
                ("overflow", "hidden"),
                ("box-shadow", "0 4px 6px rgba(0,0,0,0.1)")
            ]}
        ])
        .apply(highlight_progress, axis=1)
    )
    
    return styled
