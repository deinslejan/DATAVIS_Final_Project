# SDG 5: Gender Equality - Education Access Analysis

## 📊 Project Overview

This project analyzes gender equality indicators related to education access, with a focus on **SDG 5 (Gender Equality)** using World Bank Development Indicators data from 2000-2023.

### Research Question
**How does access to primary education for girls correlate with female literacy rates, adolescent fertility rates, and female labor force participation across different countries and time periods?**

---

## 📁 Project Structure

```
DATAVIS_Final_Project/
│
├── 1_Data_Loading_Exploration.ipynb        # Initial data exploration
├── 2_Data_Preparation_Cleaning.ipynb       # Data cleaning & hybrid imputation
├── 3_Exploratory_Data_Analysis.ipynb       # Statistical analysis (matplotlib/seaborn)
├── 4_Interactive_Visualizations.ipynb      # Interactive dashboards (Plotly)
│
├── fetch_gender_data.py                     # Data collection script
├── gender_education_dataset.csv             # Raw dataset (World Bank)
├── gender_education_cleaned.csv             # Processed dataset (after Notebook 2)
│
└── README.md                                # This file
```

### 📓 Notebook Workflow

The analysis is structured as a **4-notebook pipeline** for clarity and modularity:

1. **Notebook 1: Data Loading & Exploration** - Load raw data, examine structure, check data quality
2. **Notebook 2: Data Preparation & Cleaning** - Filter data, apply hybrid imputation, create derived features
3. **Notebook 3: Exploratory Data Analysis** - Statistical visualizations using matplotlib/seaborn
4. **Notebook 4: Interactive Visualizations** - Publication-ready Plotly dashboards

---

## 📈 Indicators Used

| Indicator | Code | Description | SDG Relevance |
|-----------|------|-------------|---------------|
| **Girls Out of School** | SE.PRM.UNER.FE | Number of girls not enrolled in primary school | Identifies the problem magnitude |
| **Female Literacy Rate** | SE.ADT.LITR.FE.ZS | % of females 15+ who can read/write | Measures educational outcomes |
| **Male Literacy Rate** | SE.ADT.LITR.MA.ZS | % of males 15+ who can read/write | Enables gender comparison |
| **Adolescent Fertility** | SP.ADO.TFRT | Births per 1,000 women age 15-19 | Shows social consequences |
| **Female Labor Force** | SL.TLF.TOTL.FE.ZS | % of working-age women economically active | Indicates economic empowerment |

---

## 🔬 Analysis Components

### Part A: Dataset Description
- Justification of indicators
- Relevance to SDG 5 targets
- Data source documentation

### Part B: Data Preparation (Notebook 2)
1. **Filtering**: 
   - Removed 45 aggregate regions (World, continents, income groups)
   - Focused on 1980-2024 timespan
   - Filtered to 180+ individual countries

2. **Missing Value Handling - Hybrid Imputation** (3-step approach):
   - **Step 1**: Linear interpolation within countries (temporal continuity)
   - **Step 2**: Regional-year means (structural patterns)
   - **Step 3**: KNN imputation (similarity-based, n=5)
   - **Result**: Achieved 80%+ data coverage (from 23-28% originally)

3. **Derived Variables**: 
   - Gender Parity Index (Female/Male literacy ratio)
   - Literacy Gap (Male - Female %)
   - Regional Classifications (7 world regions)
   - Composite Gender Equality Index (0-100 scale)
   - Girls Out of School (in millions)

4. **Normalization**: Min-Max scaling (0-1) for composite indicators

### Part C: Exploratory Data Analysis (Notebook 3)
- **Descriptive Statistics**: Mean, median, std dev, quartiles for all indicators
- **Static Visualizations** (matplotlib/seaborn):
  1. **Distribution plots**: 6 histograms with mean/median lines
  2. **Regional box plots**: 4 indicators compared across 7 regions
  3. **Temporal trends**: 4 line plots showing 1980-2024 evolution
  4. **Correlation heatmap**: Relationships between all indicators
  5. **Gender parity analysis**: Regional comparisons and global trends
  6. **Performance rankings**: Top/bottom countries by indicator
  7. **Statistical testing**: ANOVA confirming regional differences

### Part D: Interactive Visualizations (Notebook 4)
**8 Interactive Visualizations** using Plotly:

1. **Time Series Line Chart**: Female literacy evolution by region (1980-2024)
2. **Animated Choropleth Map**: Global literacy rates on world map (animated)
3. **Scatter Plot**: Literacy vs. Labor Force Participation (size = fertility)
4. **Multi-Panel Dashboard**: 4 indicators compared across 7 regions (2x2 grid)
5. **Animated Bubble Chart**: Multi-dimensional temporal analysis (literacy, labor, fertility)
6. **Box Plot**: Gender Parity Index distributions by region
7. **Sunburst Chart**: Hierarchical regional breakdown (top 5 countries per region)
8. **Parallel Coordinates**: Multi-variable pattern exploration

---

## 🔍 Key Findings

