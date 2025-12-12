#!/usr/bin/env python3
"""
Final Analysis Script for v4_data.csv (N=246)
Locked-in analysis with exports for paper writing
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import os
import json

# Try to import optional libraries
try:
    import statsmodels.formula.api as smf
    HAS_STATSMODELS = True
except (ImportError, ModuleNotFoundError):
    HAS_STATSMODELS = False
    print("WARNING: statsmodels not available. Regression models will be skipped.")

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("WARNING: sklearn not available. Clustering will be skipped.")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False
    print("WARNING: matplotlib/seaborn not available. Figures will be skipped.")

print("="*70)
print("FINAL ANALYSIS: v4_data.csv (N=246)")
print("="*70)
print()

# ============================================================================
# STEP 1: LOAD AND PREPARE v4 DATA
# ============================================================================

print("STEP 1: Loading v4_data.csv...")
df_v4 = pd.read_csv("v4_data.csv", index_col=0)

# Verify N
assert len(df_v4) == 246, f"Expected 246 rows, got {len(df_v4)}"
print(f"✓ Loaded {len(df_v4)} participants")

# Rename columns
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

# Handle column name variations
for col in df_v4.columns:
    if "less connected" in col.lower() and col not in rename_map:
        rename_map[col] = "auth_less_connected"
    if ("less genuine" in col.lower() or ("authentic" in col.lower() and "worry" not in col.lower())) and col not in rename_map:
        rename_map[col] = "auth_less_authentic"

df_v4 = df_v4.rename(columns=rename_map)
adf = df_v4.copy()

print("✓ Columns renamed")

# Calculate composite scores
print("\nCalculating composite scores...")

# AI Use Score (5 items)
ai_items = ["ai_brainstorm", "ai_draft", "ai_edit", "ai_stuck", "ai_rely"]
adf["AI_USE_SCORE"] = adf[ai_items].mean(axis=1)
print(f"✓ AI_USE_SCORE calculated (N={adf['AI_USE_SCORE'].notna().sum()})")

# Creativity General (3 items)
creativity_general_items = ["creat_feels_creative", "creat_conf_no_ai", "creat_enjoy_writing"]
adf["CREATIVITY_GENERAL"] = adf[creativity_general_items].mean(axis=1)
print(f"✓ CREATIVITY_GENERAL calculated (N={adf['CREATIVITY_GENERAL'].notna().sum()})")

# Authorship Score (4 items with reverse coding)
neg_auth_items = ["auth_less_connected", "auth_less_authentic"]
for col in neg_auth_items:
    if col in adf.columns:
        adf[col + "_REV"] = 6 - adf[col]

authorship_core_items = ["auth_ideas_mine", "auth_comfort_credit", "auth_less_connected_REV", "auth_less_authentic_REV"]
adf["AUTHORSHIP_SCORE"] = adf[authorship_core_items].mean(axis=1)
print(f"✓ AUTHORSHIP_SCORE calculated (N={adf['AUTHORSHIP_SCORE'].notna().sum()})")

# Prepare covariates
print("\nPreparing covariates...")

# grade_num
adf["grade_num"] = adf["grade"].str.extract(r"(\d+)").astype(float)
print(f"✓ grade_num: {adf['grade_num'].notna().sum()} valid")

# gender_female
adf["gender_female"] = (adf["gender"] == "Female").astype(int)
print(f"✓ gender_female: {adf['gender_female'].sum()} females")

# overall_policy_num
policy_map = {
    "Completely not tolerated": 1,
    "Mostly not tolerated": 2,
    "Sometimes allowed depending on the assignment": 3,
    "Mostly allowed": 4,
    "Completely allowed": 5,
}
adf["overall_policy_num"] = adf["overall_policy"].map(policy_map)
print(f"✓ overall_policy_num: {adf['overall_policy_num'].notna().sum()} valid")

# assignments_per_week_num
if adf["assignments_per_week"].dtype == 'object':
    assignments_map = {"0-1": 1, "1": 1, "2-3": 2.5, "4-5": 4.5, "6+": 6}
    adf["assignments_per_week_num"] = adf["assignments_per_week"].map(assignments_map)
    adf["assignments_per_week_num"] = adf["assignments_per_week_num"].fillna(
        adf["assignments_per_week"].str.extract(r"(\d+)")[0].astype(float)
    )
else:
    adf["assignments_per_week_num"] = adf["assignments_per_week"]
print(f"✓ assignments_per_week_num: {adf['assignments_per_week_num'].notna().sum()} valid")

# artificial_intelligence_instruction_num
if adf["artificial_intelligence_instruction"].dtype == 'object':
    ai_edu_map = {"None at all": 1, "A little": 2, "Some": 3, "Quite a bit": 4, "A lot": 5}
    adf["artificial_intelligence_instruction_num"] = adf["artificial_intelligence_instruction"].map(ai_edu_map)
else:
    adf["artificial_intelligence_instruction_num"] = adf["artificial_intelligence_instruction"]
print(f"✓ artificial_intelligence_instruction_num: {adf['artificial_intelligence_instruction_num'].notna().sum()} valid")

# writing_ability_num
if adf["writing_ability"].dtype == 'object':
    writing_ability_map = {"Much worse": 1, "A little worse": 2, "About the same": 3, "A little better": 4, "Much better": 5}
    adf["writing_ability_num"] = adf["writing_ability"].map(writing_ability_map)
else:
    adf["writing_ability_num"] = adf["writing_ability"]
print(f"✓ writing_ability_num: {adf['writing_ability_num'].notna().sum()} valid")

# Check for missing values in key variables
print("\nChecking missing values in key variables...")
key_vars = ["AI_USE_SCORE", "CREATIVITY_GENERAL", "AUTHORSHIP_SCORE", 
            "grade_num", "gender_female", "writing_ability_num", 
            "assignments_per_week_num", "overall_policy_num", 
            "artificial_intelligence_instruction_num"]
for var in key_vars:
    missing = adf[var].isna().sum()
    if missing > 0:
        print(f"  {var}: {missing} missing")

print("\n" + "="*70)

# ============================================================================
# STEP 2: RELIABILITY AND DESCRIPTIVES
# ============================================================================

print("STEP 2: Reliability and Descriptive Statistics")
print()

def cronbach_alpha(df_subset):
    """Calculate Cronbach's alpha for internal consistency reliability."""
    items = df_subset.to_numpy(dtype=float)
    item_vars = items.var(axis=0, ddof=1)
    total_scores = items.sum(axis=1)
    total_var = total_scores.var(ddof=1)
    k = items.shape[1]
    return (k / (k-1)) * (1 - item_vars.sum() / total_var)

