from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure as fig
import numpy as np
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']

def plot_transactions_by_category(data):
    if data.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Brak danych do wyświetlenia', 
                ha='center', va='center', fontsize=16, color='gray')
        ax.axis('off')
        return fig
    
    fig, ax = plt.subplots(figsize=(12,8))

    if len(data) > 6:
        top_data = data.head(6).copy()
        other_sum = data.iloc[6:]['total'].sum()
        if other_sum > 0:
            other_row = pd.DataFrame([{'category': 'The rest', 'total':other_sum}])
            plot_data = pd.concat([top_data,other_row])
        else:
            plot_data = top_data
    
    else :
        plot_data = data
    
    wedges, texts, autotexts = ax.pie(
        plot_data['total'],
        labels = None,
        autopct='%1.1f%%',
        colors = COLORS[:len(plot_data)],
        startangle=90,
        explode = [0.04] * len(plot_data)  
    )

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
        for text in texts:
            text.set_fontsize(11)
            text.set_weight('bold') 
            
    ax.set_title('Expenses by category',fontsize = 16, weight = 'bold', pad = 20)
    legend_labels = [f"{row['category']}: {row['total']:.2f} zł" 
                     for _, row in plot_data.iterrows()]

    ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5), 
              fontsize=10, frameon=True, shadow=True)
    
    plt.tight_layout()
    return fig

def balance_over_time(data,period = 'daily'):
    if data.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'Brak danych do wyświetlenia', 
                ha='center', va='center', fontsize=16, color='gray')
        ax.axis('off')
        return fig
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Main balance line
    ax.plot(data['period'], data['balance'], 
            marker='o', # points
            linewidth=2.5,        
            color='#45B7D1',     
            label='Saldo',
            markeredgewidth=2 #point edges width
            )        
    
    # Zero balance
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, 
               alpha=0.7, label='Zero', zorder=1)
    # red for values below 0 and green above
    ax.fill_between(data['period'], data['balance'], 0, 
                     where=(data['balance'] >= 0), 
                     alpha=0.3, color='green', 
                     label='Nadwyżka', interpolate=True)
    
    ax.fill_between(data['period'], data['balance'], 0, 
                     where=(data['balance'] < 0), 
                     alpha=0.3, color='red', 
                     label='Deficyt', interpolate=True)
    
    max_idx = data['balance'].idxmax()
    min_idx = data['balance'].idxmin()
    
    ax.scatter(data.loc[max_idx, 'period'], data.loc[max_idx, 'balance'],
               color='green', s=150, zorder=5, marker='^', 
               edgecolors='darkgreen', linewidths=2)
    
    ax.annotate(f"Max: {data.loc[max_idx, 'balance']:.2f} zł",
                xy=(data.loc[max_idx, 'period'], data.loc[max_idx, 'balance']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=10, weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))
    
    ax.scatter(data.loc[min_idx, 'period'], data.loc[min_idx, 'balance'],
               color='red', s=150, zorder=5, marker='v',
               edgecolors='darkred', linewidths=2)
    ax.annotate(f"Min: {data.loc[min_idx, 'balance']:.2f} zł",
                xy=(data.loc[min_idx, 'period'], data.loc[min_idx, 'balance']),
                xytext=(0, -15), textcoords='offset points',
                ha='center', fontsize=10, weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8))
    
    ax.set_xlabel('Period' if period == 'monthly' else 'Data', 
                  fontsize=12, weight='bold')
    ax.set_ylabel('Balance (zł)', fontsize=12, weight='bold')
    
    title = 'Balance in period(monthly)' if period == 'monthly' else 'Daily Balance'
    ax.set_title(title, fontsize=16, weight='bold', pad=20)
    
    ax.legend(loc='best', fontsize=10, frameon=True, shadow=True)
    
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True) 
    
    if len(data) > 8:
        plt.xticks(rotation=45, ha='right')
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    plt.tight_layout()
    return fig

def plot_incomes_vs_expenses(data):
    if data.empty:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.text(0.5, 0.5, 'Brak danych do wyświetlenia', 
        ha='center', va='center', fontsize=16, color='gray')
        ax.axis('off')
        return fig

    fig, ax = plt.subplots(figsize=(14,8))

    x = np.arange(len(data))
    width = 0.35

    bars1 = ax.bar(x - width/2, data['income'], width, 
                   label='Incomes', color='#4ECDC4', 
                   alpha=0.9, edgecolor='#000000', linewidth=1.5)
    
    bars2 = ax.bar(x + width/2, data['expenses'], width, 
                   label='Expenses', color='#FF6B6B', 
                   alpha=0.9, edgecolor='#000000', linewidth=1.5)
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0: 
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.0f}',
                       ha='center', va='bottom', 
                       fontsize=12, weight='bold')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.3)
    
    ax.set_xlabel('Period', fontsize=12, weight='bold')
    ax.set_ylabel('Amount (zł)', fontsize=12, weight='bold')
    ax.set_title('Incomes vs Expenses', fontsize=16, weight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(data['period'], rotation=45, ha='right')

    ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    plt.tight_layout()
    return fig

def plot_top_n_expenses(data):
    if data.empty:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.text(0.5, 0.5, 'Brak danych do wyświetlenia', 
        ha='center', va='center', fontsize=16, color='gray')
        ax.axis('off')
        return fig
    
    fig, ax = plt.subplots(figsize=(12,8))
    y = np.arange(len(data))
    height = 0.5

    bars = ax.barh(y, data['total_expense'], height, color = 'orange', edgecolor = 'black')
    for bar in bars:
        ax.annotate(f'{bar.get_width():,.2f} zł',  
                    xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                    xytext=(5,0), textcoords='offset points',
                    ha='left', va='center', fontsize=10)

    ax.set_yticks(y)
    ax.set_yticklabels(data['category'])
    ax.set_xlabel("Expense amount (zł)",fontsize=12,weight = 'bold')
    ax.set_ylabel("Categories", fontsize = 12,weight='bold')
    ax.set_title('Top expenses',fontsize =12, weight = 'bold',pad = 20 )

    ax.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    return fig

def plot_savings_progress(data):
    if data.empty:
        fig, ax = plt.subplots(figsize=(10,6))
        ax.text(0.5, 0.5, 'Brak danych do wyświetlenia', 
                ha='center', va='center', fontsize=16, color='gray')
        ax.axis('off')
        return fig
    
    data = data.sort_values(by='progress')
    fig, ax = plt.subplots(figsize=(12,8))
    x = np.arange(len(data))  
    width = 0.6               
    
    colors = []
    for p in data['progress']:
        if p < 50:
            colors.append('salmon')
        elif p < 80:
            colors.append('gold')
        else:
            colors.append('lightgreen')
    
    bars = ax.bar(x, data['progress'], width, color=colors, edgecolor='black')
    
    for bar in bars:
        ax.annotate(f'{bar.get_height():.1f}%',
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0,3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=10, weight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(data['goal_name'], rotation=45, ha='right')
    ax.set_ylim(0, 100)
    
    ax.set_ylabel('Progress (%)', fontsize=12, weight='bold')
    ax.set_xlabel('Saving goal', fontsize=12, weight='bold')
    ax.set_title('Savings progress', fontsize=16, weight='bold', pad=20)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    return fig
