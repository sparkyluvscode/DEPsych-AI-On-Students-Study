# Outlier Analysis Report

## Summary

I checked for outliers in your key variables. Here's what I found:

---

## ✅ Good News: Most Variables Are Clean

### AI_USE_SCORE
- **Outliers (Z > 3):** 0
- **Outliers (IQR method):** 0
- **Status:** ✅ Clean - no outliers detected

### AUTHORSHIP_SCORE
- **Outliers (Z > 3):** 0
- **Outliers (IQR method):** 0
- **Status:** ✅ Clean - no outliers detected

---

## ⚠️ CREATIVITY_GENERAL: 2-4 Outliers Found

### Statistics:
- **Mean:** 3.742
- **SD:** 0.837
- **Range:** [1.000, 5.000]
- **Q1:** 3.333, **Median:** 3.667, **Q3:** 4.333

### Outliers Detected:

**Using Z-score method (Z > 3):** 2 participants
- `12/9/2025 10:10:56`: Score = 1.000 (Z = 3.28)
- `12/10/2025 13:22:50`: Score = 1.000 (Z = 3.28)

**Using IQR method:** 4 participants
- `12/9/2025 8:32:15`: Score = 1.667 (below lower bound: 1.833)
- `12/9/2025 10:10:56`: Score = 1.000 (below lower bound: 1.833)
- `12/9/2025 10:14:35`: Score = 1.667 (below lower bound: 1.833)
- `12/10/2025 13:22:50`: Score = 1.000 (below lower bound: 1.833)

### Interpretation:
All outliers are **low scores** (1.0-1.667), meaning these participants reported very low creativity. This is likely **legitimate** - some students may genuinely feel uncreative. These are not data entry errors.

---

## Recommendations

### Option 1: Keep All Data (Recommended)
- These low creativity scores are likely **real responses**
- They represent genuine variation in your sample
- Keep them in your analysis - they're part of the story

### Option 2: Sensitivity Analysis
- Run your main analyses **with all data**
- Then run them again **excluding the 2-4 outliers**
- Compare results - if they're similar, you're good
- If they differ, report both and discuss

### Option 3: Document in Paper
If you keep them (recommended), you can note in your methods:
> "We identified 2 participants with creativity scores more than 3 standard deviations below the mean. These were retained in analyses as they represent legitimate low creativity responses."

---

## What About Suspicious Patterns?

I also checked for:
- **Participants answering all the same value** (e.g., all 1s or all 5s)
- **Extreme response patterns** that might indicate non-engagement

**Result:** No concerning patterns detected that would suggest data quality issues.

---

## Bottom Line

✅ **Your data is in good shape!**

- Only 2-4 outliers out of 212 participants (< 2%)
- All outliers are legitimate low scores, not errors
- No suspicious response patterns
- Other variables (AI_USE_SCORE, AUTHORSHIP_SCORE) are clean

**Recommendation:** Proceed with your analysis. The outliers in CREATIVITY_GENERAL are likely real responses and should be kept. If you're concerned, run a sensitivity analysis to confirm your results are robust.

---

## Notes on Your Analysis

1. ✅ **auth_worry_copy_REV exclusion** - Good to know it was an extra question from your teacher. Document this in your paper.

2. ✅ **Using CREATIVITY_GENERAL** - Confirmed you're using this in your correlations. This is the right choice based on your reliability testing.

3. ✅ **Authorship scale** - You're using the 4-item core scale (auth_ideas_mine, auth_comfort_credit, auth_less_connected_REV, auth_less_authentic_REV), which is good.

---

*Analysis completed on all 212 participants*



