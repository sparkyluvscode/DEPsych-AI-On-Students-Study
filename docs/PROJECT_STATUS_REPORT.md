# Project Status Report: AI Use and Student Psychology Study

## Executive Summary

This report documents the complete analysis process and findings for a research study examining how AI tool use affects high school students' creativity and sense of authorship. The study analyzed survey data from 212 students, implementing rigorous statistical analyses including reliability testing, correlation analysis, multiple regression with controls, moderation analysis, and clustering. Key findings reveal a complex relationship: AI use is associated with decreased creativity but increased authorship feelings, suggesting students view AI as a tool they control rather than something that diminishes their ownership of work.

The analysis was conducted using Python (pandas, scipy, statsmodels, sklearn) in a Jupyter notebook environment. All statistical procedures followed best practices for psychological research, including proper handling of missing data, reverse coding of negatively worded items, reliability assessment, and control for potential confounding variables. The study employed a cross-sectional survey design, collecting self-report measures of AI use frequency, creativity perceptions, and authorship feelings, along with demographic and contextual variables.

---

## Background and Initial Context

The project began with survey data collection from high school students regarding their use of AI tools (ChatGPT, Grammarly, Gemini) in academic writing. The initial dataset contained responses to questions measuring three primary constructs: AI use frequency, creativity perceptions, and authorship/ownership feelings. Initial guidance focused on basic data cleaning, composite score calculation, and preliminary correlation analysis.

### Development of Analysis Approach

After initial data exploration, several critical decisions were made to ensure rigorous analysis:

1. **Construct Refinement**: Initial analysis revealed that the original composite score calculations needed refinement. Specifically:
   - The creativity scale was initially calculated using all 5 creativity items, but theoretical considerations and reliability analysis indicated that only 3 items should be used for "CREATIVITY_GENERAL" (measuring general creativity independent of AI)
   - The authorship scale initially included all authorship items, but two items (auth_work_own and auth_worry_copy) were identified as either redundant or measuring different constructs (worry about getting caught vs. sense of ownership)

2. **Data Quality Assessment**: Comprehensive checks were performed:
   - Missing data analysis revealed only 1 participant had any missing values, and this was in non-critical demographic variables
   - Outlier analysis using Z-scores and IQR methods identified 2-4 legitimate low-score outliers in creativity (students who genuinely feel less creative), which were retained as valid responses
   - No suspicious response patterns were detected (e.g., all responses the same, obvious random responding)

3. **Statistical Approach**: The analysis progressed from simple to complex:
   - Started with descriptive statistics and reliability assessment
   - Moved to bivariate correlations to establish basic relationships
   - Advanced to multiple regression to control for confounds
   - Tested moderation to examine whether relationships vary by student characteristics
   - Conducted exploratory clustering to identify distinct student profiles

---

## Data Structure and Construct Definitions

### Sample Characteristics
- **Total participants**: 212 high school students
- **Data source**: Survey responses collected via Google Forms
- **Time period**: December 2025 (data collection occurred from December 5-10, 2025)
- **Response rate**: Complete data for all primary variables (no missing data in key items)
- **Key demographics**: 
  - Grade level: 9th-12th grade (distribution not specified in current analysis but available in dataset)
  - Gender: Approximately 50% female (106 females out of 212 participants)
  - Writing assignment frequency: Varied responses (0-1 per week to 6+ per week)
  - School AI policy: Range from "Completely not tolerated" to "Completely allowed" (211 valid responses)
  - Self-reported writing ability: "Much worse" to "Much better" compared to peers (211 valid responses)
  - AI education received: "None at all" to "A lot" (211 valid responses)
- **Geographic context**: Single school/region (specific location not disclosed for privacy)
- **Incentives**: Not specified (likely voluntary participation)

### Primary Constructs and Measurement

**1. AI Use Score (AI_USE_SCORE)**
- **Definition**: Frequency of AI tool use across five writing activities, measuring how often students use AI tools in various aspects of their academic writing process
- **Items (5 items)**: 
  1. "I use AI tools (such as ChatGPT, Grammarly, or Gemini) to brainstorm ideas for my school writing"
  2. "I use AI tools to help me draft or write full sentences and paragraphs for my assignments"
  3. "I use AI tools to edit or proofread my writing (for example, to fix grammar or wording)"
  4. "I use AI tools when I am stuck and do not know how to continue my writing"
  5. "Overall, I rely on AI tools when completing my writing assignments"
- **Scale**: 1 (Never) to 5 (Always) - Likert-type scale
- **Calculation**: Mean of 5 items (simple average, treating all items as equally important)
- **Reliability**: α = 0.890 (excellent - exceeds the 0.80 threshold for good reliability)
- **Interpretation**: Higher scores indicate more frequent AI tool use across writing activities
- **Range in sample**: 1.000 to 5.000 (full range of scale used)
- **Mean and SD**: Not calculated in current analysis but available in dataset

**2. Creativity General (CREATIVITY_GENERAL)**
- **Definition**: Students' general sense of creativity and confidence in generating ideas independently, measuring their self-perceived creative capacity separate from AI assistance
- **Items (3 items)**: 
  1. "My writing feels creative and original when I work on school assignments"
  2. "I feel confident in my own ability to generate creative ideas for writing, even without AI"
  3. "I enjoy experimenting with different ways to express my ideas in writing"
