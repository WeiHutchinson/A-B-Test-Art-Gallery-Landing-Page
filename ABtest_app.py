import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.outliers_influence import variance_inflation_factor
from datetime import datetime

# Load data
df = pd.read_csv('AB_Test-Landing_page.csv')
# Data preprocessing
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y')
df['variant_id'] = df['variant_id'].astype(int)
df['converted'] = df['converted'].astype(int)

# Streamlit App Structure
st.title('A/B Test Insight for Landing Page')
st.subheader('Wei Hutchinson, PhD, Marketing Data Scientist')

# Custom HTML to create anchors
st.markdown("""
## Table of Contents
1. [Background](#background)
2. [Methodology/Approach](#methodology-approach)
3. [Part I - Probability](#part-i---probability)
4. [Part II - A/B Test](#part-ii---ab-test)
5. [Part III - Regression](#part-iii---regression)
6. [Summary & Conclusions](#summary--conclusions)
""", unsafe_allow_html=True)

st.markdown("<a name='background'></a>", unsafe_allow_html=True)
st.write("## 1. Background")
st.write("""
As a marketing data scientist, I partnered with an art gallery to enhance their website's landing page. Our primary goal was to increase user engagement by testing a new design aimed at boosting the sign-up rate for email updates about upcoming exhibitions and events.

This A/B test was part of a broader strategy to optimise the gallery's digital presence. By improving the landing page, we aimed to build a more robust mailing list, which is essential for keeping art enthusiasts informed and engaged with the gallery's offerings.

Given the importance of the landing page in converting visitors into subscribers, we focused on creating a design that would be more effective in driving these conversions. The data used in this analysis has been anonymised and de-sensitised to protect user privacy, while still providing a realistic view of user interactions.

Key objectives of this project included:
- Evaluating whether the new landing page design could outperform the existing one in terms of conversion rates.
- Understanding the behaviours and preferences of different user segments, such as those based on location and device type.

Through this analysis, we aimed to provide the gallery with actionable insights that would help them make informed decisions to enhance their digital engagement strategy.
""")

st.markdown("<a name='methodology-approach'></a>", unsafe_allow_html=True)
st.write("## 2. Methodology/Approach")
st.write("""
A/B testing was employed to assess the performance of two different versions of the landing page. Visitors were randomly assigned to either the control group, which saw the current landing page, or the treatment group, which was shown the new design.

**Hypothesis:**
- Null Hypothesis (H0): The new landing page is no better or worse than the old page in terms of conversion rates.
- Alternative Hypothesis (H1): The new landing page improves conversion rates compared to the old page.

**Analytical Techniques:**
- Descriptive Statistics
- Hypothesis Testing (Z-Test)
- Segment Analysis by Location and Device
- Statistical Inference Using Permutation and Bootstrap Methods
""")

st.markdown("<a name='part-i---probability'></a>", unsafe_allow_html=True)
st.write("## 3. Part I - Probability")

# Show the data
st.write("### Data Overview")
st.write(df.head())

st.write(f"Number of rows: {df.shape[0]}")
st.write(f"Number of columns: {df.shape[1]}")
st.write(f"{df['user_id'].nunique()} unique users")

# Conversion rates
overall_conversion_rate = df['converted'].mean()
st.write(f"Proportion of users converted = {overall_conversion_rate * 100:.2f}%")

control_conversion_rate = df.query('variant_id == 0')['converted'].mean()
st.write(f"Probability of conversion for control group: {control_conversion_rate * 100:.2f}%")

treatment_conversion_rate = df.query('variant_id == 1')['converted'].mean()
st.write(f"Probability of conversion for treatment group: {treatment_conversion_rate * 100:.2f}%")

# Probability of receiving the new page (treatment)
prob_new_page = (df['variant_id'] == 1).mean()
st.write(f"Probability of receiving the new page: {prob_new_page:.5f}")