# Reliability
alpha_ai = cronbach_alpha(adf[ai_items])
alpha_creat_gen = cronbach_alpha(adf[creativity_general_items])
alpha_auth_core = cronbach_alpha(adf[authorship_core_items])

print("Reliability (Cronbach's Alpha):")
print(f"  AI_USE_SCORE: α = {alpha_ai:.3f}")
print(f"  CREATIVITY_GENERAL: α = {alpha_creat_gen:.3f}")
print(f"  AUTHORSHIP_SCORE: α = {alpha_auth_core:.3f}")

# Descriptives
desc_vars = ["AI_USE_SCORE", "CREATIVITY_GENERAL", "AUTHORSHIP_SCORE"]
desc_data = []

for var in desc_vars:
    n = adf[var].notna().sum()
    mean = adf[var].mean()
    sd = adf[var].std()
    min_val = adf[var].min()
    max_val = adf[var].max()
    
    # Get alpha
    if var == "AI_USE_SCORE":
        alpha = alpha_ai
    elif var == "CREATIVITY_GENERAL":
        alpha = alpha_creat_gen
    else:
        alpha = alpha_auth_core
    
    desc_data.append({
        "variable_name": var,
        "N": n,
        "mean": mean,
        "sd": sd,
        "min": min_val,
        "max": max_val,
        "alpha": alpha
    })
    
    print(f"\n{var}:")
    print(f"  N = {n}")
    print(f"  M = {mean:.3f}")
    print(f"  SD = {sd:.3f}")
    print(f"  Min = {min_val:.3f}")
    print(f"  Max = {max_val:.3f}")
    print(f"  α = {alpha:.3f}")