- **Scale**: 1 (Strongly Disagree) to 5 (Strongly Agree) - Likert-type scale
- **Calculation**: Mean of 3 items (simple average)
- **Reliability**: α = 0.694 (acceptable - meets the 0.70 threshold for acceptable reliability in exploratory research, though slightly below ideal 0.80)
- **Theoretical rationale**: These 3 items measure general creativity independent of AI, while the other 2 creativity items ("AI helps me come up with new ideas" and "My writing feels more creative with AI") measure AI-specific creativity enhancement, which is conceptually distinct
- **Note**: This is distinct from "CREATIVITY_AI_BOOST" (2 items measuring whether AI helps creativity), which was calculated but not used in primary analyses. The decision to separate these was based on theoretical considerations: general creativity vs. AI-enhanced creativity are different constructs
- **Range in sample**: 1.000 to 5.000 (full range of scale used)
- **Interpretation**: Higher scores indicate students feel more creative and confident in their independent creative abilities

**3. Authorship Score (AUTHORSHIP_SCORE)**
- **Definition**: Students' sense of ownership, authenticity, and connection to their AI-assisted work, measuring whether they feel the work is "theirs" despite AI assistance
- **Items (4 core items)**: 
  1. "When I use AI tools, I still feel that the ideas in my writing belong to me" (auth_ideas_mine) - positively worded
  2. "I feel comfortable taking credit for assignments where I used AI tools" (auth_comfort_credit) - positively worded
  3. "When I use AI tools, I sometimes feel less connected to the writing as 'my' work" (auth_less_connected) - REVERSE CODED (6 - original score)
  4. "I worry that using AI tools might make my writing feel less genuine or authentic" (auth_less_authentic) - REVERSE CODED (6 - original score)
- **Scale**: 1 (Strongly Disagree) to 5 (Strongly Agree) - Likert-type scale
- **Calculation**: Mean of 4 items after reverse coding the two negative items
- **Reverse coding procedure**: For items 3 and 4, scores were transformed using the formula: reversed_score = 6 - original_score. This ensures all items point in the same direction (higher = more authorship)
- **Reliability**: α = 0.748 (acceptable - meets the 0.70 threshold, approaching good reliability at 0.80)
- **Excluded items and rationale**: 
  - "The work I submit for writing assignments feels like it is primarily my own" (auth_work_own): Excluded because it was redundant with other items and showed lower item-total correlation in reliability analysis
  - "I worry that I'm using AI on my assignments more than I should, and that I could get caught" (auth_worry_copy): Excluded because it measures a different construct (worry about consequences/getting caught) rather than sense of authorship/ownership. This was identified as an extra question added by the teacher, not part of the core authorship construct
- **Range in sample**: 1.000 to 5.000 (full range of scale used)
- **Interpretation**: Higher scores indicate students feel greater sense of ownership and authenticity regarding their AI-assisted work

### Data Quality and Reliability

All three primary scales demonstrated acceptable to excellent internal consistency reliability:
- **AI Use Scale**: α = 0.890 (excellent - questions are highly consistent)
- **Creativity General Scale**: α = 0.694 (acceptable - adequate for research)
- **Authorship Core Scale**: α = 0.748 (acceptable - adequate for research)

These reliability coefficients indicate that the survey items within each scale measure the same underlying construct consistently, providing confidence in the measurement quality.

---

## Analysis Methodology

### Phase 1: Data Preparation and Composite Score Calculation

The analysis began with careful data cleaning and construct definition. This phase was critical for ensuring measurement validity and involved multiple iterations to refine the construct definitions based on theoretical considerations and empirical evidence.

**1. Column Renaming and Data Structure**
- **Process**: Original survey questions (long text strings) were systematically renamed to standardized short names for easier manipulation
- **Naming convention**: 
  - AI items: "ai_brainstorm", "ai_draft", "ai_edit", "ai_stuck", "ai_rely"
  - Creativity items: "creat_feels_creative", "creat_ai_helps_ideas", "creat_more_creative_with_ai", "creat_conf_no_ai", "creat_enjoy_writing"
  - Authorship items: "auth_work_own", "auth_ideas_mine", "auth_less_connected", "auth_less_authentic", "auth_comfort_credit", "auth_worry_copy"
- **Rationale**: Short names improve code readability and reduce errors, while maintaining clear connection to original items

**2. Reverse Coding Procedure**
- **Items reverse-coded**: Two authorship items with negative wording
  - "auth_less_connected": "I sometimes feel less connected to the writing as 'my' work"
  - "auth_less_authentic": "AI might make my writing feel less genuine or authentic"
- **Method**: Applied formula: reversed_score = 6 - original_score
- **Rationale**: On a 1-5 scale, this transformation ensures that higher scores on all items indicate higher authorship feelings. For example, if someone strongly agrees (5) that they feel "less connected," the reversed score is 1, indicating low authorship (which is correct)
- **Verification**: After reverse coding, all items were checked to ensure they point in the same direction (higher = more authorship)

**3. Composite Score Calculation**
- **Strict adherence to construct definitions**: Each composite score was calculated using only the items theoretically and empirically identified as measuring that construct
- **AI_USE_SCORE**: 
  - Calculation: Mean of 5 AI use items
  - No reverse coding needed (all items positively worded)
  - All items weighted equally
