# Notebook Structure Explanation

## Overview
Your notebook now has **TWO sections** doing similar analyses:
1. **ORIGINAL SECTION** (Cells 0-14): Your original code
2. **CLEANED-UP SECTION** (Cells 15+): Corrected and expanded analyses I added

## What Was There Originally (Cells 0-14)

### Cell 0: Imports
- Basic imports (pandas, matplotlib, numpy)
- **Note**: I later added `pearsonr`, `statsmodels`, `sklearn` imports here

### Cell 1: Load Data
- `df = pd.read_csv("v3_data.csv", index_col=0)`

### Cell 2: Data Info
- `df.info()` to see data types

### Cell 3: Rename Columns
- Renamed all columns to shorter names (e.g., `ai_brainstorm`, `creat_feels_creative`, etc.)

### Cell 4: Describe Data
- `df.describe()` to see summary statistics

### Cell 5: Head
- `df.head()` to preview data

### Cell 6: Organize Items
- Created lists: `ai_items`, `authorship_items`, `creativity_items`
- These were used to categorize survey questions

### Cell 7: Calculate Composite Scores
**⚠️ THIS HAD ISSUES:**
- Calculated `AI_USE_SCORE` (correct)
- Calculated `CREATIVITY_SCORE` using **ALL 5 creativity items** (WRONG - should use only 3 items for `CREATIVITY_GENERAL`)
- Calculated `AUTHORSHIP_SCORE` using **ALL authorship items** including `auth_worry_copy` (WRONG - should exclude this)
- Reverse coding was done but not consistently

### Cell 8: Cronbach's Alpha
- Calculated reliability for scales
- **Issue**: Used old `CREATIVITY_SCORE` (5 items) instead of `CREATIVITY_GENERAL` (3 items)
- **Issue**: Used all authorship items instead of core 4 items

### Cell 9: Correlations
- Calculated correlations between scores
- **Issue**: Used wrong score definitions

### Cell 10-14: Additional Analysis
- Some plotting code
- Some additional reliability checks

## What I Added (Cells 15+)

### Cell 15: Markdown Header
- "CLEANED-UP ANALYSIS SECTION"
- Marks where the corrected code begins

### Cell 16: Corrected Composite Scores
**✅ FIXED:**
- `AI_USE_SCORE`: Same (5 items) ✓
- `CREATIVITY_GENERAL`: **Only 3 items** (feels_creative, conf_no_ai, enjoy_writing) ✓
- `CREATIVITY_AI_BOOST`: 2 items (ai_helps_ideas, more_creative_with_ai) - for reference
- `AUTHORSHIP_SCORE`: **Only 4 core items** (excludes `auth_work_own` and `auth_worry_copy`) ✓
- Proper reverse coding for negative items

### Cell 17: Corrected Reliability
- Cronbach's Alpha for:
  - AI Use Scale (5 items)
  - Creativity General Scale (3 items) ✓
  - Authorship Core Scale (4 items) ✓

### Cell 18: Corrected Correlations
- Uses the **correct** score definitions
- Reports sample sizes and p-values

### Cell 19: Markdown - Regression Section

### Cell 20: Prepare Covariates
- Converts categorical variables to numeric for regression
- Creates: `grade_num`, `gender_female`, `overall_policy_num`, etc.

### Cell 21: Model A - Predict CREATIVITY_GENERAL
- Regression with controls
- Predicts `CREATIVITY_GENERAL` from `AI_USE_SCORE` + covariates

### Cell 22: Model B - Predict AUTHORSHIP_SCORE
- Regression with controls
- Predicts `AUTHORSHIP_SCORE` from `AI_USE_SCORE` + covariates

### Cell 23: Multicollinearity Check
- Correlation matrix of predictors

### Cell 24: Markdown - Moderation Section

### Cell 25: Model C - Moderation Analysis
- Tests if `AI_USE_SCORE × writing_ability` interaction affects `AUTHORSHIP_SCORE`
- Calculates simple slopes if interaction is significant

### Cell 26: Markdown - Clustering Section

### Cell 27: K-Means Clustering
- Identifies student profiles based on AI use, creativity, authorship, writing ability

### Cell 28: Cluster Visualization
- Plots cluster profiles

### Cell 29: Cluster Interpretation
- Describes what each cluster represents

### Cell 30: Markdown - Summary Section

### Cell 31: Summary of Key Results
- Compiles all key statistics for your paper

## Key Differences

| Aspect | Original (Cells 0-14) | Cleaned-Up (Cells 15+) |
|--------|----------------------|------------------------|
| **CREATIVITY_SCORE** | 5 items (WRONG) | 3 items → `CREATIVITY_GENERAL` (CORRECT) |
| **AUTHORSHIP_SCORE** | All items including `auth_worry_copy` (WRONG) | 4 core items only (CORRECT) |
| **Reverse Coding** | Inconsistent | Properly done |
| **Reliability** | Wrong scales | Correct scales |
| **Correlations** | Wrong scores | Correct scores |
| **Regression** | ❌ Not included | ✅ Models A, B, C |
| **Moderation** | ❌ Not included | ✅ Model C |
| **Clustering** | ❌ Not included | ✅ K-Means analysis |

## What You Should Do

### Option 1: Use Only the Cleaned-Up Section (Recommended)
1. **Keep cells 0-5**: Data loading and renaming (these are fine)
2. **Skip cells 6-14**: Old analysis with wrong definitions
3. **Use cells 15+**: All corrected analyses

### Option 2: Clean Up the Old Section
1. Delete or comment out cells 6-14 (the old analysis)
2. Keep only cells 15+ (the corrected analysis)

### Option 3: Keep Both (Not Recommended)
- You'll have duplicate/conflicting results
- Confusing which results to use for your paper

## For Your Paper

**Use results from:**
- Cell 16: Composite scores
- Cell 17: Reliability (Cronbach's Alpha)
- Cell 18: Correlations
- Cell 21: Model A results
- Cell 22: Model B results
- Cell 25: Model C results (if interaction is significant)
- Cell 27-29: Clustering results
- Cell 31: Summary statistics

**Do NOT use results from:**
- Cells 7-9: Old composite scores and correlations (wrong definitions)

## Questions?

If you're confused about:
- **Which scores to use**: Use `CREATIVITY_GENERAL` and `AUTHORSHIP_SCORE` from cell 16
- **Which correlations**: Use cell 18
- **Which reliability**: Use cell 17
- **Regression results**: Use cells 21, 22, 25