### 1. Strong Inverse Relationship: Education ↔ Fertility
- **Correlation: r = -0.66** (strong negative)
- Countries with >90% female literacy: <30 adolescent births/1,000
- Countries with <50% female literacy: >100 births/1,000

### 2. Regional Disparities
- **Europe & North America**: Near-perfect parity (GEI: 85-95)
- **Sub-Saharan Africa**: Lowest indicators, steady improvement
- **South Asia**: Dramatic literacy improvements (2000→2023)
- **East Asia & Pacific**: High female labor participation

### 3. Gender Gap Closing
- Global literacy gap: 8% (2000) → 4% (2023)
- 15 countries achieved gender parity or female advantage

### 4. Complex Labor Participation
- **NOT** strictly correlated with literacy (r ≈ 0.30)
- Cultural, economic, and policy factors dominate

---

## 🛠️ Technical Requirements

### Python Libraries
```python
# Data manipulation
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0

# Data processing
scikit-learn>=1.3.0
```

### Installation
```bash
pip install pandas numpy scipy matplotlib seaborn plotly scikit-learn
```

---

## 🚀 How to Use

### Option 1: Run Complete Workflow (Recommended)

Execute notebooks in order:

1. **Notebook 1**: `1_Data_Loading_Exploration.ipynb` (explore raw data)
2. **Notebook 2**: `2_Data_Preparation_Cleaning.ipynb` (clean & impute data)
3. **Notebook 3**: `3_Exploratory_Data_Analysis.ipynb` (statistical analysis)
4. **Notebook 4**: `4_Interactive_Visualizations.ipynb` (interactive dashboards)

**⚠️ Important**: Notebook 2 must complete before running Notebooks 3-4 (it creates `gender_education_cleaned.csv`)

### Option 2: Skip to Visualizations

If `gender_education_cleaned.csv` exists, you can jump directly to:
- **Notebook 3** for statistical analysis
- **Notebook 4** for interactive visualizations

### Data Collection (Optional)

To refresh data from World Bank:
```bash
python fetch_gender_data.py
```

### Interacting with Visualizations

- **Hover**: View detailed data points
- **Click legends**: Show/hide series
- **Animation controls**: Play/pause temporal animations
- **Zoom/Pan**: Explore maps and scatter plots
- **Download**: Export charts as PNG/SVG

---

## 📊 Visualization Features

All visualizations include:
- ✅ Clear axis labels and titles
- ✅ Data source citations
- ✅ Color-coded legends
- ✅ Interactive hover details (Plotly charts)
- ✅ Professional styling
- ✅ Accessibility considerations

---

## 📝 Data Quality Notes

| Indicator | Original Completeness | After Imputation | Temporal Coverage | Notes |
|-----------|----------------------|------------------|-------------------|-------|
| Female Literacy | 23% | 83%+ | 1980-2024 | Self-reported by countries |
| Male Literacy | 28% | 83%+ | 1980-2024 | Self-reported by countries |
| Adolescent Fertility | 69% | 92%+ | 1980-2024 | Highly reliable |
| Labor Force Participation | 95% | 99%+ | 1980-2024 | Updated annually |
| Girls Out of School | 72% | 95%+ | 1980-2024 | Census-dependent |

**Hybrid Imputation**: 3-step approach (linear interpolation → regional means → KNN) significantly improved data coverage while preserving regional and temporal patterns.

**Missing Data**: Conflict-affected states (Syria, Yemen, South Sudan) and small island nations have remaining gaps even after imputation.

---

## 🎯 Policy Implications

1. **Education as Foundation**: Investing in girls' education has cascading positive effects
2. **Regional Strategies**: One-size-fits-all approaches ineffective
3. **Beyond Literacy**: Must couple education with economic opportunities
4. **Data Gaps**: Need better monitoring in conflict/fragile states

---

## 👨‍💻 Author
Data Visualization Final Project  
SDG Analysis Series

## 📄 License
Data Source: World Bank Development Indicators (Open Data)  
Analysis: Educational/Research Use

## 🔗 References
- World Bank DataBank: https://databank.worldbank.org/
- SDG 5 Indicators: https://unstats.un.org/sdgs/metadata/
- Pandas Documentation: https://pandas.pydata.org/
- Plotly Documentation: https://plotly.com/python/

---

## 🔄 Key Improvements

### Modular Workflow
- **Before**: Single monolithic notebook with imputation at the bottom (illogical)
- **After**: 4 focused notebooks with proper data flow (imputation before analysis)

### Data Coverage
- **Before**: 23-28% coverage for literacy indicators
- **After**: 83%+ coverage via hybrid imputation (linear → regional → KNN)

### Visualization Depth
- **Before**: Mixed static and interactive in one notebook
- **After**: Separate notebooks for statistical (matplotlib/seaborn) and interactive (Plotly) visualizations

---

**Last Updated**: December 2025  
**Data Coverage**: 1980-2024 (45 years)  
**Countries Analyzed**: 180+ individual countries (aggregate regions excluded)