# Conversion Rate by Location
conversion_rate_by_location = df.groupby('location')['converted'].mean()
st.write("### Conversion Rate by Location")
st.write(conversion_rate_by_location)
plt.figure(figsize=(10, 6))
sns.barplot(x=conversion_rate_by_location.index, y=conversion_rate_by_location.values, palette='Blues_d')
plt.title('Conversion Rates by Location')
plt.ylabel('Conversion Rate')
plt.ylim(0, 0.30)
st.pyplot(plt)

# Conversion Rate by Device
conversion_rate_by_device = df.groupby('device')['converted'].mean()
st.write("### Conversion Rate by Device Type")
st.write(conversion_rate_by_device)
plt.figure(figsize=(10, 6))
sns.barplot(x=conversion_rate_by_device.index, y=conversion_rate_by_device.values, palette='Blues_d')
plt.title('Conversion Rates by Device Type')
plt.ylabel('Conversion Rate')
plt.ylim(0, 0.30)
st.pyplot(plt)

st.write("""
### Summary of Conversion Analysis
- Total Number of Rows: 5,000
- Number of Unique Users: 5,000
- Proportion of Users Converted: 22.74%
- Probability of Conversion for Control Group: 22.16%
- Probability of Conversion for Treatment Group: 23.32%
- Probability of Receiving the New Page: 50%

#### Conversion Rate by Location
- Asia: 28.21%
- Europe: 22.02%
- North America: 21.08%
- Other Regions: 19.90%

#### Conversion Rate by Device Type
- Desktop: 23.88%
- Mobile: 21.11%
- Tablet: 23.21%

Insights:
- The conversion rate is slightly higher in the treatment group (23.32%) compared to the control group (22.16%).
- Users in Asia have the highest conversion rate at 28.21%.
- Desktop users convert at the highest rate (23.88%).
""")

st.markdown("<a name='part-ii---ab-test'></a>", unsafe_allow_html=True)
st.write("## 4. Part II - A/B Test")

st.write("### Hypothesis Setup")
st.write("""
- Null Hypothesis (H0): The new page is not better or worse than the old page in terms of conversion rates.
- Alternative Hypothesis (H1): The new page improves conversion rates compared to the old page.
""")

# Simulation under the Null Hypothesis
p_new = overall_conversion_rate
p_old = overall_conversion_rate
n_new = df.query('variant_id == 1').shape[0]
n_old = df.query('variant_id == 0').shape[0]

new_page_converted = np.random.binomial(n_new, p_new, 10000) / n_new
old_page_converted = np.random.binomial(n_old, p_old, 10000) / n_old

p_diffs = new_page_converted - old_page_converted
plt.figure(figsize=(8, 6))
plt.hist(p_diffs, bins=30, alpha=0.75, color='blue')
plt.axvline(x=0, color='black', linestyle='--')
plt.title('Simulated Differences in Conversion Rates under Null Hypothesis')
plt.xlabel('Difference in Conversion Rate')
plt.ylabel('Frequency')
st.pyplot(plt)

obs_diff = df.query('variant_id == 1')['converted'].mean() - df.query('variant_id == 0')['converted'].mean()
p_value = (p_diffs > obs_diff).mean()
st.write(f"P-value: {p_value:.5f}")

# Z-Test
convert_old = df.query('variant_id == 0')['converted'].sum()
convert_new = df.query('variant_id == 1')['converted'].sum()

z_score, p_value = proportions_ztest([convert_old, convert_new], [n_old, n_new], alternative='larger')
st.write(f"Z-Score: {z_score:.5f}, P-Value: {p_value:.5f}")

plt.figure(figsize=(8, 6))
sns.barplot(x=['Control', 'Treatment'], y=[convert_old/n_old, convert_new/n_new])
plt.title('Observed Conversion Rates with Z-Test Results')
plt.ylabel('Conversion Rate')
plt.ylim(0, 0.25)
plt.text(0, convert_old/n_old + 0.01, f'{convert_old/n_old:.3f}', ha='center', va='bottom')
plt.text(1, convert_new/n_new + 0.01, f'{convert_new/n_new:.3f}', ha='center', va='bottom')
st.pyplot(plt)