# Create Table 1
table1 = pd.DataFrame(desc_data)
print("\n✓ Table 1 (Descriptives + Reliability) created")

# ============================================================================
# STEP 3: CORRELATION MATRIX
# ============================================================================

print("\n" + "="*70)
print("STEP 3: Correlation Matrix")
print()

corr_vars = ["AI_USE_SCORE", "CREATIVITY_GENERAL", "AUTHORSHIP_SCORE",
              "writing_ability_num", "artificial_intelligence_instruction_num", 
              "overall_policy_num"]

corr_data = adf[corr_vars].dropna()
corr_matrix = corr_data.corr()

print("Correlation Matrix:")
print(corr_matrix.round(3))

# Store key correlations with p-values
key_corrs = {
    "AI_USE_vs_CREATIVITY": {"r": None, "p": None},
    "AI_USE_vs_AUTHORSHIP": {"r": None, "p": None},
    "CREATIVITY_vs_AUTHORSHIP": {"r": None, "p": None},
}

r1, p1 = pearsonr(adf['AI_USE_SCORE'], adf['CREATIVITY_GENERAL'])
r2, p2 = pearsonr(adf['AI_USE_SCORE'], adf['AUTHORSHIP_SCORE'])
r3, p3 = pearsonr(adf['CREATIVITY_GENERAL'], adf['AUTHORSHIP_SCORE'])

key_corrs["AI_USE_vs_CREATIVITY"]["r"] = r1
key_corrs["AI_USE_vs_CREATIVITY"]["p"] = p1
key_corrs["AI_USE_vs_AUTHORSHIP"]["r"] = r2
key_corrs["AI_USE_vs_AUTHORSHIP"]["p"] = p2
key_corrs["CREATIVITY_vs_AUTHORSHIP"]["r"] = r3
key_corrs["CREATIVITY_vs_AUTHORSHIP"]["p"] = p3

print("\nKey Correlations:")
print(f"  AI_USE vs CREATIVITY: r = {r1:.3f}, p = {p1:.4f}")
print(f"  AI_USE vs AUTHORSHIP: r = {r2:.3f}, p = {p2:.4f}")
print(f"  CREATIVITY vs AUTHORSHIP: r = {r3:.3f}, p = {p3:.4f}")

print("\n✓ Table 2 (Correlation Matrix) created")

# ============================================================================
# STEP 4: REGRESSION MODELS
# ============================================================================

