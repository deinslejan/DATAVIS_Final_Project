"""
Generate Interactive HTML Dashboard from Plotly Visualizations
This script creates a standalone HTML file with all interactive visualizations
"""

import pandas as pd
import base64
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

print("Loading data and figure files...")

# Load the cleaned dataset
df = pd.read_csv('gender_education_cleaned.csv')
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year].copy()

# Helper function to convert image file to base64
def img_to_base64(filepath):
    """Convert image file to base64 string"""
    try:
        with open(filepath, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        return img_base64
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return None

# Helper function to read HTML file
def read_html_file(filepath):
    """Read HTML file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
        return ""

# ============================================================================
# LOAD EXISTING FIGURES FROM NOTEBOOKS
# ============================================================================

print("Loading existing figures from notebooks...")

# EDA 1: Distribution Histograms (6 figures from Notebook 3)
eda_distributions = []
distribution_files = [
    'figures/figure1a_histogram_literacy-rate-female.png',
    'figures/figure1b_histogram_literacy-rate-male.png',
    'figures/figure1c_histogram_adolescent-fertility-rate.png',
    'figures/figure1d_histogram_female-labor-force-participation.png',
    'figures/figure1e_histogram_girls-out-of-school-primary.png',
    'figures/figure1f_histogram_literacy-gap.png'
]
for filepath in distribution_files:
    img_base64 = img_to_base64(filepath)
    if img_base64:
        eda_distributions.append(img_base64)

# EDA 2: Regional Box Plots (4 figures from Notebook 3)
eda_boxplots = []
boxplot_files = [
    'figures/figure2a_boxplot_literacy-rate-female.png',
    'figures/figure2b_boxplot_adolescent-fertility-rate.png',
    'figures/figure2c_boxplot_female-labor-force-participation.png',
    'figures/figure2d_boxplot_literacy-gap.png'
]
for filepath in boxplot_files:
    img_base64 = img_to_base64(filepath)
    if img_base64:
        eda_boxplots.append(img_base64)

# EDA 3: Temporal Trends (3 figures from Notebook 3)
eda_trends = []
trend_files = [
    'figures/figure3a_timeseries_literacy-rate-female.png',
    'figures/figure3b_timeseries_adolescent-fertility-rate.png',
    'figures/figure3c_timeseries_female-labor-force-participation.png'
]
for filepath in trend_files:
    img_base64 = img_to_base64(filepath)
    if img_base64:
        eda_trends.append(img_base64)

# EDA 4: Correlation Heatmap (1 figure from Notebook 3)
eda_correlation = img_to_base64('figures/figure4_correlation_heatmap.png')

# EDA 5: Gender Parity Analysis (2 figures from Notebook 3)
eda_parity_regional = img_to_base64('figures/figure5a_gender_parity_regional.png')
eda_parity_temporal = img_to_base64('figures/figure5b_gender_parity_temporal.png')

print(f"✓ Loaded {len(eda_distributions)} distribution charts")
print(f"✓ Loaded {len(eda_boxplots)} box plots")
print(f"✓ Loaded {len(eda_trends)} trend charts")
print(f"✓ Loaded correlation heatmap")
print(f"✓ Loaded gender parity analysis")

# ============================================================================
# LOAD INTERACTIVE PLOTLY VISUALIZATIONS (from Notebook 4)
# ============================================================================

print("Generating interactive Plotly charts from data...")

# 1. Regional Literacy Trends
regional_trends = df.groupby(['year', 'region'])['Literacy_Rate_Female'].mean().reset_index()

fig_trends = px.line(
    regional_trends,
    x='year',
    y='Literacy_Rate_Female',
    color='region',
    title='Female Literacy Rate Evolution by Region (1980-2024)',
    labels={
        'year': 'Year',
        'Literacy_Rate_Female': 'Female Literacy Rate (%)',
        'region': 'World Region'
    },
    markers=True,
    template='plotly_white',
    height=600
)
fig_trends.update_traces(line=dict(width=3), marker=dict(size=6))
fig_trends.update_layout(
    title_font_size=18,
    title_x=0.5,
    legend=dict(orientation='v', yanchor='middle', y=0.5, xanchor='left', x=1.02),
    hovermode='x unified'
)

# 2. Choropleth Map
iso_mapping = {
    'United States': 'USA', 'United Kingdom': 'GBR', 'China': 'CHN', 'India': 'IND',
    'Brazil': 'BRA', 'Germany': 'DEU', 'France': 'FRA', 'Japan': 'JPN', 'Italy': 'ITA',
    'Canada': 'CAN', 'Australia': 'AUS', 'Spain': 'ESP', 'Mexico': 'MEX', 'Korea, Rep.': 'KOR',
    'Indonesia': 'IDN', 'Netherlands': 'NLD', 'Saudi Arabia': 'SAU', 'Turkey': 'TUR',
    'Switzerland': 'CHE', 'Poland': 'POL', 'Belgium': 'BEL', 'Sweden': 'SWE', 'Norway': 'NOR',
    'Austria': 'AUT', 'Nigeria': 'NGA', 'Argentina': 'ARG', 'Egypt, Arab Rep.': 'EGY',
    'South Africa': 'ZAF', 'Pakistan': 'PAK', 'Bangladesh': 'BGD', 'Vietnam': 'VNM',
    'Philippines': 'PHL', 'Thailand': 'THA', 'Malaysia': 'MYS', 'Colombia': 'COL',
    'Chile': 'CHL', 'Finland': 'FIN', 'Denmark': 'DNK', 'Singapore': 'SGP', 'Portugal': 'PRT',
    'Ireland': 'IRL', 'Greece': 'GRC', 'Czech Republic': 'CZE', 'Romania': 'ROU',
    'New Zealand': 'NZL', 'Peru': 'PER', 'Ukraine': 'UKR', 'Kenya': 'KEN', 'Ethiopia': 'ETH',
    'Morocco': 'MAR', 'Algeria': 'DZA', 'Sudan': 'SDN', 'Tanzania': 'TZA', 'Uganda': 'UGA',
    'Ghana': 'GHA', 'Angola': 'AGO', 'Mozambique': 'MOZ', 'Madagascar': 'MDG', 'Cameroon': 'CMR',
    'Niger': 'NER', 'Mali': 'MLI', 'Burkina Faso': 'BFA', 'Malawi': 'MWI', 'Zambia': 'ZMB',
    'Senegal': 'SEN', 'Chad': 'TCD', 'Zimbabwe': 'ZWE', 'Rwanda': 'RWA', 'Benin': 'BEN',
    'Tunisia': 'TUN', 'Cuba': 'CUB', 'Dominican Republic': 'DOM', 'Guatemala': 'GTM',
    'Ecuador': 'ECU', 'Bolivia': 'BOL', 'Haiti': 'HTI', 'Honduras': 'HND', 'Paraguay': 'PRY',
    'Nicaragua': 'NIC', 'El Salvador': 'SLV', 'Costa Rica': 'CRI', 'Panama': 'PAN',
    'Uruguay': 'URY', 'Lebanon': 'LBN', 'Jordan': 'JOR', 'Libya': 'LBY', 'Yemen, Rep.': 'YEM',
    'Afghanistan': 'AFG', 'Nepal': 'NPL', 'Sri Lanka': 'LKA', 'Myanmar': 'MMR',
    'Cambodia': 'KHM', 'Lao PDR': 'LAO', 'Mongolia': 'MNG', 'Kazakhstan': 'KAZ',
    'Uzbekistan': 'UZB', 'Azerbaijan': 'AZE', 'Georgia': 'GEO', 'Armenia': 'ARM',
    'Albania': 'ALB', 'Croatia': 'HRV', 'Serbia': 'SRB', 'Bulgaria': 'BGR',
    'Slovakia': 'SVK', 'Lithuania': 'LTU', 'Slovenia': 'SVN', 'Latvia': 'LVA',
    'Estonia': 'EST', 'Hungary': 'HUN', 'Belarus': 'BLR', 'Bosnia and Herzegovina': 'BIH',
    'North Macedonia': 'MKD', 'Moldova': 'MDA', 'Luxembourg': 'LUX', 'Iceland': 'ISL',
    'Jamaica': 'JAM', 'Trinidad and Tobago': 'TTO', 'Bahamas, The': 'BHS', 'Barbados': 'BRB',
    'Mauritius': 'MUS', 'Botswana': 'BWA', 'Namibia': 'NAM', 'Gabon': 'GAB',
    'Lesotho': 'LSO', 'Gambia, The': 'GMB', 'Guinea': 'GIN', 'Togo': 'TGO',
    'Sierra Leone': 'SLE', 'Liberia': 'LBR', 'Central African Republic': 'CAF',
    'Congo, Rep.': 'COG', 'Congo, Dem. Rep.': 'COD', 'Burundi': 'BDI', 'Somalia': 'SOM',
    'Djibouti': 'DJI', 'Comoros': 'COM', 'Equatorial Guinea': 'GNQ', 'Guinea-Bissau': 'GNB',
    'Eritrea': 'ERI', 'South Sudan': 'SSD', 'Russian Federation': 'RUS', 'Turkiye': 'TUR',
    'Iran, Islamic Rep.': 'IRN', 'Iraq': 'IRQ', 'Syrian Arab Republic': 'SYR',
    'Oman': 'OMN', 'Kuwait': 'KWT', 'Qatar': 'QAT', 'United Arab Emirates': 'ARE',
    'Bahrain': 'BHR', 'Cyprus': 'CYP', 'Bhutan': 'BTN', 'Maldives': 'MDV',
    'Brunei Darussalam': 'BRN', 'Timor-Leste': 'TLS', 'Fiji': 'FJI',
    'Papua New Guinea': 'PNG', 'Solomon Islands': 'SLB', 'Vanuatu': 'VUT',
    'Samoa': 'WSM', 'Mauritania': 'MRT', 'Eswatini': 'SWZ', 'Guyana': 'GUY',
    'Suriname': 'SUR', 'Belize': 'BLZ', 'Cape Verde': 'CPV', 'Seychelles': 'SYC',
    'Sao Tome and Principe': 'STP', 'Kyrgyz Republic': 'KGZ', 'Tajikistan': 'TJK',
    'Turkmenistan': 'TKM', 'Montenegro': 'MNE', 'Kosovo': 'XKX'
}

df['iso_alpha'] = df['country'].map(iso_mapping)
map_data = df[df['iso_alpha'].notna() & (df['year'] % 2 == 0)].copy()

fig_map = px.choropleth(
    map_data,
    locations='iso_alpha',
    color='Literacy_Rate_Female',
    hover_name='country',
    hover_data={
        'iso_alpha': False,
        'Literacy_Rate_Female': ':.1f',
        'region': True,
        'year': True
    },
    animation_frame='year',
    color_continuous_scale='RdYlGn',
    range_color=[0, 100],
    title='Global Female Literacy Rate Evolution (1980-2024)',
    labels={'Literacy_Rate_Female': 'Female Literacy (%)'},
    template='plotly_white',
    height=600
)
fig_map.update_layout(
    title_font_size=18,
    title_x=0.5,
    geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth')
)

# 3. Scatter Plot
fig_scatter = px.scatter(
    latest_data,
    x='Literacy_Rate_Female',
    y='Female_Labor_Force_Participation',
    color='region',
    size='Adolescent_Fertility_Rate',
    hover_name='country',
    hover_data={
        'Literacy_Rate_Female': ':.1f',
        'Female_Labor_Force_Participation': ':.1f',
        'Adolescent_Fertility_Rate': ':.1f',
        'region': True
    },
    title=f'Female Literacy vs. Labor Force Participation ({latest_year})',
    labels={
        'Literacy_Rate_Female': 'Female Literacy Rate (%)',
        'Female_Labor_Force_Participation': 'Female Labor Force Participation (%)',
        'region': 'World Region',
        'Adolescent_Fertility_Rate': 'Adolescent Fertility Rate'
    },
    template='plotly_white',
    height=700
)
fig_scatter.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig_scatter.update_layout(
    title_font_size=18,
    title_x=0.5,
    legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=1.02)
)

# 4. Regional Dashboard
regional_summary = latest_data.groupby('region').agg({
    'Literacy_Rate_Female': 'mean',
    'Adolescent_Fertility_Rate': 'mean',
    'Female_Labor_Force_Participation': 'mean',
    'Literacy_Gap': 'mean'
}).reset_index()
regional_summary = regional_summary.sort_values('Literacy_Rate_Female', ascending=True)

fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Female Literacy Rate (%)',
        'Adolescent Fertility Rate',
        'Female Labor Force Participation (%)',
        'Gender Literacy Gap (M-F %)'
    ),
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'bar'}]],
    vertical_spacing=0.15,
    horizontal_spacing=0.15
)

fig_dashboard.add_trace(go.Bar(y=regional_summary['region'], x=regional_summary['Literacy_Rate_Female'],
    orientation='h', marker=dict(color='skyblue', line=dict(color='navy', width=1)),
    text=regional_summary['Literacy_Rate_Female'].round(1), textposition='auto'), row=1, col=1)

fig_dashboard.add_trace(go.Bar(y=regional_summary['region'], x=regional_summary['Adolescent_Fertility_Rate'],
    orientation='h', marker=dict(color='lightcoral', line=dict(color='darkred', width=1)),
    text=regional_summary['Adolescent_Fertility_Rate'].round(1), textposition='auto'), row=1, col=2)

fig_dashboard.add_trace(go.Bar(y=regional_summary['region'], x=regional_summary['Female_Labor_Force_Participation'],
    orientation='h', marker=dict(color='lightgreen', line=dict(color='darkgreen', width=1)),
    text=regional_summary['Female_Labor_Force_Participation'].round(1), textposition='auto'), row=2, col=1)

fig_dashboard.add_trace(go.Bar(y=regional_summary['region'], x=regional_summary['Literacy_Gap'],
    orientation='h', marker=dict(color='plum', line=dict(color='purple', width=1)),
    text=regional_summary['Literacy_Gap'].round(1), textposition='auto'), row=2, col=2)

fig_dashboard.update_layout(
    title_text=f"Regional Gender Education Dashboard ({latest_year})",
    title_font_size=20, title_x=0.5, showlegend=False, height=900, template='plotly_white',
    margin=dict(l=200, r=100, t=120, b=80)
)
fig_dashboard.update_xaxes(title_text='%', row=1, col=1)
fig_dashboard.update_xaxes(title_text='Births per 1000', row=1, col=2)
fig_dashboard.update_xaxes(title_text='%', row=2, col=1)
fig_dashboard.update_xaxes(title_text='% Points', row=2, col=2)

# 5. Animated Bubble Chart
bubble_data = df[df['year'] % 3 == 0].copy()

fig_bubble = px.scatter(
    bubble_data,
    x='Literacy_Rate_Female',
    y='Female_Labor_Force_Participation',
    size='Adolescent_Fertility_Rate',
    color='region',
    hover_name='country',
    animation_frame='year',
    animation_group='country',
    size_max=60,
    range_x=[0, 105],
    range_y=[0, 100],
    title='Female Education & Employment Evolution (1980-2024)',
    labels={
        'Literacy_Rate_Female': 'Female Literacy Rate (%)',
        'Female_Labor_Force_Participation': 'Female Labor Force Participation (%)',
        'Adolescent_Fertility_Rate': 'Adolescent Fertility',
        'region': 'World Region'
    },
    template='plotly_white',
    height=700
)
fig_bubble.update_traces(marker=dict(line=dict(width=1.5, color='DarkSlateGrey')), selector=dict(mode='markers'))
fig_bubble.update_layout(
    title_font_size=18,
    title_x=0.5,
    legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=1.02)
)

# 6. Gender Parity Box Plot (Full Timeline: 1980-2024)
fig_parity = px.box(
    df,
    x='region',
    y='Literacy_Gender_Parity_Index',
    color='region',
    title='Gender Parity Index Distribution by Region (1980-2024)',
    labels={
        'region': 'World Region',
        'Literacy_Gender_Parity_Index': 'Gender Parity Index (F/M ratio)'
    },
    template='plotly_white',
    height=600,
    points='outliers'
)
fig_parity.add_hline(y=1.0, line_dash='dash', line_color='red', 
               annotation_text='Perfect Parity (1.0)', annotation_position='right')
fig_parity.update_layout(title_font_size=18, title_x=0.5, showlegend=False, xaxis_tickangle=-45)

# 6b. Interactive Adolescent Fertility Rate Temporal Trends
fertility_trends = df.groupby(['year', 'region'])['Adolescent_Fertility_Rate'].mean().reset_index()

fig_fertility_trends = px.line(
    fertility_trends,
    x='year',
    y='Adolescent_Fertility_Rate',
    color='region',
    title='Adolescent Fertility Rate Evolution by Region (1980-2024)',
    labels={
        'year': 'Year',
        'Adolescent_Fertility_Rate': 'Adolescent Fertility Rate (births per 1000 women 15-19)',
        'region': 'World Region'
    },
    markers=True,
    template='plotly_white',
    height=600
)
fig_fertility_trends.update_traces(line=dict(width=3), marker=dict(size=6))
fig_fertility_trends.update_layout(
    title_font_size=18,
    title_x=0.5,
    legend=dict(orientation='v', yanchor='middle', y=0.5, xanchor='left', x=1.02),
    hovermode='x unified'
)

# 7. Parallel Coordinates
latest_sample = latest_data[['country', 'region', 'Literacy_Rate_Female', 'Literacy_Rate_Male', 
                              'Adolescent_Fertility_Rate', 'Female_Labor_Force_Participation',
                              'Literacy_Gap']].dropna().copy()

# Add a text column for hover display
latest_sample['hover_text'] = latest_sample['country'] + ' (' + latest_sample['region'] + ')'

# Create parallel coordinates with country hover
fig_parallel = go.Figure(data=
    go.Parcoords(
        line=dict(
            color=latest_sample['Literacy_Rate_Female'],
            colorscale='RdYlGn',
            showscale=True,
            cmin=0,
            cmax=100,
            colorbar=dict(title='Female<br>Literacy (%)')
        ),
        dimensions=[
            dict(range=[0, 100],
                 label='Female Literacy (%)',
                 values=latest_sample['Literacy_Rate_Female']),
            dict(range=[0, 100],
                 label='Male Literacy (%)',
                 values=latest_sample['Literacy_Rate_Male']),
            dict(range=[0, 250],
                 label='Adolescent Fertility',
                 values=latest_sample['Adolescent_Fertility_Rate']),
            dict(range=[0, 100],
                 label='Female Labor (%)',
                 values=latest_sample['Female_Labor_Force_Participation']),
            dict(range=[-20, 70],
                 label='Literacy Gap (%)',
                 values=latest_sample['Literacy_Gap'])
        ],
        # Add hover labels using the name property
        name='Countries'
    )
)

# Add annotations for better hover experience
fig_parallel.update_layout(
    title=f'Multi-Dimensional Gender Education Analysis ({latest_year})<br><sub>Drag axes to filter data ranges | Each line represents one country</sub>',
    title_font_size=18,
    title_x=0.5,
    height=600,
    template='plotly_white',
    font=dict(size=11)
)

# Note: Parallel coordinates has limited hover support in Plotly
# Users can select ranges on axes to filter and see the data

# 8. Sunburst Chart
sunburst_data = latest_data.groupby(['region', 'country'])['Literacy_Rate_Female'].mean().reset_index()
# Show all countries instead of just top 100
sunburst_data = sunburst_data.sort_values('Literacy_Rate_Female', ascending=False)

fig_sunburst = px.sunburst(
    sunburst_data,
    path=['region', 'country'],
    values='Literacy_Rate_Female',
    color='Literacy_Rate_Female',
    color_continuous_scale='RdYlGn',
    title=f'Hierarchical Female Literacy Analysis by Region ({latest_year})',
    height=700
)
fig_sunburst.update_layout(title_font_size=18, title_x=0.5)

# Convert to HTML
plotly_chart_trends = fig_trends.to_html(include_plotlyjs='cdn', div_id='chart_trends', full_html=False)
plotly_chart_fertility_trends = fig_fertility_trends.to_html(include_plotlyjs='cdn', div_id='chart_fertility_trends', full_html=False)
plotly_chart_map = fig_map.to_html(include_plotlyjs='cdn', div_id='chart_map', full_html=False)
plotly_chart_scatter = fig_scatter.to_html(include_plotlyjs='cdn', div_id='chart_scatter', full_html=False)
plotly_chart_dashboard = fig_dashboard.to_html(include_plotlyjs='cdn', div_id='chart_dashboard', full_html=False)
plotly_chart_bubble = fig_bubble.to_html(include_plotlyjs='cdn', div_id='chart_bubble', full_html=False)
plotly_chart_parity = fig_parity.to_html(include_plotlyjs='cdn', div_id='chart_parity', full_html=False)
plotly_chart_parallel = fig_parallel.to_html(include_plotlyjs='cdn', div_id='chart_parallel', full_html=False)
plotly_chart_sunburst = fig_sunburst.to_html(include_plotlyjs='cdn', div_id='chart_sunburst', full_html=False)

print(f"✓ Generated all interactive Plotly visualizations")



# ============================================================================
# Generate HTML Dashboard
# ============================================================================
print("Generating HTML dashboard...")

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDG 5: Gender Equality Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary-color: #1a365d;
            --secondary-color: #2c5282;
            --accent-color: #3182ce;
            --text-dark: #1a202c;
            --text-light: #718096;
            --bg-light: #f7fafc;
            --border-color: #e2e8f0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            background: #ffffff;
            color: var(--text-dark);
            line-height: 1.6;
        }
        
        /* Burger Menu Sidebar */
        .sidebar {
            position: fixed;
            left: -320px;
            top: 0;
            width: 320px;
            height: 100vh;
            background: var(--primary-color);
            box-shadow: 2px 0 15px rgba(0,0,0,0.2);
            transition: left 0.3s ease;
            z-index: 1000;
            overflow-y: auto;
        }
        
        .sidebar.active {
            left: 0;
        }
        
        .sidebar-header {
            padding: 25px 20px;
            background: var(--secondary-color);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .sidebar-header h2 {
            color: white;
            font-size: 1.2em;
            font-weight: 600;
        }
        
        .sidebar-nav {
            padding: 20px 0;
        }
        
        .sidebar-nav .nav-section {
            margin-bottom: 15px;
        }
        
        .sidebar-nav .section-label {
            padding: 10px 20px;
            font-size: 0.75em;
            color: #a0aec0;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        .sidebar-nav a {
            display: block;
            padding: 12px 20px 12px 40px;
            color: #e2e8f0;
            text-decoration: none;
            transition: all 0.2s ease;
            border-left: 3px solid transparent;
            font-size: 0.95em;
        }
        
        .sidebar-nav a:hover {
            background: rgba(255,255,255,0.1);
            border-left-color: var(--accent-color);
            padding-left: 45px;
        }
        
        /* Burger Button */
        .burger-btn {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 50px;
            height: 50px;
            background: var(--primary-color);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            z-index: 999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }
        
        .burger-btn:hover {
            background: var(--secondary-color);
            transform: scale(1.05);
        }
        
        .burger-btn span {
            display: block;
            width: 24px;
            height: 2px;
            background: white;
            margin: 5px auto;
            transition: all 0.3s ease;
        }
        
        .burger-btn.active span:nth-child(1) {
            transform: rotate(45deg) translate(6px, 6px);
        }
        
        .burger-btn.active span:nth-child(2) {
            opacity: 0;
        }
        
        .burger-btn.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -7px);
        }
        
        /* Overlay */
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 998;
        }
        
        .overlay.active {
            opacity: 1;
            visibility: visible;
        }
        
        /* Main Container */
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            padding-top: 80px;
        }
        
        /* Header */
        header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 60px 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        header h1 {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.95;
            font-weight: 300;
        }
        
        /* Stats Bar */
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            border-left: 4px solid var(--accent-color);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 25px rgba(0,0,0,0.12);
        }
        
        .stat-number {
            font-size: 2.2em;
            font-weight: 700;
            color: var(--accent-color);
            display: block;
            margin-bottom: 8px;
        }
        
        .stat-label {
            font-size: 0.95em;
            color: var(--text-light);
            font-weight: 500;
        }
        
        /* Content Sections */
        .section {
            background: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            scroll-margin-top: 100px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: var(--text-dark);
            margin-bottom: 15px;
            font-weight: 700;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border-color);
        }
        
        .section-description {
            color: var(--text-light);
            margin-bottom: 30px;
            font-size: 1.05em;
            line-height: 1.7;
        }
        
        .chart-container {
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .chart-container img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        /* Footer */
        footer {
            background: var(--primary-color);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-top: 40px;
            text-align: center;
        }
        
        footer p {
            margin: 10px 0;
            opacity: 0.9;
        }
        
        footer a {
            color: var(--accent-color);
            text-decoration: none;
            transition: opacity 0.2s ease;
        }
        
        footer a:hover {
            opacity: 0.8;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main-container {
                padding: 15px;
                padding-top: 80px;
            }
            
            header {
                padding: 40px 25px;
            }
            
            header h1 {
                font-size: 1.8em;
            }
            
            .section {
                padding: 25px;
            }
            
            .stats-bar {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Burger Menu Button -->
    <button class="burger-btn" id="burgerBtn">
        <span></span>
        <span></span>
        <span></span>
    </button>
    
    <!-- Overlay -->
    <div class="overlay" id="overlay"></div>
    
    <!-- Sidebar Navigation -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h2>Navigation</h2>
        </div>
        <div class="sidebar-nav">
            <div class="nav-section">
                <div class="section-label">Presentation Graphs</div>
                <a href="#pres-correlation">1. Correlation Matrix</a>
                <a href="#pres-parity">2. Gender Parity Index</a>
                <a href="#pres-literacy-trends">3. Female Literacy Evolution</a>
                <a href="#pres-fertility-trends">4. Adolescent Fertility Evolution</a>
                <a href="#pres-map">5. Global Literacy Map</a>
                <a href="#pres-scatter">6. Literacy vs Labor Force</a>
            </div>
            <div class="nav-section">
                <div class="section-label">Additional Analysis</div>
                <a href="#add-distributions">Distribution Analysis</a>
                <a href="#add-regional">Regional Comparisons</a>
                <a href="#add-temporal">Temporal Trends</a>
                <a href="#add-regional-parity">Regional Gender Parity</a>
                <a href="#add-dashboard">Regional Dashboard</a>
                <a href="#add-bubble">Multi-Dimensional Evolution</a>
                <a href="#add-parallel">Parallel Coordinates</a>
                <a href="#add-sunburst">Hierarchical Analysis</a>
            </div>
            <div class="nav-section">
                <div class="section-label">Resources</div>
                <a href="#methodology">Methodology</a>
                <a href="analysis.html">Detailed Analysis</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-container">
        <header>
            <h1>SDG 5: Gender Equality Dashboard</h1>
            <p>Education Access Analysis (1980-2024)</p>
        </header>
        
        <div class="stats-bar">
            <div class="stat-card">
                <span class="stat-number">180+</span>
                <span class="stat-label">Countries Analyzed</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">45 Years</span>
                <span class="stat-label">Data Coverage (1980-2024)</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">5</span>
                <span class="stat-label">Key Indicators</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">7</span>
                <span class="stat-label">World Regions</span>
            </div>
        </div>
        
        <!-- ========================================== -->
        <!-- PRESENTATION GRAPHS (FOR PRESENTATION)     -->
        <!-- ========================================== -->
        
        <div style="background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); color: white; padding: 30px; border-radius: 12px; margin: 40px 0 30px 0; text-align: center;">
            <h1 style="font-size: 2em; margin: 0; font-weight: 700;">Presentation Graphs</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.95; font-size: 1.1em;">Key visualizations for presentation</p>
        </div>
        
        <!-- 1. CORRELATION MATRIX -->
        <section id="pres-correlation" class="section">
            <h2 class="section-title">1. Correlation Matrix</h2>
            <p class="section-description">
                Heatmap showing correlations between all gender education indicators. Strong negative correlation between literacy and adolescent fertility (-0.66) confirms education's role in delaying childbearing.
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,""" + eda_correlation + """">
            </div>
        </section>
        
        <!-- 2. GENDER PARITY INDEX -->
        <section id="pres-parity" class="section">
            <h2 class="section-title">2. Gender Parity Index Distribution (1980-2024)</h2>
            <p class="section-description">
                Interactive box plot showing the distribution of Gender Parity Index by region across the <strong>full 45-year timeline (1980-2024)</strong>. 
                A value of 1.0 represents perfect gender parity. The chart shows how gender gaps have narrowed over time across all regions.
            </p>
            <div class="chart-container">
                """ + plotly_chart_parity + """
            </div>
        </section>
        
        <!-- 3. FEMALE LITERACY RATE EVOLUTION -->
        <section id="pres-literacy-trends" class="section">
            <h2 class="section-title">3. Female Literacy Rate Evolution by Region</h2>
            <p class="section-description">
                Interactive line chart tracking female literacy rates across world regions from 1980 to 2024. 
                <strong>Hover over lines</strong> to see exact values, <strong>click legend</strong> to show/hide regions.
            </p>
            <div class="chart-container">
                """ + plotly_chart_trends + """
            </div>
        </section>
        
        <!-- 4. ADOLESCENT FERTILITY RATE EVOLUTION -->
        <section id="pres-fertility-trends" class="section">
            <h2 class="section-title">4. Adolescent Fertility Rate Evolution by Region</h2>
            <p class="section-description">
                Interactive line chart showing how adolescent fertility rates have declined globally from 1980 to 2024. 
                This decline closely tracks female education improvements, demonstrating the strong link between education and delayed childbearing.
            </p>
            <div class="chart-container">
                """ + plotly_chart_fertility_trends + """
            </div>
        </section>
        
        <!-- 5. GLOBAL LITERACY MAP -->
        <section id="pres-map" class="section">
            <h2 class="section-title">5. Global Female Literacy Map</h2>
            <p class="section-description">
                Animated choropleth map showing worldwide changes in female literacy rates over time. 
                <strong>Click the play button</strong> to animate through years, hover over countries for details.
            </p>
            <div class="chart-container">
                """ + plotly_chart_map + """
            </div>
        </section>
        
        <!-- 6. LITERACY VS LABOR FORCE -->
        <section id="pres-scatter" class="section">
            <h2 class="section-title">6. Female Literacy vs. Labor Force Participation</h2>
            <p class="section-description">
                Interactive scatter plot showing the relationship between female literacy and labor force participation rates (current year snapshot). 
                Bubble size represents adolescent fertility rate. <strong>Note:</strong> This shows a single point in time, while the "Education & Employment Evolution" 
                shows how countries moved across these dimensions over 45 years through animation.
            </p>
            <div class="chart-container">
                """ + plotly_chart_scatter + """
            </div>
        </section>
        
        <!-- ========================================== -->
        <!-- ADDITIONAL GRAPHS (SUPPLEMENTARY ANALYSIS) -->
        <!-- ========================================== -->
        
        <div style="background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); color: white; padding: 30px; border-radius: 12px; margin: 60px 0 30px 0; text-align: center;">
            <h1 style="font-size: 2em; margin: 0; font-weight: 700;">Additional Analysis</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.95; font-size: 1.1em;">Supplementary visualizations and deeper insights</p>
        </div>
        
        <!-- DISTRIBUTION ANALYSIS -->
        <section id="add-distributions" class="section">
            <h2 class="section-title">Distribution Analysis</h2>
            <p class="section-description">
                Histograms showing the distribution of each indicator across all countries.
            </p>""" + "".join([f"""
            <div class="chart-container">
                <img src="data:image/png;base64,{img}">
            </div>
            """ for img in eda_distributions]) + """
        </section>
        
        <!-- REGIONAL BOX PLOTS -->
        <section id="add-regional" class="section">
            <h2 class="section-title">Regional Comparisons</h2>
            <p class="section-description">
                Box plots comparing indicator distributions across world regions.
            </p>""" + "".join([f"""
            <div class="chart-container">
                <img src="data:image/png;base64,{img}">
            </div>
            """ for img in eda_boxplots]) + """
        </section>
        
        <!-- TEMPORAL TRENDS (STATIC) -->
        <section id="add-temporal" class="section">
            <h2 class="section-title">Temporal Trends (Static Version)</h2>
            <p class="section-description">
                Static line plots showing how indicators evolved over 45 years by region.
            </p>""" + "".join([f"""
            <div class="chart-container">
                <img src="data:image/png;base64,{img}">
            </div>
            """ for img in eda_trends]) + """
        </section>
        
        <!-- GENDER PARITY (STATIC) -->
        """ + (f"""
        <section id="add-regional-parity" class="section">
            <h2 class="section-title">Gender Parity Analysis (Static)</h2>
            <p class="section-description">
                Regional and temporal analysis of Gender Parity Index (F/M literacy ratio).
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,{eda_parity_regional}">
            </div>
            <div class="chart-container">
                <img src="data:image/png;base64,{eda_parity_temporal}">
            </div>
        </section>
        """ if eda_parity_regional and eda_parity_temporal else "") + """
        
        <!-- REGIONAL DASHBOARD -->
        <section id="add-dashboard" class="section">
            <h2 class="section-title">Regional Comparison Dashboard</h2>
            <p class="section-description">
                Multi-panel comparison of key indicators across all world regions. Hover over bars for exact values.
            </p>
            <div class="chart-container">
                """ + plotly_chart_dashboard + """
            </div>
        </section>
        
        <!-- MULTI-DIMENSIONAL EVOLUTION -->
        <section id="add-bubble" class="section">
            <h2 class="section-title">Multi-Dimensional Evolution (Education & Employment)</h2>
            <p class="section-description">
                Animated bubble chart showing how countries evolved across literacy, labor force, and fertility dimensions over time (1980-2024). 
                <strong>Click play</strong> to see the evolution. This differs from the scatter plot above by showing the <strong>animated progression over 45 years</strong> 
                rather than a single snapshot.
            </p>
            <div class="chart-container">
                """ + plotly_chart_bubble + """
            </div>
        </section>
        
        <!-- PARALLEL COORDINATES -->
        <section id="add-parallel" class="section">
            <h2 class="section-title">Multi-Dimensional Analysis</h2>
            <p class="section-description">
                Parallel coordinates plot showing relationships across all indicators simultaneously. 
                <strong>Drag on any axis to filter data ranges</strong> and explore patterns. Each line represents one country, 
                colored by female literacy rate (red=low, green=high).
            </p>
            <div class="chart-container">
                """ + plotly_chart_parallel + """
            </div>
        </section>
        
        <!-- SUNBURST CHART -->
        <section id="add-sunburst" class="section">
            <h2 class="section-title">Hierarchical Literacy Analysis</h2>
            <p class="section-description">
                Sunburst chart showing literacy rates organized by region and country. Click segments to zoom in/out.
            </p>
            <div class="chart-container">
                """ + plotly_chart_sunburst + """
            </div>
        </section>
        
        <section id="methodology" class="section">
            <h2 class="section-title">Methodology</h2>
            <p class="section-description">
                <strong>Data Source:</strong> World Bank Development Indicators (1980-2024)<br>
                <strong>Missing Data Treatment:</strong> Hybrid imputation (linear interpolation, regional means, KNN)<br>
                <strong>Indicators Analyzed:</strong> Female literacy, male literacy, adolescent fertility, labor force participation, girls out of school<br>
                <strong>Geographic Coverage:</strong> 180+ countries across 7 world regions
            </p>
        </section>
        
        <footer>
            <p><strong>Data Source:</strong> World Bank Development Indicators</p>
            <p><strong>Analysis:</strong> SDG 5 Gender Equality - Education Access Project</p>
            <p style="margin-top: 15px;">
                <a href="https://databank.worldbank.org/" target="_blank">World Bank DataBank</a> | 
                <a href="https://unstats.un.org/sdgs/metadata/" target="_blank">SDG Indicators</a>
            </p>
        </footer>
    </div>
    
    <script>
        // Burger menu functionality
        const burgerBtn = document.getElementById('burgerBtn');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        
        burgerBtn.addEventListener('click', () => {
            burgerBtn.classList.toggle('active');
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        });
        
        overlay.addEventListener('click', () => {
            burgerBtn.classList.remove('active');
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
        
        // Smooth scrolling
        document.querySelectorAll('.sidebar-nav a').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        // Close menu on mobile
                        burgerBtn.classList.remove('active');
                        sidebar.classList.remove('active');
                        overlay.classList.remove('active');
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

# Write to file
output_file = 'gender_education_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Create separate analysis page
analysis_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detailed Analysis - SDG 5 Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: #f7fafc;
            color: #1a202c;
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        }
        
        h1 {
            color: #1a365d;
            font-size: 2.5em;
            margin-bottom: 30px;
            border-bottom: 3px solid #3182ce;
            padding-bottom: 15px;
        }
        
        h2 {
            color: #2c5282;
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        
        h3 {
            color: #2c5282;
            font-size: 1.4em;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        
        p, li {
            margin-bottom: 15px;
            color: #4a5568;
            font-size: 1.05em;
        }
        
        ul {
            padding-left: 30px;
        }
        
        .insight-box {
            background: #ebf8ff;
            border-left: 4px solid #3182ce;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .back-link {
            display: inline-block;
            padding: 12px 24px;
            background: #3182ce;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin-bottom: 20px;
            transition: background 0.2s;
        }
        
        .back-link:hover {
            background: #2c5282;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="gender_education_dashboard.html" class="back-link">← Back to Dashboard</a>
        
        <h1>Detailed Analysis: SDG 5 Gender Equality in Education</h1>
        
        <h2>Executive Summary</h2>
        <p>
            This analysis examines 45 years (1980-2024) of gender education data across 180+ countries, 
            revealing significant progress in female literacy rates globally while highlighting persistent 
            regional disparities and complex relationships between education, labor force participation, 
            and fertility rates.
        </p>
        
        <h2>Distribution Analysis Findings</h2>
        <div class="insight-box">
            <h3>Key Patterns</h3>
            <ul>
                <li><strong>Bimodal Literacy Distribution:</strong> Countries cluster into high literacy (>85%) and low literacy (<60%) groups, indicating a global education divide.</li>
                <li><strong>Right-Skewed Fertility:</strong> Most countries have achieved low adolescent fertility rates (<40 per 1000), with outliers in Sub-Saharan Africa and parts of South Asia.</li>
                <li><strong>Wide Labor Force Variation:</strong> Female labor force participation ranges from 30% to 80%, showing cultural and economic factors beyond education.</li>
                <li><strong>Out-of-School Extremes:</strong> Most countries have low rates, but crisis-affected regions show extreme outliers indicating emergency education contexts.</li>
            </ul>
        </div>
        
        <h2>Regional Comparison Insights</h2>
        <h3>Europe & Central Asia</h3>
        <ul>
            <li>Highest median literacy rates (>95%)</li>
            <li>Tightest distribution indicating uniformity across countries</li>
            <li>Lowest adolescent fertility rates</li>
            <li>Near-perfect gender parity (0.98-1.00)</li>
        </ul>
        
        <h3>Sub-Saharan Africa</h3>
        <ul>
            <li>Lowest median literacy rates but widest variation</li>
            <li>Some countries approaching universal literacy while others remain below 50%</li>
            <li>Highest adolescent fertility rates</li>
            <li>Largest gender gaps in literacy</li>
        </ul>
        
        <h3>South Asia</h3>
        <ul>
            <li>Dramatic improvement: 30% average literacy (1980) to 70% (2024)</li>
            <li>Significant inter-country variation</li>
            <li>Persistent gender gaps (6-8 percentage points)</li>
            <li>Cultural barriers to female labor participation despite rising literacy</li>
        </ul>
        
        <h3>East Asia & Pacific</h3>
        <ul>
            <li>High and rising literacy rates</li>
            <li>Highest female labor force participation (60%+)</li>
            <li>Rapid fertility decline</li>
            <li>Strong correlation between education and economic participation</li>
        </ul>
        
        <h2>Temporal Trends (1980-2024)</h2>
        <div class="insight-box">
            <h3>Universal Progress</h3>
            <p>
                All regions show upward literacy trends with no reversals, indicating sustained global 
                commitment to education despite conflicts, economic crises, and pandemics.
            </p>
        </div>
        
        <ul>
            <li><strong>Acceleration After 2000:</strong> Millennium Development Goals (MDGs) and SDGs drove faster improvements post-2000.</li>
            <li><strong>Fertility Decline:</strong> Adolescent fertility declining globally since 1990s, closely tracking female education improvements.</li>
            <li><strong>Labor Force Plateau:</strong> Some regions (MENA, South Asia) show plateaued female labor participation despite rising literacy.</li>
            <li><strong>Gender Gap Narrowing:</strong> Global gender literacy gap reduced from 15 percentage points (1980) to 5 points (2024).</li>
        </ul>
        
        <h2>Correlation Analysis</h2>
        <h3>Strong Relationships</h3>
        <ul>
            <li><strong>Female ↔ Male Literacy (r ≈ 0.95):</strong> Very strong positive correlation indicates education systems affect both genders similarly.</li>
            <li><strong>Literacy ↔ Adolescent Fertility (r ≈ -0.66):</strong> Strong negative correlation confirms education's role in delaying childbearing.</li>
            <li><strong>Out of School ↔ Literacy (r ≈ -0.70):</strong> Strong negative correlation validates data quality and indicator consistency.</li>
        </ul>
        
        <h3>Moderate Relationships</h3>
        <ul>
            <li><strong>Literacy ↔ Labor Participation (r ≈ 0.30):</strong> Moderate positive correlation indicates education is necessary but not sufficient for economic participation. Cultural norms, childcare availability, and employment opportunities matter significantly.</li>
        </ul>
        
        <h2>Gender Parity Progress</h2>
        <div class="insight-box">
            <h3>Overall Improvement</h3>
            <p>
                Global Gender Parity Index improved from 0.85 (1980) to 0.95 (2024), representing 
                significant but incomplete progress toward equality.
            </p>
        </div>
        
        <h3>Regional Performance</h3>
        <ul>
            <li><strong>Achieved Parity (≥0.98):</strong> Europe, North America, Latin America, East Asia</li>
            <li><strong>Near Parity (0.90-0.97):</strong> Parts of Middle East, Southeast Asia</li>
            <li><strong>Significant Gaps (0.75-0.90):</strong> South Asia, North Africa, Sub-Saharan Africa</li>
            <li><strong>Reverse Gap (>1.00):</strong> 15 countries where female literacy exceeds male (mostly small island states and highly developed nations)</li>
        </ul>
        
        <h2>Multi-Dimensional Evolution</h2>
        <p>
            The animated bubble chart reveals countries generally move rightward (↑literacy) while 
            bubbles shrink (↓fertility), but vertical movement (labor participation) varies dramatically:
        </p>
        <ul>
            <li><strong>Fastest Improvers:</strong> China, Bangladesh, Iran, Morocco show dramatic literacy gains with fertility decline.</li>
            <li><strong>Labor Force Paradox:</strong> Some countries (e.g., India, Turkey) show declining female labor participation despite rising literacy, indicating complex socioeconomic factors.</li>
            <li><strong>Successful Integration:</strong> East Asian countries demonstrate both high literacy and sustained high female labor participation.</li>
        </ul>
        
        <h2>Key Policy Implications</h2>
        <div class="insight-box">
            <h3>Education Alone Is Insufficient</h3>
            <p>
                While literacy improvements are crucial and globally consistent, translating education 
                into economic participation requires complementary policies addressing cultural norms, 
                childcare, workplace discrimination, and economic opportunity structures.
            </p>
        </div>
        
        <ul>
            <li><strong>Target Persistent Gaps:</strong> South Asia and MENA require targeted interventions addressing cultural barriers beyond schooling access.</li>
            <li><strong>Maintain Momentum:</strong> Progress plateaued in some regions post-2010; renewed commitment needed.</li>
            <li><strong>Address Labor Market Barriers:</strong> High literacy without labor participation indicates barriers beyond education.</li>
            <li><strong>Support Crisis Contexts:</strong> Extreme outliers in girls' out-of-school rates indicate emergency education needs in conflict/disaster zones.</li>
        </ul>
        
        <h2>Methodology Notes</h2>
        <h3>Data Source</h3>
        <p>World Bank Development Indicators (1980-2024), covering 180+ countries with biennial measurements.</p>
        
        <h3>Missing Data Treatment</h3>
        <p>Hybrid imputation approach:</p>
        <ol>
            <li>Linear interpolation for within-country gaps</li>
            <li>Regional mean imputation for isolated missing values</li>
            <li>K-Nearest Neighbors (KNN) for complex patterns</li>
        </ol>
        
        <h3>Indicators</h3>
        <ul>
            <li>Female literacy rate (% ages 15+)</li>
            <li>Male literacy rate (% ages 15+)</li>
            <li>Adolescent fertility rate (births per 1000 women ages 15-19)</li>
            <li>Female labor force participation rate (% ages 15+)</li>
            <li>Girls out of school, primary (% of primary school-age girls)</li>
            <li>Gender Parity Index (Female literacy / Male literacy)</li>
        </ul>
        
        <h2>Conclusion</h2>
        <p>
            The 45-year analysis reveals substantial global progress in gender equality in education, 
            with female literacy rates improving across all regions. However, persistent regional 
            disparities, particularly in South Asia and Sub-Saharan Africa, require sustained policy 
            attention. Furthermore, the moderate correlation between literacy and labor participation 
            highlights that education, while necessary, must be complemented by broader social and 
            economic reforms to achieve full gender equality in all dimensions of development.
        </p>
        
        <a href="gender_education_dashboard.html" class="back-link" style="margin-top: 40px;">← Back to Dashboard</a>
    </div>
</body>
</html>
"""

with open('analysis.html', 'w', encoding='utf-8') as f:
    f.write(analysis_html)

print(f"\n✓ Dashboard created successfully: {output_file}")
print(f"✓ Analysis page created: analysis.html")
print(f"✓ Open the file in your browser to view all interactive visualizations!")
print(f"\nFeatures included:")
print("  • Professional design with burger menu navigation")
print("  • Responsive layout with smooth scrolling")
print("  • 6 interactive Plotly visualizations")
print("  • Clean interface without emojis")
print("  • Separate detailed analysis page")
