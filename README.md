# Art Gallery Landing Page A/B Test Optimisation

## Table of Contents
1. [Introduction/Overview](#introductionoverview)
2. [Objective](#objective)
3. [Methodology/Approach](#methodologyapproach)
4. [Installation/Requirements](#installationrequirements)
5. [File Descriptions](#file-descriptions)
6. [Data Collection and Sources](#data-collection-and-sources)
7. [Results/Conclusions](#resultsconclusions)
8. [License](#license)

## 1. Introduction/Overview
As a marketing data consultant, I collaborated with one of my clients, an art gallery, to optimise their website's landing page. The goal was to increase user engagement by testing a new landing page design aimed at improving the sign-up rate for email updates about upcoming exhibitions and events. This project involves analysing an A/B test conducted to determine if the new design should be implemented.

**Note**: The data used in this analysis has been de-sensitised, with patterns mimicked to maintain confidentiality while still reflecting realistic user behaviour and interactions.

## 2. Objective
The objective of this project is to analyse A/B test results to determine which landing page design is more effective in converting visitors into subscribers to the gallery's mailing list.

## 3. Methodology/Approach
A/B testing is employed to assess the performance of two different versions of the landing page. Visitors were randomly assigned to either the control group, which saw the current landing page, or the treatment group, which was shown the new design.

### Hypothesis:
- **Null Hypothesis (H0)**: The new landing page is no better or worse than the old page in terms of conversion rates.
- **Alternative Hypothesis (H1)**: The new landing page improves conversion rates compared to the old page.

### Analytical Techniques:
- Descriptive Statistics
- Hypothesis Testing (Z-Test)
- Segment Analysis by Location and Device
- Statistical Inference Using Permutation and Bootstrap Methods

## 4. Installation/Requirements
This project requires the following Python libraries:

- Numpy
- Pandas
- Statsmodels
- Matplotlib
- Seaborn

Ensure that Python version 3.x is installed. All code should run without issues in a Jupyter Notebook environment.

## 5. File Descriptions
This repository contains the following files:

- **AB_Test_Data_With_Analysis.csv**: The dataset used for analysis, including A/B test results and additional segmentation data.
- **AB-Test-Insights-For-Art-Gallery.ipynb**: A Jupyter notebook containing the analysis code and steps performed to derive insights from the A/B test data.
- **README.md**: This README file.

## 6. Data Collection and Sources
### Datasets:
- **AB_Test_Data_With_Analysis.csv**: Contains the results of the A/B test, including additional information for segment analysis.
  - `user_id`: Unique identifier for each user.
  - `timestamp`: The date and time when the user visited the landing page.
  - `experiment_id`: Identifier for the A/B test experiment.
  - `variant_id`: Indicates the group (0 for control, 1 for treatment).
  - `converted`: Indicates whether the user converted (signed up for email updates).
  - `location`: Simulated location data for each user.
  - `device`: Simulated device type for each user.


**Note**: The data is simulated to mimic realistic patterns while preserving the confidentiality of the original data.

## 7. Results/Conclusions
The analysis suggests that while the new landing page design does not significantly improve overall conversion rates, it may be more effective in specific locations such as Asia. This insight can help inform targeted marketing strategies and further optimisation efforts.

## 8. License
This project is licensed under the MIT Licence.