if HAS_STATSMODELS:
    print("\n" + "="*70)
    print("STEP 4: Regression Models")
    print()
    
    # Prepare regression data (listwise deletion)
    reg_vars = ["CREATIVITY_GENERAL", "AUTHORSHIP_SCORE", "AI_USE_SCORE",
                "grade_num", "gender_female", "writing_ability_num",
                "assignments_per_week_num", "overall_policy_num",
                "artificial_intelligence_instruction_num"]
    
    reg_data = adf[reg_vars].dropna()
    n_reg = len(reg_data)
    print(f"Regression sample size (listwise deletion): N = {n_reg}")
    
    # Model A: Predicting CREATIVITY_GENERAL
    print("\nModel A: Predicting CREATIVITY_GENERAL")
    model_a = smf.ols(
        "CREATIVITY_GENERAL ~ AI_USE_SCORE + grade_num + gender_female + "
        "writing_ability_num + assignments_per_week_num + overall_policy_num + "
        "artificial_intelligence_instruction_num",
        data=reg_data
    ).fit()
    
    ai_use_a = model_a.params['AI_USE_SCORE']
    ai_use_se_a = model_a.bse['AI_USE_SCORE']
    ai_use_t_a = model_a.tvalues['AI_USE_SCORE']
    ai_use_p_a = model_a.pvalues['AI_USE_SCORE']
    
    print(f"  N = {model_a.nobs}")
    print(f"  R² = {model_a.rsquared:.3f}")
    print(f"  AI_USE_SCORE: B = {ai_use_a:.3f}, SE = {ai_use_se_a:.3f}, "
          f"t = {ai_use_t_a:.3f}, p = {ai_use_p_a:.4f}")
    
    # Model B: Predicting AUTHORSHIP_SCORE
    print("\nModel B: Predicting AUTHORSHIP_SCORE")
    model_b = smf.ols(
        "AUTHORSHIP_SCORE ~ AI_USE_SCORE + grade_num + gender_female + "
        "writing_ability_num + assignments_per_week_num + overall_policy_num + "
        "artificial_intelligence_instruction_num",
        data=reg_data
    ).fit()
    
    ai_use_b = model_b.params['AI_USE_SCORE']
    ai_use_se_b = model_b.bse['AI_USE_SCORE']
    ai_use_t_b = model_b.tvalues['AI_USE_SCORE']
    ai_use_p_b = model_b.pvalues['AI_USE_SCORE']
    
    print(f"  N = {model_b.nobs}")
    print(f"  R² = {model_b.rsquared:.3f}")
    print(f"  AI_USE_SCORE: B = {ai_use_b:.3f}, SE = {ai_use_se_b:.3f}, "
          f"t = {ai_use_t_b:.3f}, p = {ai_use_p_b:.4f}")
    
    # Model C: Moderation
    print("\nModel C: Moderation (AUTHORSHIP_SCORE with interaction)")
    model_c = smf.ols(
        "AUTHORSHIP_SCORE ~ AI_USE_SCORE * writing_ability_num + grade_num + "
        "gender_female + assignments_per_week_num + overall_policy_num + "
        "artificial_intelligence_instruction_num",
        data=reg_data
    ).fit()
    
    if 'AI_USE_SCORE:writing_ability_num' in model_c.params.index:
        int_coef = model_c.params['AI_USE_SCORE:writing_ability_num']
        int_se = model_c.bse['AI_USE_SCORE:writing_ability_num']
        int_t = model_c.tvalues['AI_USE_SCORE:writing_ability_num']
        int_p = model_c.pvalues['AI_USE_SCORE:writing_ability_num']
        
        print(f"  N = {model_c.nobs}")
        print(f"  R² = {model_c.rsquared:.3f}")
        print(f"  Interaction (AI_USE × writing_ability): B = {int_coef:.3f}, "
              f"SE = {int_se:.3f}, t = {int_t:.3f}, p = {int_p:.4f}")
    else:
        int_coef = int_se = int_t = int_p = None
        print("  Interaction term not found")
    
    # Store regression results
    reg_results = {
        "model_a": {
            "model_name": "Model A",
            "outcome_name": "CREATIVITY_GENERAL",
            "N": int(model_a.nobs),
            "R2": model_a.rsquared,
            "AI_USE_SCORE_B": ai_use_a,
            "AI_USE_SCORE_SE": ai_use_se_a,
            "AI_USE_SCORE_p": ai_use_p_a,
        },
        "model_b": {
            "model_name": "Model B",
            "outcome_name": "AUTHORSHIP_SCORE",
            "N": int(model_b.nobs),
            "R2": model_b.rsquared,
            "AI_USE_SCORE_B": ai_use_b,
            "AI_USE_SCORE_SE": ai_use_se_b,
            "AI_USE_SCORE_p": ai_use_p_b,
        },
        "model_c": {
            "model_name": "Model C",
            "outcome_name": "AUTHORSHIP_SCORE",
            "N": int(model_c.nobs),
            "R2": model_c.rsquared,
            "interaction_B": int_coef,
            "interaction_SE": int_se,
            "interaction_p": int_p,
        }
    }
    
    print("\n✓ Regression models completed")
