# Mastercard Inclusive Growth Score (IGS) - Data Dictionary

**Dataset Source:** Mastercard Center for Inclusive Growth  
**Temporal Coverage:** 2017-2024  
**Geographic Scope:** U.S. Census Tracts  
**Last Updated:** November 19, 2025

---

## Dataset Overview

The Mastercard Inclusive Growth Score (IGS) measures economic inclusion at the census tract level across the United States. Unlike traditional economic indicators that focus solely on growth, IGS emphasizes **equitable distribution** of opportunities within communities.

### File Locations

- **Raw Data:** `data/raw/IGS-score.csv` (original, unprocessed)
- **Processed Data:** `data/processed/IGS-score-cleaned.csv` (cleaned for analysis)

### Dataset Dimensions

- **Total Records:** 32 data rows (after cleaning)
- **Total Columns:** 71
- **Geographic Coverage:** Multiple counties across Georgia, New York, California, and Texas
- **Temporal Range:** 2017-2024 (8 years)

---

## Data Cleaning Steps Performed

1. **Removed Metadata Rows:** Rows 1-3 contained category headers and were removed
2. **Standardized Missing Values:** Converted "N/A" strings to proper null values
3. **Type Conversion:** All score columns converted to numeric (float/int)
4. **Column Naming:** Retained original descriptive column names for clarity
5. **Index Column Removal:** Removed redundant row index column

---

## Column Definitions

### Core Identification Fields

| Column Name | Data Type | Description | Example |
|-------------|-----------|-------------|---------|
| `Is an Opportunity Zone` | String | Indicates if tract is designated as an Opportunity Zone | "N/A", "Yes" |
| `Census Tract FIPS code` | String | 11-digit unique identifier for census tract | "13089021415" |
| `County` | String | County name | "DeKalb County" |
| `State` | String | State name | "Georgia" |
| `Year` | Integer | Data year | 2017-2024 |

---

### Summary Metrics (Composite Scores)

| Column Name | Data Type | Range | Description |
|-------------|-----------|-------|-------------|
| `Inclusive Growth Score` | Integer | 1-100 | **Primary metric**: Composite score measuring overall economic inclusion relative to state average |
| `Growth` | Integer | 1-100 | Sub-score measuring economic expansion indicators |
| `Inclusion` | Integer | 1-100 | Sub-score measuring equitable distribution of opportunities |

**Interpretation:** Scores are normalized to state averages (50 = average). Higher scores indicate better performance.

---

### PLACE Category (Living Environment Quality)

| Column Name | Data Type | Description | Social Impact |
|-------------|-----------|-------------|---------------|
| `Place` | Integer (1-100) | Composite score for living environment quality | Overall neighborhood vitality |
| `Place Growth` | Integer (1-100) | Growth dimension of place metrics | Improving infrastructure |
| `Place Inclusion` | Integer (1-100) | Inclusion dimension of place metrics | Equitable access to amenities |

#### Place Sub-Metrics

| Metric | Description | Why It Matters |
|--------|-------------|----------------|
| `Net Occupancy Score` | Occupancy rate of residential properties | Housing demand indicator |
| `Residential Real Estate Value Score` | Home value appreciation | Wealth building opportunity |
| `Acres of Park Land Score` | Access to green spaces per capita | Health and recreation access |
| **`Affordable Housing Score`** | **Housing cost burden relative to income** | **Economic stability** |
| **`Internet Access Score`** | **% of households with broadband** | **Digital inclusion (education/work)** |
| `Travel Time to Work Score` | Commute duration | Time/transportation equity |

**Note:** Each score has corresponding "Base %" (state average) and "Tract %" (actual tract value) columns.

---

### ECONOMY Category (Economic Opportunity)

| Column Name | Data Type | Description | Social Impact |
|-------------|-----------|-------------|---------------|
| `Economy` | Integer (1-100) | Composite score for economic opportunity | Overall economic health |
| `Economy Growth` | Integer (1-100) | Economic expansion indicators | Job creation, business growth |
| `Economy Inclusion` | Integer (1-100) | Equitable access to economic opportunity | Income equality, entrepreneurship |

#### Economy Sub-Metrics

| Metric | Description | Why It Matters |
|--------|-------------|----------------|
| `New Businesses Score` | Rate of new business formation | Entrepreneurial activity |
| `Spend Growth Score` | Consumer spending growth rate | Economic vitality |
| `Small Business Loans Score` | Access to small business financing | Entrepreneurial support |
| **`Minority/Women Owned Businesses Score`** | **% of businesses owned by marginalized groups** | **Economic equity & empowerment** |
| `Labor Market Engagement Index Score` | Workforce participation rate | Employment opportunity |
| `Commercial Diversity Score` | Variety of business types | Economic resilience |

