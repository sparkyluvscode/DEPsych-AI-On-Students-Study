"""
Script to fix critical data issues identified in the analysis.

Run this BEFORE your main analysis to ensure data quality.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Load data
df = pd.read_csv("v3_data.csv", index_col=0)

# Apply your renaming (copy from your notebook)
rename_map = {
    "What is your age?": "age",
    "What is your current grade level?": "grade",
    "What is your gender?": "gender",
    "About how many writing assignments (paragraphs, essays, or written projects) do you complete for school in a typical week?": "assignments_per_week",
    "At your school, using AI tools for writing assignments is:": "overall_policy",
    "Compared to other students in my grade, I think my writing skills are:": "writing_ability",
    "I use AI tools (such as ChatGPT, Grammarly, or Gemini) to brainstorm ideas for my school writing.": "ai_brainstorm",
    "I use AI tools to help me draft or write full sentences and paragraphs for my assignments.\n": "ai_draft",
    "I use AI tools to edit or proofread my writing (for example, to fix grammar or wording).\n": "ai_edit",
    "I use AI tools when I am stuck and do not know how to continue my writing.\n": "ai_stuck",
    "Overall, I rely on AI tools when completing my writing assignments.\n": "ai_rely",
    "My writing feels creative and original when I work on school assignments.\n": "creat_feels_creative",
    "Using AI tools helps me come up with new ideas for my writing.\n": "creat_ai_helps_ideas",
    "When I use AI tools, my writing feels more creative than when I do not use them.\n": "creat_more_creative_with_ai",
    "I feel confident in my own ability to generate creative ideas for writing, even without AI.\n": "creat_conf_no_ai",
    "I enjoy experimenting with different ways to express my ideas in writing.\n": "creat_enjoy_writing",
    "The work I submit for writing assignments feels like it is primarily my own.\n": "auth_work_own",
    "When I use AI tools, I still feel that the ideas in my writing belong to me.\n": "auth_ideas_mine",
    "When I use AI tools, I sometimes feel less connected to the writing as \"my\" work.\n": "auth_less_connected",
    "I worry that using AI tools might make my writing feel less genuine or authentic.\n": "auth_less_authentic",
    "I feel comfortable taking credit for assignments where I used AI tools.\n": "auth_comfort_credit",
    "I worry that I'm using AI on my assignments more than I should, and that I could get caught": "auth_worry_copy",
    "How much have you been educated on AI use?": "artificial_intelligence_instruction",
}

df = df.rename(columns=rename_map)

# Create analysis dataframe
adf = df.copy()

# Define item groups
ai_items = ["ai_brainstorm", "ai_draft", "ai_edit", "ai_stuck", "ai_rely"]

creativity_items = [
    "creat_feels_creative",
    "creat_ai_helps_ideas",
    "creat_more_creative_with_ai",
    "creat_conf_no_ai",
    "creat_enjoy_writing",
]

# ============================================================================
# FIX #1: Improved Cronbach's Alpha (handles missing data)
# ============================================================================
def cronbach_alpha_fixed(df_subset, min_items_required=None):
    """
    Calculate Cronbach's alpha with proper missing data handling.
    
    Parameters:
    -----------
    df_subset : DataFrame
        Subset of dataframe with items to calculate alpha for
    min_items_required : int, optional
        Minimum number of items required (default: all items)
    
    Returns:
    --------
    float : Cronbach's alpha value
    """
    # Drop rows with ANY missing data for this calculation
    items_complete = df_subset.dropna()
    
    if items_complete.shape[0] < 2:
        return np.nan
    
    items = items_complete.to_numpy(dtype=float)
    k = items.shape[1]
    
    if k < 2:
        return np.nan
    
    item_vars = items.var(axis=0, ddof=1)
    total_scores = items.sum(axis=1)
    total_var = total_scores.var(ddof=1)
    
    if total_var == 0:  # All items identical
        return 1.0
    
    alpha = (k / (k-1)) * (1 - item_vars.sum() / total_var)
    return alpha


# ============================================================================
# FIX #2: Composite scores with missing data handling
# ============================================================================
def calculate_composite_score(df, items, min_items_required=None, method='mean'):
    """
    Calculate composite score with proper missing data handling.
    
    Parameters:
    -----------
    df : DataFrame
        Dataframe with items
    items : list
        List of column names to include
    min_items_required : int, optional
        Minimum number of non-missing items required (default: all items)
    method : str
        'mean' or 'sum'
    
    Returns:
    --------
    Series : Composite scores
    """
    if min_items_required is None:
        min_items_required = len(items)
    
    # Count non-missing items per row
    item_data = df[items]
    non_missing_count = item_data.notna().sum(axis=1)
    
    # Only calculate if enough items are present
    valid_mask = non_missing_count >= min_items_required
    
    if method == 'mean':
        scores = item_data.mean(axis=1, skipna=True)
    else:
        scores = item_data.sum(axis=1, skipna=True)
    
    # Set to NaN if not enough items
    scores[~valid_mask] = np.nan
    
    return scores


# ============================================================================
# FIX #3: Reverse code items properly
# ============================================================================
neg_auth_items = ["auth_less_connected", "auth_less_authentic", "auth_worry_copy"]

for col in neg_auth_items:
    if col in adf.columns:
        adf[col + "_REV"] = 6 - adf[col]  # 1-5 scale -> reverse

# ============================================================================
# Calculate composite scores (FIXED VERSION)
# ============================================================================
# AI Use Score - require at least 4 out of 5 items
adf["AI_USE_SCORE"] = calculate_composite_score(adf, ai_items, min_items_required=4)

# Creativity Score - require at least 4 out of 5 items
adf["CREATIVITY_SCORE"] = calculate_composite_score(adf, creativity_items, min_items_required=4)

# Authorship Score - DECIDE: which items to include?
# Option A: Full scale (5 items)
authorship_items_full = [
    "auth_work_own",
    "auth_ideas_mine",
    "auth_comfort_credit",
    "auth_less_connected_REV",
    "auth_less_authentic_REV",
]

# Option B: Core scale (4 items, excluding auth_work_own)
authorship_core_items = [
    "auth_ideas_mine",
    "auth_comfort_credit",
    "auth_less_connected_REV",
    "auth_less_authentic_REV",
]

# ⚠️ DECISION NEEDED: Which scale to use?
# Based on your reliability testing, use the one with better alpha
# For now, using core scale (you can change this)
adf["AUTHORSHIP_SCORE"] = calculate_composite_score(adf, authorship_core_items, min_items_required=3)

# Sub-scales
creativity_general_items = [
    "creat_feels_creative",
    "creat_conf_no_ai",
    "creat_enjoy_writing",
]

creativity_ai_boost_items = [
    "creat_ai_helps_ideas",
    "creat_more_creative_with_ai",
]

adf["CREATIVITY_GENERAL"] = calculate_composite_score(adf, creativity_general_items, min_items_required=2)
adf["CREATIVITY_AI_BOOST"] = calculate_composite_score(adf, creativity_ai_boost_items, min_items_required=1)

# ============================================================================
# FIX #4: Recalculate Cronbach's Alpha (CORRECTED)
# ============================================================================
print("=== RELIABILITY (CORRECTED) ===")
alpha_ai = cronbach_alpha_fixed(adf[ai_items])
alpha_creat = cronbach_alpha_fixed(adf[creativity_items])
alpha_auth = cronbach_alpha_fixed(adf[authorship_core_items])
alpha_creat_gen = cronbach_alpha_fixed(adf[creativity_general_items])

print(f"AI Use Scale: α = {alpha_ai:.3f}")
print(f"Creativity Scale: α = {alpha_creat:.3f}")
print(f"Authorship Scale (Core): α = {alpha_auth:.3f}")
print(f"Creativity General: α = {alpha_creat_gen:.3f}")

# ============================================================================
# FIX #5: Data Quality Checks
# ============================================================================
print("\n=== DATA QUALITY CHECKS ===")

# Check for invalid values (outside 1-5)
all_scale_items = ai_items + creativity_items + authorship_core_items
invalid_count = 0
for item in all_scale_items:
    if item in adf.columns:
        invalid = ((adf[item] < 1) | (adf[item] > 5)).sum()
        if invalid > 0:
            print(f"⚠️  {item}: {invalid} invalid values")
            invalid_count += invalid

if invalid_count == 0:
    print("✅ No invalid values found (all within 1-5 range)")

# Check for suspicious patterns (all same value)
suspicious_patterns = 0
for idx, row in adf.iterrows():
    ai_vals = [row[col] for col in ai_items if pd.notna(row.get(col)) and col in adf.columns]
    if len(ai_vals) >= 3:
        if len(set(ai_vals)) == 1:  # All same value
            suspicious_patterns += 1

if suspicious_patterns > 0:
    print(f"⚠️  {suspicious_patterns} participants with suspicious response patterns")
else:
    print("✅ No suspicious response patterns detected")

# Check missing data
print("\n=== MISSING DATA SUMMARY ===")
print(f"Total participants: {len(adf)}")
print(f"AI_USE_SCORE missing: {adf['AI_USE_SCORE'].isna().sum()} ({adf['AI_USE_SCORE'].isna().sum()/len(adf)*100:.1f}%)")
print(f"CREATIVITY_SCORE missing: {adf['CREATIVITY_SCORE'].isna().sum()} ({adf['CREATIVITY_SCORE'].isna().sum()/len(adf)*100:.1f}%)")
print(f"AUTHORSHIP_SCORE missing: {adf['AUTHORSHIP_SCORE'].isna().sum()} ({adf['AUTHORSHIP_SCORE'].isna().sum()/len(adf)*100:.1f}%)")

# ============================================================================
# FIX #6: Recalculate Correlations (with proper missing data handling)
# ============================================================================
print("\n=== CORRELATIONS (CORRECTED) ===")
pairs = [
    ("AI_USE_SCORE", "CREATIVITY_GENERAL"),
    ("AI_USE_SCORE", "AUTHORSHIP_SCORE"),
    ("CREATIVITY_GENERAL", "AUTHORSHIP_SCORE"),
]

for x, y in pairs:
    # Drop rows where either variable is missing
    valid_data = adf[[x, y]].dropna()
    if len(valid_data) > 2:
        r, p = pearsonr(valid_data[x], valid_data[y])
        print(f"{x} vs {y}: r = {r:.3f}, p = {p:.4f}, n = {len(valid_data)}")
    else:
        print(f"{x} vs {y}: Insufficient data")

# ============================================================================
# Save cleaned data
# ============================================================================
# Optionally save the cleaned dataframe
# adf.to_csv("v3_data_cleaned.csv")

print("\n=== FIXES APPLIED ===")
print("✅ Cronbach's alpha now handles missing data correctly")
print("✅ Composite scores handle missing data (require min items)")
print("✅ Data quality checks performed")
print("✅ Correlations recalculated with proper missing data handling")
print("\n⚠️  ACTION REQUIRED: Decide which authorship scale to use (full vs core)")