else:
    reg_results = None
    print("\n⚠ Regression models skipped (statsmodels not available)")

# ============================================================================
# STEP 5: CLUSTERING (OPTIONAL)
# ============================================================================

cluster_results = None
if HAS_SKLEARN:
    print("\n" + "="*70)
    print("STEP 5: Clustering Analysis")
    print()
    
    cluster_features = adf[[
        "AI_USE_SCORE", "CREATIVITY_GENERAL", "AUTHORSHIP_SCORE",
        "writing_ability_num", "artificial_intelligence_instruction_num"
    ]].dropna()
    
    print(f"Clustering on {len(cluster_features)} participants with complete data")
    
    scaler = StandardScaler()
    X = scaler.fit_transform(cluster_features)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_features = cluster_features.copy()
    cluster_features["cluster"] = kmeans.fit_predict(X)
    
    cluster_means = cluster_features.groupby("cluster").mean()
    cluster_sizes = cluster_features["cluster"].value_counts().sort_index()
    
    print("\nCluster Profiles:")
    cluster_profiles = []
    for cluster_id in sorted(cluster_features["cluster"].unique()):
        n = cluster_sizes[cluster_id]
        means = cluster_means.loc[cluster_id]
        cluster_profiles.append({
            "cluster": int(cluster_id),
            "N": int(n),
            "AI_USE_SCORE": means["AI_USE_SCORE"],
            "CREATIVITY_GENERAL": means["CREATIVITY_GENERAL"],
            "AUTHORSHIP_SCORE": means["AUTHORSHIP_SCORE"],
            "writing_ability_num": means["writing_ability_num"],
            "artificial_intelligence_instruction_num": means["artificial_intelligence_instruction_num"],
        })
        print(f"\nCluster {cluster_id} (n = {n}):")
        print(f"  AI_USE_SCORE: {means['AI_USE_SCORE']:.3f}")
        print(f"  CREATIVITY_GENERAL: {means['CREATIVITY_GENERAL']:.3f}")
        print(f"  AUTHORSHIP_SCORE: {means['AUTHORSHIP_SCORE']:.3f}")
        print(f"  writing_ability_num: {means['writing_ability_num']:.3f}")
        print(f"  artificial_intelligence_instruction_num: {means['artificial_intelligence_instruction_num']:.3f}")
    
    cluster_results = pd.DataFrame(cluster_profiles)
    print("\n✓ Clustering completed")
else:
    print("\n⚠ Clustering skipped (sklearn not available)")

# ============================================================================
# STEP 6: EXPORT DATA, TABLES, AND FIGURES
# ============================================================================

print("\n" + "="*70)
print("STEP 6: Exporting Data, Tables, and Figures")
print()