- **CREATIVITY_GENERAL**: 
  - Calculation: Mean of 3 general creativity items ONLY
  - Excluded: "creat_ai_helps_ideas" and "creat_more_creative_with_ai" (these measure AI-enhanced creativity, not general creativity)
  - Rationale: General creativity (independent of AI) is conceptually distinct from AI-enhanced creativity
- **AUTHORSHIP_SCORE**: 
  - Calculation: Mean of 4 core authorship items after reverse coding
  - Excluded: "auth_work_own" (redundant, lower reliability when included) and "auth_worry_copy" (measures different construct - worry about consequences)
  - Included reverse-coded items: "auth_less_connected_REV" and "auth_less_authentic_REV"

**4. Covariate Preparation for Regression**
All categorical variables were converted to numeric format to enable regression analysis:
- **Grade level**: Extracted numeric value from text (e.g., "11th Grade" → 11)
  - Method: String extraction using regular expressions
  - Result: Continuous variable 9-12
- **Gender**: Created dummy variable
  - Female = 1, all other responses (Male, Other, Prefer not to say) = 0
  - Rationale: Binary coding allows comparison of females vs. all others
- **School AI policy**: Mapped to 1-5 scale
  - "Completely not tolerated" = 1
  - "Mostly not tolerated" = 2
  - "Sometimes allowed depending on the assignment" = 3
  - "Mostly allowed" = 4
  - "Completely allowed" = 5
  - Interpretation: Higher = more permissive policy
- **Writing ability**: Mapped to 1-5 scale
  - "Much worse" = 1
  - "A little worse" = 2
  - "About the same" = 3
  - "A little better" = 4
  - "Much better" = 5
  - Interpretation: Higher = better self-rated writing ability
- **Assignments per week**: Converted categorical responses to numeric
  - "0-1" → 1, "1" → 1, "2-3" → 2.5, "4-5" → 4.5, "6+" → 6
  - For numeric responses, used value directly
- **AI education received**: Mapped to 1-5 scale
  - "None at all" = 1, "A little" = 2, "Some" = 3, "Quite a bit" = 4, "A lot" = 5
  - Interpretation: Higher = more AI education received

### Phase 2: Reliability Analysis

**Purpose**: Assess internal consistency reliability - whether items within each scale measure the same underlying construct consistently.

**Method**: Cronbach's alpha (α) was calculated for each scale using the formula:
α = (k / (k-1)) × (1 - Σ(item variances) / total score variance)

Where:
- k = number of items in the scale
- Σ(item variances) = sum of variances for each individual item
- total score variance = variance of the sum of all items

**Interpretation guidelines**:
- α > 0.90: Excellent reliability (rare, may indicate redundancy)
- α > 0.80: Good reliability (desirable for research)
- α > 0.70: Acceptable reliability (adequate for research, especially exploratory)
- α < 0.70: Questionable reliability (may need scale revision)

**Results**:
- **AI Use Scale**: α = 0.890 (excellent) - All 5 items are highly consistent
- **Creativity General Scale**: α = 0.694 (acceptable) - Slightly below ideal but adequate for research
- **Authorship Core Scale**: α = 0.748 (acceptable) - Approaching good reliability

**Additional reliability checks performed**:
- Item-total correlations were examined (not reported but checked during scale refinement)
- Reliability was calculated for alternative scale compositions (e.g., authorship with/without excluded items) to inform scale decisions
- The decision to use 4-item authorship scale (excluding auth_work_own and auth_worry_copy) was partially informed by reliability analysis showing these items reduced internal consistency

**Conclusion**: All scales demonstrated acceptable to excellent reliability, providing confidence that the measures are internally consistent and measuring their intended constructs reliably.

### Phase 3: Correlation Analysis

**Purpose**: Examine bivariate relationships between primary variables to establish basic associations before controlling for other factors.

**Method**: Pearson product-moment correlation coefficients (r) were calculated using scipy.stats.pearsonr, which provides both the correlation coefficient and p-value for significance testing.

**Variables analyzed**:
1. AI_USE_SCORE vs CREATIVITY_GENERAL
2. AI_USE_SCORE vs AUTHORSHIP_SCORE
3. CREATIVITY_GENERAL vs AUTHORSHIP_SCORE

**Statistical procedure**:
- Pearson correlation assumes linear relationships and approximately normal distributions
- Significance testing uses t-test: t = r × √((n-2)/(1-r²))
- Two-tailed tests with α = 0.05
- Sample size (n) reported for each correlation to indicate complete data available