st.write("""
### Part II - A/B Test Results
- P-value (Simulated): 0.16450
- Z-Score: -0.97845
- P-Value (Z-Test): 0.83608
  Interpretation:
- Both P-values are greater than the significance level of 0.05, so we fail to reject the null hypothesis.
- The new page does not significantly outperform the old page in terms of conversion rate.
- The company may consider keeping the current page or running the experiment for a longer duration to gather more data.
""")

st.markdown("<a name='part-iii---regression'></a>", unsafe_allow_html=True)
st.write("## 5. Part III - Regression")

st.write("### Encode Device and Location")
location_dummies = pd.get_dummies(df['location'], prefix='location', dtype=int)
device_dummies = pd.get_dummies(df['device'], prefix='device', dtype=int)
df = pd.concat([df, location_dummies, device_dummies], axis=1)
df.drop(columns=['location', 'device'], inplace=True)

st.write(df.head())

# Calculate VIF
df['intercept'] = 1
X = df[['intercept', 'variant_id', 'location_Asia', 'location_Europe', 'location_North America', 'location_Other', 'device_Desktop', 'device_Mobile', 'device_Tablet']]
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
st.write("### Variance Inflation Factor (VIF) Analysis")
st.write(vif_data)

# Logistic Regression Models
X_reduced1 = df[['intercept', 'variant_id', 'location_Asia', 'location_North America', 'location_Europe']]
y = df['converted']

# Recalculate VIFs
vif_data_reduced1 = pd.DataFrame()
vif_data_reduced1["feature"] = X_reduced1.columns
vif_data_reduced1["VIF"] = [variance_inflation_factor(X_reduced1.values, i) for i in range(len(X_reduced1.columns))]
st.write("### Logistic Regression Model 1 - Reduced Variables")
st.write(vif_data_reduced1)

logit_model_reduced1 = sm.Logit(y, X_reduced1)
results_reduced1 = logit_model_reduced1.fit()

st.write("#### Model 1 Summary")
st.write(results_reduced1.summary2().tables[1])

# Second Logistic Regression Model
X_reduced2 = df[['intercept', 'variant_id', 'location_Asia', 'device_Desktop', 'device_Mobile']]
vif_data_reduced2 = pd.DataFrame()
vif_data_reduced2["feature"] = X_reduced2.columns
vif_data_reduced2["VIF"] = [variance_inflation_factor(X_reduced2.values, i) for i in range(len(X_reduced2.columns))]
st.write("### Logistic Regression Model 2 - Reduced Variables")
st.write(vif_data_reduced2)

logit_model_reduced2 = sm.Logit(y, X_reduced2)
results_reduced2 = logit_model_reduced2.fit()

st.write("#### Model 2 Summary")
st.write(results_reduced2.summary2().tables[1])

st.markdown("<a name='summary--conclusions'></a>", unsafe_allow_html=True)
st.write("## 6. Summary & Conclusions")
st.write("""
The logistic regression analysis revealed that the conversion rates for different locations and devices vary. Specifically:
- An individual from Asia is approximately 1.59 times more likely to convert than an individual from Europe, holding all other variables constant.
- The conversion rates for North America and Europe do not show statistically significant differences from Asia in this dataset.
- The device used (Desktop or Mobile) does not significantly impact conversion rates in this context.

The p-values in both models indicate that we failed to reject the null hypothesis at a 5% significance level. This suggests that the variant of the page (old vs. new) does not significantly affect the conversion rate.

Given the analysis, it seems that the location of users might have some influence on conversion rates, but the overall impact of the new page design is not statistically significant. The company may choose to stick with the current page or consider conducting a longer or more targeted test to better understand the potential impact of different factors on conversion rates. The current test was conducted for 181 days, which should generally provide a reliable dataset, but further exploration may be needed to gain deeper insights.
""")