# Create directories
os.makedirs("data", exist_ok=True)
os.makedirs("tables", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# Export clean dataset
export_cols = [
    "AI_USE_SCORE", "CREATIVITY_GENERAL", "AUTHORSHIP_SCORE",
    "grade_num", "gender_female", "writing_ability_num",
    "assignments_per_week_num", "overall_policy_num",
    "artificial_intelligence_instruction_num"
] + ai_items + creativity_general_items + authorship_core_items

# Only include columns that exist
export_cols = [col for col in export_cols if col in adf.columns]

adf_clean = adf[export_cols].copy()
adf_clean.to_csv("data/ai_psych_final_v4_clean.csv", index=True)
print("✓ Exported: data/ai_psych_final_v4_clean.csv")

# Export tables
table1.to_csv("tables/table1_descriptives_reliability.csv", index=False)
print("✓ Exported: tables/table1_descriptives_reliability.csv")

corr_matrix.to_csv("tables/table2_correlation_matrix.csv")
print("✓ Exported: tables/table2_correlation_matrix.csv")

if reg_results:
    # Create regression summary table
    reg_summary = []
    for model_key in ["model_a", "model_b"]:
        m = reg_results[model_key]
        reg_summary.append({
            "Model": m["model_name"],
            "Outcome": m["outcome_name"],
            "N": m["N"],
            "R2": m["R2"],
            "AI_USE_B": m["AI_USE_SCORE_B"],
            "AI_USE_SE": m["AI_USE_SCORE_SE"],
            "AI_USE_p": m["AI_USE_SCORE_p"],
        })
    
    reg_table = pd.DataFrame(reg_summary)
    reg_table.to_csv("tables/table3_regression_summary.csv", index=False)
    print("✓ Exported: tables/table3_regression_summary.csv")
    
    # Export full regression results as JSON
    with open("tables/regression_results.json", "w") as f:
        json.dump(reg_results, f, indent=2, default=str)
    print("✓ Exported: tables/regression_results.json")

if cluster_results is not None:
    cluster_results.to_csv("tables/table4_cluster_profiles.csv", index=False)
    print("✓ Exported: tables/table4_cluster_profiles.csv")

# Export figures
if HAS_PLOTTING:
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Histograms
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    adf['AI_USE_SCORE'].hist(ax=axes[0], bins=20, edgecolor='black')
    axes[0].set_xlabel('AI Use Score')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution of AI Use Score')
    
    adf['CREATIVITY_GENERAL'].hist(ax=axes[1], bins=20, edgecolor='black')
    axes[1].set_xlabel('Creativity General')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Distribution of Creativity General')
    
    adf['AUTHORSHIP_SCORE'].hist(ax=axes[2], bins=20, edgecolor='black')
    axes[2].set_xlabel('Authorship Score')
    axes[2].set_ylabel('Frequency')
    axes[2].set_title('Distribution of Authorship Score')
    
    plt.tight_layout()
    plt.savefig('figures/histograms_main_variables.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Exported: figures/histograms_main_variables.png")
    
    # Scatterplots with regression lines
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # AI_USE vs CREATIVITY
    axes[0].scatter(adf['AI_USE_SCORE'], adf['CREATIVITY_GENERAL'], alpha=0.5, s=30)
    z = np.polyfit(adf['AI_USE_SCORE'].dropna(), adf['CREATIVITY_GENERAL'].dropna(), 1)
    p = np.poly1d(z)
    axes[0].plot(adf['AI_USE_SCORE'].sort_values(), p(adf['AI_USE_SCORE'].sort_values()), "r--", alpha=0.8)
    axes[0].set_xlabel('AI Use Score')
    axes[0].set_ylabel('Creativity General')
    axes[0].set_title(f'AI Use vs Creativity (r = {r1:.3f})')
    axes[0].grid(True, alpha=0.3)
    
    # AI_USE vs AUTHORSHIP
    axes[1].scatter(adf['AI_USE_SCORE'], adf['AUTHORSHIP_SCORE'], alpha=0.5, s=30)
    z = np.polyfit(adf['AI_USE_SCORE'].dropna(), adf['AUTHORSHIP_SCORE'].dropna(), 1)
    p = np.poly1d(z)
    axes[1].plot(adf['AI_USE_SCORE'].sort_values(), p(adf['AI_USE_SCORE'].sort_values()), "r--", alpha=0.8)
    axes[1].set_xlabel('AI Use Score')
    axes[1].set_ylabel('Authorship Score')
    axes[1].set_title(f'AI Use vs Authorship (r = {r2:.3f})')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/scatterplots_main_relationships.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Exported: figures/scatterplots_main_relationships.png")
else:
    print("⚠ Figures skipped (matplotlib not available)")

print("\n" + "="*70)

# ============================================================================
# STEP 7: FINAL SUMMARY FOR CHATGPT
# ============================================================================

print("\n" + "="*70)
print("[RESULTS_FOR_CHATGPT]")
print("="*70)
print()

print(f"N_final = {len(adf)}")
print()

print("Reliability:")
print(f"  • AI_USE_SCORE: alpha = {alpha_ai:.3f}")
print(f"  • CREATIVITY_GENERAL: alpha = {alpha_creat_gen:.3f}")
print(f"  • AUTHORSHIP_SCORE: alpha = {alpha_auth_core:.3f}")
print()

print("Descriptives (v4):")
for var in desc_vars:
    row = table1[table1['variable_name'] == var].iloc[0]
    print(f"  • {var}: M = {row['mean']:.3f}, SD = {row['sd']:.3f}, "
          f"min = {row['min']:.3f}, max = {row['max']:.3f}")
print()

print("Correlations (v4):")
print(f"  • r(AI_USE, CREATIVITY_GENERAL) = {r1:.3f}, p = {p1:.4f}")
print(f"  • r(AI_USE, AUTHORSHIP_SCORE) = {r2:.3f}, p = {p2:.4f}")
print(f"  • r(CREATIVITY_GENERAL, AUTHORSHIP_SCORE) = {r3:.3f}, p = {p3:.4f}")
print()

if reg_results:
    print("Regression Model A (Outcome: CREATIVITY_GENERAL):")
    m = reg_results["model_a"]
    print(f"  • N = {m['N']}")
    print(f"  • R2 = {m['R2']:.3f}")
    print(f"  • AI_USE_SCORE: B = {m['AI_USE_SCORE_B']:.3f}, "
          f"SE = {m['AI_USE_SCORE_SE']:.3f}, p = {m['AI_USE_SCORE_p']:.4f}")
    print()
    
    print("Regression Model B (Outcome: AUTHORSHIP_SCORE):")
    m = reg_results["model_b"]
    print(f"  • N = {m['N']}")
    print(f"  • R2 = {m['R2']:.3f}")
    print(f"  • AI_USE_SCORE: B = {m['AI_USE_SCORE_B']:.3f}, "
          f"SE = {m['AI_USE_SCORE_SE']:.3f}, p = {m['AI_USE_SCORE_p']:.4f}")
    print()
    
    print("Regression Model C (Moderation: Outcome = AUTHORSHIP_SCORE):")
    m = reg_results["model_c"]
    print(f"  • N = {m['N']}")
    print(f"  • R2 = {m['R2']:.3f}")
    if m['interaction_B'] is not None:
        print(f"  • Interaction (AI_USE * writing_ability_num): B = {m['interaction_B']:.3f}, "
              f"SE = {m['interaction_SE']:.3f}, p = {m['interaction_p']:.4f}")
    else:
        print("  • Interaction term not available")
    print()
else:
    print("Regression Models: Not available (statsmodels required)")
    print()

if cluster_results is not None:
    print("Cluster Profiles:")
    for _, row in cluster_results.iterrows():
        print(f"  • Cluster {int(row['cluster'])}: N = {int(row['N'])}, "
              f"AI_USE = {row['AI_USE_SCORE']:.3f}, "
              f"Creativity = {row['CREATIVITY_GENERAL']:.3f}, "
              f"Authorship = {row['AUTHORSHIP_SCORE']:.3f}")
    print()
else:
    print("Cluster Profiles: Not computed")
    print()

print("Exported files:")
print("  • data/ai_psych_final_v4_clean.csv")
print("  • tables/table1_descriptives_reliability.csv")
print("  • tables/table2_correlation_matrix.csv")
if reg_results:
    print("  • tables/table3_regression_summary.csv")
    print("  • tables/regression_results.json")
if cluster_results is not None:
    print("  • tables/table4_cluster_profiles.csv")
if HAS_PLOTTING:
    print("  • figures/histograms_main_variables.png")
    print("  • figures/scatterplots_main_relationships.png")

print()
print("="*70)
print("[/RESULTS_FOR_CHATGPT]")
print("="*70)

print("\n✓ Analysis complete!")

