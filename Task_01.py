import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel file
file_path = "/Users/shyamsanogar/Downloads/IndiaAgeWise.xlsx"
xls = pd.ExcelFile(file_path)
print(xls.sheet_names)

# Parse sheet
df = xls.parse('C-13')
print(df.head())

# Data Cleaning
df = df[df['Age'] != 'All ages']
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df = df.dropna(subset=['Age'])
df = df.sort_values(by='Age')

# Create Age Groups
bins = [0, 12, 19, 59, 150]
labels = ['Children (0–12)', 'Teenagers (13–19)', 'Adults (20–59)', 'Seniors (60+)']
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

# Summarize Population by Age Group
age_summary = df.groupby('Age Group')['Total Persons'].sum().reset_index()
age_summary = age_summary.sort_values(by='Total Persons', ascending=False)
order = age_summary['Age Group'].tolist()

# ✅ Match colors to sorted labels
color_map = {
    'Children (0–12)': '#00b050',
    'Teenagers (13–19)': '#0070c0',
    'Adults (20–59)': '#ffc000',
    'Seniors (60+)': '#ff0000'
}
colors = [color_map[label] for label in order]

# Total population for percentage calculation
total_pop = age_summary['Total Persons'].sum()

# Plotting
plt.figure(figsize=(8,8), facecolor='black')
ax = sns.barplot(
    x='Age Group', 
    y='Total Persons', 
    data=age_summary, 
    palette=colors, 
    width=1, 
    edgecolor='white', 
    linewidth=2, 
    order=order
)
ax.set_facecolor('black')

# Make border white
for spine in ax.spines.values():
    spine.set_color('white')

# Make tick labels white and bold
plt.xticks(fontsize=12, fontweight='bold', color='white')
plt.yticks(fontsize=12, fontweight='bold', color='white')
ax.tick_params(axis='both', colors='white')

# Add population & percentage text on bars
for bar, (_, row) in zip(ax.patches, age_summary.iterrows()):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    pct = row['Total Persons'] / total_pop * 100
    plt.text(
        x, y + 1e7,
        f"{row['Total Persons'] / 1e6:.0f} Mn\n({pct:.1f}%)",
        ha='center', fontsize=12, weight='bold', color='white'
    )

# Titles and labels
plt.title("India's Population Distribution by Age Group", fontsize=16, fontweight='bold', color='white')
plt.ylabel("Population", fontweight='bold', color='white')
plt.xlabel("Age Group", fontweight='bold', color='white')

# Add extra 25% headroom
plt.ylim(0, age_summary['Total Persons'].max() * 1.25)

plt.tight_layout()
plt.show()