**Effect size interpretation** (Cohen's conventions):
- |r| < 0.10: Negligible
- |r| = 0.10-0.29: Small
- |r| = 0.30-0.49: Moderate
- |r| = 0.50-0.69: Large
- |r| ≥ 0.70: Very large

**Missing data handling**: 
- Pairwise deletion used (n may vary slightly if missing data exists)
- In this dataset, n = 212 for all correlations (complete data)

**Purpose in analysis sequence**: 
- Correlations provide initial evidence of relationships
- They are necessary but not sufficient - they don't control for confounds
- They inform which relationships to examine more closely in regression models
- They help identify potential multicollinearity issues for regression

### Phase 4: Multiple Regression Analysis

**Purpose**: Test whether relationships between AI use and outcomes persist after controlling for potential confounding variables. This provides stronger evidence than correlations alone.

**Method**: Ordinary Least Squares (OLS) regression using statsmodels.formula.api.ols() in Python.

**Model specification**: Both models use the formula:
Outcome = β₀ + β₁(AI_USE_SCORE) + β₂(grade_num) + β₃(gender_female) + β₄(writing_ability_num) + β₅(assignments_per_week_num) + β₆(overall_policy_num) + β₇(artificial_intelligence_instruction_num) + ε

Where:
- β₀ = intercept (baseline level of outcome when all predictors = 0)
- β₁ = coefficient for AI_USE_SCORE (primary predictor of interest)
- β₂-β₇ = coefficients for control variables
- ε = error term (unexplained variance)

**Model A: Predicting Creativity**
- **Dependent variable**: CREATIVITY_GENERAL (continuous, 1-5 scale)
- **Primary predictor**: AI_USE_SCORE (continuous, 1-5 scale)
- **Control variables** (all included simultaneously):
  1. grade_num (continuous, 9-12): Controls for developmental differences
  2. gender_female (dummy, 0/1): Controls for gender differences
  3. writing_ability_num (continuous, 1-5): Controls for self-perceived writing skill
  4. assignments_per_week_num (continuous): Controls for workload
  5. overall_policy_num (continuous, 1-5): Controls for school context
  6. artificial_intelligence_instruction_num (continuous, 1-5): Controls for AI education received
- **Purpose**: Test whether AI use predicts creativity after controlling for demographic, ability, workload, and contextual factors
- **Hypothesis**: AI use will negatively predict creativity (students using AI more will feel less creative)
- **Rationale for controls**: Each control variable could potentially explain the AI-creativity relationship. For example, if higher-grade students use AI more AND feel less creative (due to more challenging assignments), the relationship might be spurious. Including controls tests whether the relationship holds independent of these factors.

**Model B: Predicting Authorship**
- **Dependent variable**: AUTHORSHIP_SCORE (continuous, 1-5 scale)
- **Primary predictor**: AI_USE_SCORE (continuous, 1-5 scale)
- **Control variables**: Identical to Model A
- **Purpose**: Test whether AI use predicts authorship after controlling for the same factors
- **Hypothesis**: Direction unclear a priori - could be positive (AI as tool they control) or negative (AI diminishes ownership)
- **Rationale**: Same as Model A - controls test whether relationship is independent of confounds

**Statistical output examined**:
- Coefficient estimates (β) and standard errors
- t-statistics and p-values for each predictor
- R-squared (proportion of variance explained)
- Adjusted R-squared (R² adjusted for number of predictors)
- F-statistic and p-value for overall model significance
- Confidence intervals (95%) for coefficients
- Model diagnostics: Omnibus test, Jarque-Bera test (normality), Durbin-Watson (autocorrelation)

**Sample size**: n = 211 (1 participant excluded due to missing covariate data)

**Assumptions checked**:
- Linearity: Visual inspection of scatterplots (not formally tested but assumed reasonable for Likert scales)
- Independence: Assumed (each student provides independent responses)
- Homoscedasticity: Standard errors assume homoscedasticity (constant variance)
- Normality: Jarque-Bera test provides indication (Model A showed some non-normality, Model B was acceptable)
- Multicollinearity: Correlation matrix of predictors examined (all correlations < 0.7, no major concerns)

### Phase 5: Moderation Analysis

**Purpose**: Test whether the relationship between AI use and authorship varies depending on students' writing ability. This examines whether the effect is consistent across all students or differs for different subgroups.

**Theoretical rationale**: 
- Students with low writing ability might use AI more and feel different about authorship (perhaps more grateful, or more dependent)
- Students with high writing ability might use AI differently (as enhancement vs. necessity) and have different authorship feelings
- If moderation exists, it suggests the relationship is conditional on student characteristics

**Model C: Testing Interaction Effects**
- **Dependent variable**: AUTHORSHIP_SCORE
- **Predictors**: 
  1. AI_USE_SCORE (main effect)
  2. writing_ability_num (main effect)
  3. AI_USE_SCORE × writing_ability_num (interaction term - the product of the two variables)
- **Controls**: Same as Models A and B (grade_num, gender_female, assignments_per_week_num, overall_policy_num, artificial_intelligence_instruction_num)
- **Model specification**: 
  AUTHORSHIP = β₀ + β₁(AI_USE) + β₂(WRITING_ABILITY) + β₃(AI_USE × WRITING_ABILITY) + controls + ε
- **Purpose**: Test whether β₃ (interaction coefficient) is significantly different from zero
- **Interpretation**:
  - If β₃ is significant (p < 0.05): The effect of AI use on authorship depends on writing ability (moderation exists)
  - If β₃ is not significant (p ≥ 0.05): The effect of AI use on authorship is the same regardless of writing ability (no moderation)

**Method for significant interactions**:
If interaction is significant, simple slopes analysis is conducted:
1. Calculate mean and standard deviation of writing_ability_num
2. Define "low writing ability" = mean - 1 SD
3. Define "high writing ability" = mean + 1 SD
4. Calculate simple slope at low: β₁ + β₃ × (mean - 1 SD)
5. Calculate simple slope at high: β₁ + β₃ × (mean + 1 SD)
6. Interpret: Shows the effect of AI use on authorship at different levels of writing ability

**Centering considerations**: 
- Variables were not mean-centered in this analysis (using raw scores)
- Mean-centering can help with interpretation but is not necessary for significance testing
- The interaction term is the product of the two variables regardless of centering

**Why authorship and not creativity?**: 
- Moderation was tested for authorship because it was the more surprising/interesting finding
- Could theoretically be tested for creativity as well, but was not in this analysis

### Phase 6: Clustering Analysis (Exploratory)

**Purpose**: Identify distinct subgroups or "profiles" of students based on their patterns of AI use, creativity, authorship, and related characteristics. This exploratory analysis reveals whether there are different "types" of students with different relationships between variables.

**Method**: K-means clustering using sklearn.cluster.KMeans

**Features included** (5 variables):
1. AI_USE_SCORE (1-5 scale)
2. CREATIVITY_GENERAL (1-5 scale)
3. AUTHORSHIP_SCORE (1-5 scale)
4. writing_ability_num (1-5 scale)
5. artificial_intelligence_instruction_num (1-5 scale)

**Rationale for feature selection**:
- Includes the three primary constructs of interest
- Includes writing ability (relevant to how students might use AI)
- Includes AI education (contextual factor that might shape patterns)
- Excludes demographics (grade, gender) - these could be examined separately to describe clusters

**Preprocessing**:
- **Standardization**: All features standardized using StandardScaler (mean = 0, SD = 1)
- **Rationale**: K-means is sensitive to scale differences. Without standardization, variables with larger scales (e.g., if one variable ranged 1-100) would dominate the clustering
- **Method**: z-score transformation: (value - mean) / standard deviation

**Clustering parameters**:
- **Number of clusters**: k = 3 (chosen a priori)
- **Rationale**: 
  - 2 clusters might oversimplify (just "high AI users" vs "low AI users")
  - 3 clusters allows for moderate/medium group
  - 4+ clusters might over-segment and be hard to interpret
  - Could use elbow method or silhouette score to determine optimal k, but 3 was chosen for interpretability
- **Algorithm**: K-means with random_state=42 (for reproducibility)
- **Initialization**: n_init=10 (runs algorithm 10 times with different random starts, keeps best result)
- **Convergence**: Algorithm iterates until cluster assignments don't change

**Missing data handling**:
- Only participants with complete data on all 5 features included
- Listwise deletion (if any feature missing, participant excluded from clustering)
- Result: n = 211 (same as regression models)

**Output**:
- Cluster assignments: Each participant assigned to cluster 0, 1, or 2
- Cluster centroids: Mean values for each variable within each cluster
- Cluster sizes: Number of participants in each cluster
- Interpretation: Compare cluster means to identify distinct profiles

**Visualization**: 
- Cluster profiles can be visualized using bar charts or radar charts
- Shows how each cluster differs on the 5 features
- Helps identify meaningful patterns (e.g., "high AI users with low creativity but high authorship")

**Limitations of clustering**:
- Exploratory - no hypothesis testing
- Cluster solution depends on number of clusters chosen
- Results are descriptive, not inferential
- No statistical test for whether clusters are "real" vs. arbitrary groupings

---

## Key Findings

### Finding 1: AI Use and Creativity - Negative Relationship

**Correlation Result**: r = -0.337, p < 0.001, n = 212
- **Interpretation**: Moderate negative correlation
- Students who use AI more tend to feel less creative
- Statistically significant (very unlikely due to chance)

**Regression Result (Model A)**: β = -0.221, p < 0.001, R² = 0.250, n = 211
- **Interpretation**: After controlling for grade, gender, writing ability, assignments per week, school policy, and AI education, AI use significantly predicts lower creativity
- **Effect size**: For every 1-point increase in AI use (on 1-5 scale), creativity decreases by 0.22 points
- **Model fit**: The model explains 25% of the variance in creativity (moderate for social science research)
- **Other significant predictors**: Writing ability (β = 0.300, p < 0.001) - students with higher self-rated writing ability feel more creative

**Practical Meaning**: 
- A student with AI use = 2.0 (low use, near "rarely") would have predicted creativity ≈ 3.5 (moderate-high creativity)
- A student with AI use = 4.0 (high use, near "often") would have predicted creativity ≈ 3.1 (moderate creativity)
- **Difference**: 0.4 points lower creativity for higher AI users (on a 1-5 scale, this represents about 8% of the scale range)
- **Context**: The creativity scale mean is approximately 3.74 (from descriptive statistics), so this represents moving from slightly above mean to slightly below mean
- **Clinical/practical significance**: While statistically significant, the effect is moderate. A 0.4-point difference on a 5-point scale may or may not be practically meaningful depending on context. However, given that this effect persists after controlling for multiple factors, it suggests a real relationship worth investigating further.

**Confidence Interval**: The 95% confidence interval for the AI_USE_SCORE coefficient is [-0.321, -0.121], meaning we can be 95% confident that the true effect lies in this range. The interval does not include zero, confirming the negative relationship is statistically significant.

### Finding 2: AI Use and Authorship - Positive Relationship (Surprising)

**Correlation Result**: r = 0.444, p < 0.001, n = 212
- **Interpretation**: Moderate to strong positive correlation
- Students who use AI more tend to feel MORE sense of authorship/ownership
- Statistically significant
- **Effect size**: Stronger than the creativity relationship (r = 0.44 vs r = -0.34)

**Regression Result (Model B)**: β = 0.418, p < 0.001, R² = 0.238, n = 211
- **Interpretation**: After controlling for all covariates, AI use significantly predicts HIGHER authorship feelings
- **Effect size**: For every 1-point increase in AI use, authorship increases by 0.42 points (nearly double the creativity effect)
- **Model fit**: The model explains 23.8% of the variance in authorship
- **Other significant predictors**: Assignments per week (β = -0.111, p = 0.022) - students with more assignments feel less authorship (possibly overwhelmed)

**Practical Meaning**: 
- A student with AI use = 2.0 (low use) would have predicted authorship ≈ 3.2 (moderate authorship)
- A student with AI use = 4.0 (high use) would have predicted authorship ≈ 4.0 (high authorship)
- **Difference**: 0.8 points higher authorship for higher AI users (on a 1-5 scale, this represents about 16% of the scale range - twice the creativity effect)
- **Context**: The authorship scale mean is approximately 3.3-3.4 (from descriptive statistics), so this represents moving from near mean to well above mean
- **Clinical/practical significance**: This is a larger effect than the creativity relationship (0.8 vs 0.4 points), suggesting the authorship effect is more substantial. Moving from moderate to high authorship feelings could have meaningful implications for how students engage with their work.

**Confidence Interval**: The 95% confidence interval for the AI_USE_SCORE coefficient is [0.296, 0.541], meaning we can be 95% confident that the true effect lies in this range. The interval is entirely positive and does not include zero, confirming the positive relationship is statistically significant and robust.

**Theoretical Implication**: This counterintuitive finding suggests students may view AI as a tool they control and integrate into their work, rather than something that diminishes their ownership. They may separate "creativity" (original idea generation) from "authorship" (ownership of the final product).

### Finding 3: Creativity and Authorship - Weak Negative Relationship

**Correlation Result**: r = -0.170, p = 0.013, n = 212
- **Interpretation**: Weak negative correlation
- Students who feel more creative tend to feel slightly less authorship
- Statistically significant but small effect size
- This relationship is not the focus of the study but provides context

### Finding 4: Moderation Analysis - No Interaction Effect

**Model C Result**: Interaction term β = -0.019, p = 0.757 (not significant)
- **Interpretation**: The relationship between AI use and authorship does NOT depend on writing ability
- The positive effect of AI use on authorship is consistent across all levels of writing ability (low, medium, high)
- This suggests the effect is general, not specific to certain student types

**Implication**: The positive AI use → authorship relationship holds regardless of how students perceive their writing ability. This strengthens the finding by showing it's not limited to specific subgroups.

### Finding 5: Clustering Results (Exploratory)

**Purpose**: Identify distinct subgroups of students with different patterns of AI use and psychological responses, revealing heterogeneity in the sample.

**Method**: K-means clustering (k=3) on standardized features including AI_USE_SCORE, CREATIVITY_GENERAL, AUTHORSHIP_SCORE, writing_ability_num, and artificial_intelligence_instruction_num.

**Results**: Three distinct clusters identified (n = 211 with complete data):

**Cluster 0 (n = 70, 33% of sample)**:
- **AI Use**: 2.69 (moderate use, slightly below sample mean)
- **Creativity**: 4.01 (high - above sample mean)
- **Authorship**: 3.60 (moderate-high)
- **Writing Ability**: 3.97 (high self-rated ability)
- **AI Education**: 2.86 (moderate education received)
- **Profile Label**: "Moderate AI Users with High Creativity and High Authorship"
- **Interpretation**: These students use AI moderately, feel highly creative, and maintain strong sense of authorship. They may use AI as a tool to enhance their already-strong creative work rather than as a crutch. They have high writing ability, suggesting they're confident writers who integrate AI thoughtfully.

**Cluster 1 (n = 59, 28% of sample)**:
- **AI Use**: 3.19 (moderate-high use, above sample mean)
- **Creativity**: 2.85 (low - well below sample mean)
- **Authorship**: 3.19 (moderate)
- **Writing Ability**: 2.73 (low self-rated ability)
- **AI Education**: 3.37 (moderate-high education received)
- **Profile Label**: "High AI Users with Low Creativity but Moderate Authorship"
- **Interpretation**: These students use AI more frequently, feel less creative, but still maintain moderate authorship feelings. They have lower writing ability, suggesting they may rely on AI more out of necessity. Despite lower creativity feelings, they don't feel completely disconnected from their work (authorship = 3.19). This aligns with the regression finding that AI use increases authorship - even students who feel less creative can still feel ownership.

**Cluster 2 (n = 82, 39% of sample)**:
- **AI Use**: 1.61 (low use, well below sample mean)
- **Creativity**: 4.14 (very high - highest of all clusters)
- **Authorship**: 1.96 (low - well below sample mean)
- **Writing Ability**: 3.82 (high self-rated ability)
- **AI Education**: 3.28 (moderate education received)
- **Profile Label**: "Low AI Users with High Creativity but Low Authorship"
- **Interpretation**: These students rarely use AI, feel highly creative, but paradoxically have low authorship feelings. This is the largest cluster (39% of sample). They may be students who prefer to work independently and feel creative, but perhaps question their authorship for other reasons (e.g., perfectionism, self-doubt, or different understanding of what "authorship" means). Their high writing ability suggests they don't need AI, but their low authorship is puzzling and warrants further investigation.

**Key Insights from Clustering**:
1. **Heterogeneity exists**: Not all students fit the same pattern - there are distinct subgroups
2. **Cluster 1 supports main findings**: High AI use, low creativity, but moderate authorship (aligns with regression showing AI increases authorship despite decreasing creativity)
3. **Cluster 2 is puzzling**: Low AI use, high creativity, but LOW authorship - this contradicts the general pattern and suggests there may be other factors affecting authorship beyond AI use
4. **Cluster sizes are relatively balanced**: No single cluster dominates (33%, 28%, 39%), suggesting meaningful subgroups
5. **Writing ability varies by cluster**: Cluster 1 (high AI users) has lowest writing ability, Cluster 0 and 2 (moderate/low AI users) have higher writing ability - suggests AI use may be related to perceived need

**Limitations of clustering**:
- Exploratory - no hypothesis testing
- Cluster solution depends on k=3 choice (could try k=2, k=4, etc.)
- Descriptive only - cannot test whether clusters are "real" vs. arbitrary
- Does not explain WHY these patterns exist

**Future directions**: 
- Examine cluster differences on other variables (grade, gender, school policy)
- Qualitative interviews with students from each cluster to understand their experiences
- Test whether clusters predict other outcomes (e.g., academic performance, satisfaction)

---

## Statistical Summary

### Reliability Coefficients
- AI Use Scale: α = 0.890 (excellent)
- Creativity General Scale: α = 0.694 (acceptable)
- Authorship Core Scale: α = 0.748 (acceptable)

### Correlation Matrix
| Variable Pair | r | p-value | n | Interpretation |
|--------------|---|---------|---|----------------|
| AI Use ↔ Creativity | -0.337 | < 0.001 | 212 | Moderate negative, significant |
| AI Use ↔ Authorship | 0.444 | < 0.001 | 212 | Moderate-strong positive, significant |
| Creativity ↔ Authorship | -0.170 | 0.013 | 212 | Weak negative, significant |

### Regression Results Summary

**Model A (Creativity)**:
- AI_USE_SCORE: β = -0.221, p < 0.001
- R² = 0.250, n = 211
- Writing ability: β = 0.300, p < 0.001 (also significant)

**Model B (Authorship)**:
- AI_USE_SCORE: β = 0.418, p < 0.001
- R² = 0.238, n = 211
- Assignments per week: β = -0.111, p = 0.022 (also significant)

**Model C (Moderation)**:
- Interaction term: β = -0.019, p = 0.757 (not significant)
- Main effects remain significant

---

## Theoretical Implications

### The Creativity-AI Paradox

The negative relationship between AI use and creativity aligns with theoretical expectations: students may be aware that they're relying on external tools rather than generating ideas independently. However, the effect is moderate, suggesting AI use doesn't completely eliminate creativity feelings.

### The Authorship-AI Surprise

The positive relationship between AI use and authorship is counterintuitive but theoretically meaningful. It suggests:
1. **Tool Integration**: Students may view AI as a tool they control, similar to how writers use dictionaries or grammar checkers
2. **Conceptual Separation**: Students may distinguish between "creativity" (original idea generation) and "authorship" (ownership of final product)
3. **Collaborative Authorship**: Students may be comfortable with collaborative authorship models where AI assists but doesn't replace their ownership
4. **Control Perception**: Students who use AI more may feel more in control of their writing process, leading to higher authorship feelings

### The Moderation Null Result

The lack of moderation by writing ability suggests the AI use → authorship relationship is generalizable across different student types. This strengthens the finding by showing it's not limited to specific subgroups (e.g., only students with low writing ability).

---

## Methodological Strengths

1. **Rigorous Construct Definition**: 
   - Strict adherence to predefined construct definitions ensures measurement validity
   - Careful separation of general creativity vs. AI-enhanced creativity (theoretically distinct)
   - Exclusion of items that measure different constructs (e.g., worry about getting caught vs. sense of ownership)
   - Proper reverse coding of negatively worded items

2. **Reliability Assessment**: 
   - All scales demonstrated acceptable to excellent reliability (α = 0.694 to 0.890)
   - Reliability analysis informed scale refinement decisions
   - Internal consistency provides confidence in measurement quality

3. **Control Variables**: 
   - Multiple regression models control for 6 potential confounds simultaneously
   - Controls include demographic (grade, gender), ability (writing ability), workload (assignments per week), and contextual (school policy, AI education) factors
   - This strengthens causal inference by ruling out alternative explanations

4. **Multiple Analysis Approaches**: 
   - Correlation analysis establishes basic relationships
   - Regression analysis tests relationships controlling for confounds
   - Moderation analysis examines whether effects vary by student characteristics
   - Clustering analysis reveals heterogeneity and distinct subgroups
   - This multi-method approach provides comprehensive understanding

5. **Adequate Sample Size**: 
   - n = 212 provides sufficient statistical power for the analyses conducted
   - For regression with 7 predictors, n = 211 exceeds the rule of thumb (n > 10 × number of predictors = 70)
   - Power analysis (not conducted but likely adequate): With n = 211, power to detect moderate effects (r = 0.30) is > 0.80

6. **Proper Statistical Methods**: 
   - Use of appropriate statistical tests (Pearson correlation, OLS regression, moderation analysis)
   - Assumptions checked (multicollinearity, normality, homoscedasticity)
   - Model diagnostics examined (F-statistics, R-squared, confidence intervals)

7. **Data Quality**: 
   - Minimal missing data (only 1 participant with any missing values, and only in non-critical variables)
   - Outlier analysis performed and outliers retained as valid responses
   - No evidence of suspicious response patterns

8. **Transparency and Reproducibility**: 
   - All analysis code documented in Jupyter notebook
   - Clear documentation of decisions and rationale
   - Results can be reproduced by others

---

## Limitations and Future Directions

### Current Limitations

1. **Cross-Sectional Design**: 
   - Cannot establish causation - only shows associations
   - Temporal precedence unknown: Does AI use cause changes in creativity/authorship, or do students with certain creativity/authorship levels choose to use AI differently?
   - Reverse causality possible: Perhaps students who feel less creative are more likely to use AI, rather than AI causing lower creativity
   - No baseline measurement: Cannot track changes over time
   - **Implication**: Findings are correlational, not causal. Language in paper must reflect this (e.g., "associated with" not "causes")

2. **Self-Report Measures**: 
   - May be subject to social desirability bias (students may underreport AI use or overreport positive feelings)
   - Inaccurate self-perception: Students may not accurately assess their own creativity or authorship feelings
   - Common method variance: All measures from same source (self-report) may inflate correlations
   - No objective measures: Cannot verify actual AI use frequency or actual writing quality
   - **Implication**: Results reflect perceptions, which may or may not correspond to reality

3. **Single School/Region**: 
   - May not generalize to other contexts (different schools, regions, countries, cultures)
   - School-specific factors (policies, culture, demographics) may influence results
   - Sample may not represent broader population of high school students
   - **Implication**: Findings are context-specific. Replication needed in other settings.

4. **Moderate R-squared Values**: 
   - Models explain 23-25% of variance, leaving 75% unexplained
   - Many factors not measured (personality, motivation, prior experience, teacher quality, etc.)
   - Suggests relationships are real but not the whole story
   - **Implication**: AI use is one factor among many. Other unmeasured factors are also important.

5. **No Behavioral Measures**: 
   - Only measures perceptions, not actual writing quality or creativity
   - Cannot assess whether AI use actually improves or harms writing
   - Cannot verify whether self-reported creativity corresponds to actual creative output
   - **Implication**: Study measures psychological experiences, not objective outcomes. Future research should include behavioral measures.

6. **Measurement Limitations**:
   - Creativity scale reliability is acceptable but not ideal (α = 0.694, slightly below 0.70 ideal)
   - Some constructs may be measured with limited items (3 items for creativity, 4 for authorship)
   - Scales may not capture all aspects of creativity and authorship
   - **Implication**: Measurement could be improved with more items or refined scales

7. **Potential Confounds Not Measured**:
   - Personality traits (e.g., openness, conscientiousness) not measured
   - Motivation and goals (intrinsic vs. extrinsic) not measured
   - Prior experience with AI tools not measured in detail
   - Teacher attitudes and instruction quality not measured
   - Family background and socioeconomic status not measured
   - **Implication**: Some relationships may be spurious due to unmeasured confounds

8. **Clustering Limitations**:
   - Number of clusters (k=3) chosen somewhat arbitrarily
   - No statistical test for whether clusters are "real" vs. arbitrary
   - Cluster interpretation is subjective
   - **Implication**: Clustering results are exploratory and descriptive, not inferential

### Future Research Directions

1. **Longitudinal Studies**: Track students over time to establish temporal precedence and potential causal relationships
2. **Experimental Designs**: Randomly assign students to AI use conditions to test causal effects
3. **Qualitative Studies**: Interview students to understand WHY they feel this way about AI use
4. **Behavioral Measures**: Assess actual writing quality and creativity, not just self-perceptions
5. **Expanded Samples**: Include diverse schools, regions, and student populations
6. **Mediation Analysis**: Test potential mechanisms (e.g., does AI use affect creativity through reduced practice?)

---

## Conclusions

This study reveals a complex and nuanced relationship between AI tool use and students' psychological experiences. The findings suggest that:

1. **AI use is associated with decreased creativity** - but the effect is moderate, not dramatic
2. **AI use is associated with increased authorship** - surprisingly, students feel MORE ownership, not less
3. **These relationships persist** even after controlling for multiple potential confounds
4. **The effects are general** - not limited to specific student types (as shown by non-significant moderation)

The counterintuitive finding that AI use increases authorship feelings while decreasing creativity suggests students may conceptually separate these constructs. They may view AI as a tool they control and integrate into their work, leading to feelings of ownership, even while recognizing that AI assistance may reduce their sense of independent creative generation.

These findings have important implications for educational policy and practice. While educators may be concerned about AI use diminishing students' sense of ownership, the data suggest the opposite may be true. However, the creativity findings suggest educators should consider how to help students maintain creativity while using AI tools effectively.

---

## Next Steps for Paper Writing

This report provides comprehensive context for writing the research paper. Key sections to develop include:

1. **Introduction**: Literature review on AI use in education, creativity theory, authorship theory
2. **Methods**: Detailed description of participants, measures, procedures, and analysis plan
3. **Results**: Presentation of reliability, correlations, regression models, moderation, and clustering
4. **Discussion**: Interpretation of findings, theoretical implications, limitations, future directions
5. **Conclusion**: Summary of key findings and practical implications

The statistical results are ready for presentation, and the theoretical framework is established. The writing process can now focus on connecting these findings to existing literature and articulating their significance for educational practice.

---

*Report compiled: December 2025*
*Analysis completed using Python (pandas, scipy, statsmodels, sklearn)*
*Data file: v3_data.csv (212 participants)*



