
import pandas as pd
import numpy as np

df = pd.read_csv("v3_data.csv", index_col=0)

# After your renaming and score calculations:
print("=== MISSING DATA DIAGNOSTIC ===")
print(f"Total participants: {len(adf)}")
print(f"AI_USE_SCORE missing: {adf['AI_USE_SCORE'].isna().sum()}")
print(f"CREATIVITY_SCORE missing: {adf['CREATIVITY_SCORE'].isna().sum()}")
print(f"AUTHORSHIP_SCORE missing: {adf['AUTHORSHIP_SCORE'].isna().sum()}")

# Check which items have missing data
print("\n=== MISSING DATA BY ITEM ===")
for item in ai_items + creativity_items + authorship_items:
    missing = adf[item].isna().sum() if item in adf.columns else 0
    if missing > 0:
        print(f"{item}: {missing} missing ({missing/len(adf)*100:.1f}%)")
```

---

## 📝 What to Report in Your Paper

### Methods Section Should Include:
1. **Missing data handling**: 
   - "Composite scores were calculated as means of available items. Participants with missing data on >50% of items in a scale were excluded."
   
2. **Reliability**: 
   - "Cronbach's alpha was calculated using complete cases only."
   - Report the corrected alpha values

3. **Data quality**:
   - "We checked for invalid responses (values outside 1-5 range) and response patterns (e.g., all same value). X participants were excluded due to data quality issues."

4. **Scale construction**:
   - "The authorship scale included 4 items (auth_ideas_mine, auth_comfort_credit, auth_less_connected_REV, auth_less_authentic_REV) based on reliability testing."

---

## ⚠️ Final Recommendations

**Before writing your paper, you should:**
1. ✅ ~~Fix missing data handling~~ - **NOT NEEDED** (verified no missing data)
2. ✅ ~~Recalculate Cronbach's alpha~~ - **OPTIONAL** (works fine as-is)
3. **Verify which authorship scale you're using** - **IMPORTANT**
4. **Document all decisions about excluded items** - **IMPORTANT**

The authorship scale inconsistency (#3 and #4) is the main issue to address. Missing data is not a concern for your dataset.

---

*Report generated from analysis of v1_analysis_notebook.ipynb*
