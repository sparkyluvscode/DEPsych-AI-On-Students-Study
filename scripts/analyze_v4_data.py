#!/usr/bin/env python3
"""
Comprehensive analysis of v4_data.csv
Generates results for ChatGPT report
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr

try:
    import statsmodels.formula.api as smf
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("Warning: statsmodels not available, skipping regression analyses")

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: sklearn not available, skipping clustering")

# Load v4_data.csv
print("Loading v4_data.csv...")
df_v4 = pd.read_csv("v4_data.csv", index_col=0)

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
adf_v4 = df_v4.copy()

# Calculate composite scores
ai_items = ["ai_brainstorm", "ai_draft", "ai_edit", "ai_stuck", "ai_rely"]
creativity_general_items = ["creat_feels_creative", "creat_conf_no_ai", "creat_enjoy_writing"]
creativity_ai_boost_items = ["creat_ai_helps_ideas", "creat_more_creative_with_ai"]

adf_v4["AI_USE_SCORE"] = adf_v4[ai_items].mean(axis=1)
adf_v4["CREATIVITY_GENERAL"] = adf_v4[creativity_general_items].mean(axis=1)
adf_v4["CREATIVITY_AI_BOOST"] = adf_v4[creativity_ai_boost_items].mean(axis=1)

# Reverse code authorship items
neg_auth_items = ["auth_less_connected", "auth_less_authentic"]
for col in neg_auth_items:
    if col in adf_v4.columns:
        adf_v4[col + "_REV"] = 6 - adf_v4[col]

authorship_core_items = ["auth_ideas_mine", "auth_comfort_credit", "auth_less_connected_REV", "auth_less_authentic_REV"]
adf_v4["AUTHORSHIP_SCORE"] = adf_v4[authorship_core_items].mean(axis=1)

# Reliability
def cronbach_alpha(df_subset):
    items = df_subset.to_numpy(dtype=float)
    item_vars = items.var(axis=0, ddof=1)
    total_scores = items.sum(axis=1)
    total_var = total_scores.var(ddof=1)
    k = items.shape[1]
    return (k / (k-1)) * (1 - item_vars.sum() / total_var)

alpha_ai_v4 = cronbach_alpha(adf_v4[ai_items])
alpha_creat_gen_v4 = cronbach_alpha(adf_v4[creativity_general_items])
alpha_auth_core_v4 = cronbach_alpha(adf_v4[authorship_core_items])

# Correlations
r1_v4, p1_v4 = pearsonr(adf_v4['AI_USE_SCORE'], adf_v4['CREATIVITY_GENERAL'])
r2_v4, p2_v4 = pearsonr(adf_v4['AI_USE_SCORE'], adf_v4['AUTHORSHIP_SCORE'])
r3_v4, p3_v4 = pearsonr(adf_v4['CREATIVITY_GENERAL'], adf_v4['AUTHORSHIP_SCORE'])

# Prepare covariates
adf_v4["grade_num"] = adf_v4["grade"].str.extract(r"(\d+)").astype(float)
adf_v4["gender_female"] = (adf_v4["gender"] == "Female").astype(int)

policy_map = {"Completely not tolerated": 1, "Mostly not tolerated": 2, "Sometimes allowed depending on the assignment": 3, "Mostly allowed": 4, "Completely allowed": 5}
adf_v4["overall_policy_num"] = adf_v4["overall_policy"].map(policy_map)

if adf_v4["assignments_per_week"].dtype == 'object':
    assignments_map = {"0-1": 1, "1": 1, "2-3": 2.5, "4-5": 4.5, "6+": 6}
    adf_v4["assignments_per_week_num"] = adf_v4["assignments_per_week"].map(assignments_map)
    adf_v4["assignments_per_week_num"] = adf_v4["assignments_per_week_num"].fillna(adf_v4["assignments_per_week"].str.extract(r"(\d+)")[0].astype(float))
else:
    adf_v4["assignments_per_week_num"] = adf_v4["assignments_per_week"]

if adf_v4["artificial_intelligence_instruction"].dtype == 'object':
    ai_edu_map = {"None at all": 1, "A little": 2, "Some": 3, "Quite a bit": 4, "A lot": 5}
    adf_v4["artificial_intelligence_instruction_num"] = adf_v4["artificial_intelligence_instruction"].map(ai_edu_map)
else:
    adf_v4["artificial_intelligence_instruction_num"] = adf_v4["artificial_intelligence_instruction"]

if adf_v4["writing_ability"].dtype == 'object':
    writing_ability_map = {"Much worse": 1, "A little worse": 2, "About the same": 3, "A little better": 4, "Much better": 5}
    adf_v4["writing_ability_num"] = adf_v4["writing_ability"].map(writing_ability_map)
else:
    adf_v4["writing_ability_num"] = adf_v4["writing_ability"]

# Regression analyses
results = {
    "sample_size": len(adf_v4),
    "reliability": {
        "ai_use": alpha_ai_v4,
        "creativity_general": alpha_creat_gen_v4,
        "authorship_core": alpha_auth_core_v4,
    },
    "correlations": {
        "ai_use_creativity": {"r": r1_v4, "p": p1_v4},
        "ai_use_authorship": {"r": r2_v4, "p": p2_v4},
        "creativity_authorship": {"r": r3_v4, "p": p3_v4},
    },
    "descriptives": {
        "ai_use": {"mean": adf_v4['AI_USE_SCORE'].mean(), "sd": adf_v4['AI_USE_SCORE'].std()},
        "creativity": {"mean": adf_v4['CREATIVITY_GENERAL'].mean(), "sd": adf_v4['CREATIVITY_GENERAL'].std()},
        "authorship": {"mean": adf_v4['AUTHORSHIP_SCORE'].mean(), "sd": adf_v4['AUTHORSHIP_SCORE'].std()},
    },
}

if HAS_STATSMODELS:
    # Regression Model A
    model_creat_v4 = smf.ols("CREATIVITY_GENERAL ~ AI_USE_SCORE + grade_num + gender_female + writing_ability_num + assignments_per_week_num + overall_policy_num + artificial_intelligence_instruction_num", data=adf_v4).fit()
    
    # Regression Model B
    model_auth_v4 = smf.ols("AUTHORSHIP_SCORE ~ AI_USE_SCORE + grade_num + gender_female + writing_ability_num + assignments_per_week_num + overall_policy_num + artificial_intelligence_instruction_num", data=adf_v4).fit()
    
    # Moderation Model C
    model_auth_int_v4 = smf.ols("AUTHORSHIP_SCORE ~ AI_USE_SCORE * writing_ability_num + grade_num + gender_female + assignments_per_week_num + overall_policy_num + artificial_intelligence_instruction_num", data=adf_v4).fit()
    
    results["regression"] = {
        "model_a": {
            "ai_use_coef": model_creat_v4.params['AI_USE_SCORE'],
            "ai_use_p": model_creat_v4.pvalues['AI_USE_SCORE'],
            "rsquared": model_creat_v4.rsquared,
            "n": model_creat_v4.nobs,
        },
        "model_b": {
            "ai_use_coef": model_auth_v4.params['AI_USE_SCORE'],
            "ai_use_p": model_auth_v4.pvalues['AI_USE_SCORE'],
            "rsquared": model_auth_v4.rsquared,
            "n": model_auth_v4.nobs,
        },
    }
    
    if 'AI_USE_SCORE:writing_ability_num' in model_auth_int_v4.params.index:
        results["moderation"] = {
            "interaction_coef": model_auth_int_v4.params['AI_USE_SCORE:writing_ability_num'],
            "interaction_p": model_auth_int_v4.pvalues['AI_USE_SCORE:writing_ability_num'],
        }

if HAS_SKLEARN:
    cluster_features_v4 = adf_v4[["AI_USE_SCORE", "CREATIVITY_GENERAL", "AUTHORSHIP_SCORE", "writing_ability_num", "artificial_intelligence_instruction_num"]].dropna()
    scaler_v4 = StandardScaler()
    X_v4 = scaler_v4.fit_transform(cluster_features_v4)
    kmeans_v4 = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_features_v4 = cluster_features_v4.copy()
    cluster_features_v4["cluster"] = kmeans_v4.fit_predict(X_v4)
    cluster_means_v4 = cluster_features_v4.groupby("cluster").mean()
    cluster_sizes_v4 = cluster_features_v4["cluster"].value_counts().sort_index()
    
    results["clustering"] = {
        "n_clustered": len(cluster_features_v4),
        "cluster_sizes": cluster_sizes_v4.to_dict(),
        "cluster_means": cluster_means_v4.to_dict(),
    }

# Print results
print("\n" + "="*70)
print("V4 DATA ANALYSIS RESULTS")
print("="*70)
print(f"\nSample size: {results['sample_size']} participants")
print(f"\nRELIABILITY:")
print(f"  AI Use: α = {results['reliability']['ai_use']:.3f}")
print(f"  Creativity General: α = {results['reliability']['creativity_general']:.3f}")
print(f"  Authorship Core: α = {results['reliability']['authorship_core']:.3f}")
print(f"\nCORRELATIONS:")
print(f"  AI_USE vs CREATIVITY: r = {results['correlations']['ai_use_creativity']['r']:.3f}, p = {results['correlations']['ai_use_creativity']['p']:.4f}")
print(f"  AI_USE vs AUTHORSHIP: r = {results['correlations']['ai_use_authorship']['r']:.3f}, p = {results['correlations']['ai_use_authorship']['p']:.4f}")
print(f"  CREATIVITY vs AUTHORSHIP: r = {results['correlations']['creativity_authorship']['r']:.3f}, p = {results['correlations']['creativity_authorship']['p']:.4f}")

if "regression" in results:
    print(f"\nREGRESSION MODEL A (Creativity):")
    print(f"  AI_USE_SCORE: β = {results['regression']['model_a']['ai_use_coef']:.3f}, p = {results['regression']['model_a']['ai_use_p']:.4f}, R² = {results['regression']['model_a']['rsquared']:.3f}, n = {results['regression']['model_a']['n']}")
    print(f"\nREGRESSION MODEL B (Authorship):")
    print(f"  AI_USE_SCORE: β = {results['regression']['model_b']['ai_use_coef']:.3f}, p = {results['regression']['model_b']['ai_use_p']:.4f}, R² = {results['regression']['model_b']['rsquared']:.3f}, n = {results['regression']['model_b']['n']}")

if "moderation" in results:
    print(f"\nMODERATION (Interaction):")
    print(f"  Interaction: β = {results['moderation']['interaction_coef']:.3f}, p = {results['moderation']['interaction_p']:.4f}")

print(f"\nDESCRIPTIVE STATISTICS:")
print(f"  AI_USE_SCORE: M = {results['descriptives']['ai_use']['mean']:.2f}, SD = {results['descriptives']['ai_use']['sd']:.2f}")
print(f"  CREATIVITY_GENERAL: M = {results['descriptives']['creativity']['mean']:.2f}, SD = {results['descriptives']['creativity']['sd']:.2f}")
print(f"  AUTHORSHIP_SCORE: M = {results['descriptives']['authorship']['mean']:.2f}, SD = {results['descriptives']['authorship']['sd']:.2f}")

if "clustering" in results:
    print(f"\nCLUSTER SIZES:")
    for cluster_id, size in sorted(results['clustering']['cluster_sizes'].items()):
        print(f"  Cluster {cluster_id}: n = {size}")

print("\n" + "="*70)

# Save results to JSON for report generation
import json
with open("v4_analysis_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print("\nResults saved to v4_analysis_results.json")