---

### COMMUNITY Category (Social Well-Being)

| Column Name | Data Type | Description | Social Impact |
|-------------|-----------|-------------|---------------|
| `Community` | Integer (1-100) | Composite score for social well-being | Quality of life |
| `Community Growth` | Integer (1-100) | Improving community indicators | Rising incomes, education |
| `Community Inclusion` | Integer (1-100) | Equitable social outcomes | Poverty reduction, healthcare access |

#### Community Sub-Metrics

| Metric | Description | Why It Matters |
|--------|-------------|----------------|
| **`Personal Income Score`** | **Median household income relative to state** | **Economic opportunity** |
| `Spending per Capita Score` | Consumer spending per person | Purchasing power |
| `Female Above Poverty Score` | % of women above poverty line | Gender equity |
| `Gini Coefficient Score` | Income inequality measure | Economic fairness |
| `Early Education Enrollment Score` | Pre-K enrollment rates | Educational access |
| `Health Insurance Coverage Score` | % insured population | Healthcare access |

---

## Key Variables for DEI Analysis

### Priority Metrics (Highlighted in Proposal)

1. **Minority/Women Owned Businesses Score**
   - **Why:** Direct measure of entrepreneurial equity
   - **Use Case:** Identify areas with low minority business presence for targeted support

2. **Internet Access Score**
   - **Why:** Essential for modern education and remote work
   - **Use Case:** Map "digital deserts" requiring broadband infrastructure investment

3. **Affordable Housing Score**
   - **Why:** Foundation for community stability
   - **Use Case:** Identify housing cost burden hotspots

4. **Personal Income Score**
   - **Why:** Economic opportunity baseline
   - **Use Case:** Correlate with other metrics to understand income drivers

---

## Data Quality Notes

### Missing Values

- **Small Business Loans (Base/Tract %):** Frequently missing (privacy/data availability)
- **Residential Real Estate Value:** Some missing for recent years (2021-2024)
- **Gini Coefficient:** Missing in some tracts
- **Early Education Enrollment:** Missing in rural areas

### Handling Strategy

- **Analysis:** Use `.dropna()` for complete case analysis or imputation methods
- **Visualization:** Display missing data counts in dashboard
- **Ethical Note:** Missing data may indicate underserved areas (data desert ≠ opportunity desert)

---

## Scoring Methodology

### How Scores are Calculated

1. **Raw Values:** Mastercard collects transaction data + census data
2. **State Baseline:** Calculate state average for each metric
3. **Normalization:** Score tract relative to state (1-100 scale)
   - **50 = State Average**
   - **Above 50 = Better than state average**
   - **Below 50 = Worse than state average**

### Example Interpretation

| Score | Interpretation |
|-------|----------------|
| 90 | Tract significantly outperforms state average |
| 50 | Tract matches state average |
| 20 | Tract significantly underperforms state average |

---

## Ethical Considerations in Data Use

### Representation Bias
- **Issue:** Spending data skewed toward banked populations
- **Impact:** Cash-based economies (often lower-income) may be underrepresented
- **Mitigation:** Acknowledge bias in analysis, supplement with Census data

### Privacy
- **Aggregation Level:** Census tract (avg. 4,000 people)
- **Protection:** No individual identifiers present

### Stigmatization Risk
- **Issue:** Low scores can stigmatize neighborhoods
- **Mitigation:** Frame as "opportunity potential" not "deficits"

---

## Sample Data Snapshot

| Census Tract | County | State | Year | IGS | Internet Access | Minority/Women Business |
|--------------|--------|-------|------|-----|-----------------|------------------------|
| 13089021415 | DeKalb | GA | 2024 | 58 | 83 | 21 |
| 36061013300 | New York | NY | 2024 | 67 | 75 | 44 |
| 06011000100 | Colusa | CA | 2024 | 42 | 14 | 88 |
| 48113016406 | Dallas | TX | 2024 | 53 | 36 | 86 |

---

## References

- [Mastercard Center for Inclusive Growth](https://www.mastercardcenter.org/)
- [U.S. Census Bureau - Census Tracts](https://www.census.gov/programs-surveys/geography/about/glossary.html#par_textimage_13)

---

**Document Version:** 1.0  
**Prepared by:** Emery  
**Last Updated:** November 19, 2025

