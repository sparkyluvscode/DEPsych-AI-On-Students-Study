# Code Analysis Report: AI Impact on Students' Study Analysis

## Executive Summary

This code analyzes survey data from students about how they use AI tools (like ChatGPT, Grammarly, Gemini) for their school writing assignments. The analysis examines three main areas: **AI usage patterns**, **creativity**, and **authorship/authenticity** feelings. The code processes responses from 212 students and performs statistical reliability tests and correlation analyses.

---

## What This Project Does (In Simple Terms)

Imagine you're a researcher studying how high school students use AI tools for their homework. You've collected survey responses from 212 students asking them questions like:
- How often do you use AI for brainstorming?
- Do you feel creative when writing?
- Do you feel like the work is "yours" when you use AI?

This code takes all those survey responses and:
1. **Cleans up the data** - Makes column names easier to work with
2. **Groups questions** - Organizes them into meaningful categories
3. **Calculates scores** - Creates overall scores for AI usage, creativity, and authorship
4. **Checks reliability** - Makes sure the questions in each category measure the same thing
5. **Finds relationships** - Looks for connections between AI usage, creativity, and authorship feelings

---

## File Structure

### Main Files:
- **`v1_analysis_notebook.ipynb`** - The main analysis notebook (this is what you're looking at)
- **`v3_data.csv`** - The survey data with 212 student responses
- **`v1_analysis.py`** - A simple Python script (appears incomplete, just loads data)

### Data Files:
- **`v1_data.csv`**, **`v2_data.csv`**, **`v3_data.csv`** - Different versions of the survey data (v3 is the one being used)

---

## Step-by-Step Breakdown of What the Code Does

### Step 1: Loading Libraries and Data
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("v3_data.csv", index_col=0)
```

**What this means:**
- Imports tools for data analysis (pandas), plotting (matplotlib), and math (numpy)
- Loads the survey data from a CSV file
- Uses the first column (Timestamp) as the row identifier

**Result:** You now have a table with 212 rows (students) and 28 columns (questions/answers)

---

### Step 2: Renaming Columns

**What this does:**
The original survey questions are very long, like:
- "I use AI tools (such as ChatGPT, Grammarly, or Gemini) to brainstorm ideas for my school writing."

The code renames them to shorter names like:
- `ai_brainstorm`

**Why?** Makes the code easier to read and write. Instead of typing the entire question, you can just use `ai_brainstorm`.

**Example mapping:**
- `"What is your age?"` → `"age"`
- `"I use AI tools to help me draft..."` → `"ai_draft"`
- `"My writing feels creative and original..."` → `"creat_feels_creative"`

---

### Step 3: Organizing Questions into Categories

The code groups all 28 questions into **3 main categories**:

#### Category 1: AI Usage (`ai_items`)
Questions about HOW students use AI:
- `ai_brainstorm` - Using AI to brainstorm ideas
- `ai_draft` - Using AI to write full sentences/paragraphs
- `ai_edit` - Using AI to edit/proofread
- `ai_stuck` - Using AI when stuck
- `ai_rely` - Overall reliance on AI

#### Category 2: Creativity (`creativity_items`)
Questions about CREATIVITY:
- `creat_feels_creative` - Feeling creative when writing
- `creat_ai_helps_ideas` - AI helps come up with ideas
- `creat_more_creative_with_ai` - More creative with AI than without
- `creat_conf_no_ai` - Confident generating ideas without AI
- `creat_enjoy_writing` - Enjoying experimenting with writing

#### Category 3: Authorship/Authenticity (`authorship_items`)
Questions about OWNERSHIP and AUTHENTICITY:
- `auth_work_own` - Work feels like it's primarily my own
- `auth_ideas_mine` - Ideas still feel like mine when using AI
- `auth_less_connected` - Sometimes feel less connected to work
- `auth_less_authentic` - Worry writing feels less genuine
- `auth_comfort_credit` - Comfortable taking credit for AI-assisted work

---

### Step 4: Creating Composite Scores

**What is a composite score?**
Instead of looking at 5 separate AI usage questions, the code creates ONE overall "AI Usage Score" by averaging all 5 answers.

**The code creates:**
1. **`AI_USE_SCORE`** - Average of all 5 AI usage questions
2. **`CREATIVITY_SCORE`** - Average of all 5 creativity questions
3. **`AUTHORSHIP_SCORE`** - Average of authorship questions (with some reversed)

**Why reverse some items?**
Some questions are worded negatively (e.g., "I feel less connected"). To make all questions point in the same direction, the code reverses them. So "I feel less connected" (high score = bad) becomes "I feel MORE connected" (high score = good).

**Sub-scores created:**
- **`CREATIVITY_GENERAL`** - General creativity (without AI-specific questions)
- **`CREATIVITY_AI_BOOST`** - How much AI boosts creativity
- **`AUTHORSHIP_SCORE`** - Core authorship items (after reliability testing)

---

### Step 5: Reliability Testing (Cronbach's Alpha)

**What is Cronbach's Alpha?**
This is a statistical test that checks if questions in a category are measuring the same thing. Think of it like checking if all the questions on a test are actually testing the same skill.

**The formula:**
```python
def cronbach_alpha(df_subset):
    items = df_subset.to_numpy(dtype=float)
    item_vars = items.var(axis=0, ddof=1)  # Variance of each question
    total_scores = items.sum(axis=1)        # Sum of all questions per student
    total_var = total_scores.var(ddof=1)    # Variance of total scores
    k = items.shape[1]                      # Number of questions
    return (k / (k-1)) * (1 - item_vars.sum() / total_var)
```

**What the scores mean:**
- **0.7 - 0.8**: Acceptable reliability
- **0.8 - 0.9**: Good reliability
- **> 0.9**: Excellent reliability

**Results from your data:**
- **AI Usage**: α = 0.89 (Excellent - all AI questions measure the same thing)
- **Creativity General**: α = 0.69 (Acceptable)
- **Authorship Core**: α = 0.75 (Acceptable)

**What the code does:**
1. Calculates alpha for each category
2. Tests which authorship items work best together
3. Creates refined "core" scales with better reliability

---

### Step 6: Correlation Analysis

**What is correlation?**
Correlation measures how two things relate to each other. For example:
- If students who use AI more also feel less creative, there's a negative correlation
- If students who use AI more feel more ownership, there's a positive correlation

**The code calculates:**
```python
# Correlation between AI usage and creativity
AI_USE_SCORE vs CREATIVITY_GENERAL: r = -0.337, p = 0.0000

# Correlation between AI usage and authorship
AI_USE_SCORE vs AUTHORSHIP_SCORE: r = 0.444, p = 0.0000

# Correlation between creativity and authorship
CREATIVITY_GENERAL vs AUTHORSHIP_SCORE: r = -0.170, p = 0.0134
```

**What these numbers mean:**

1. **AI Usage ↔ Creativity (r = -0.337)**
   - **Negative correlation** = Students who use AI MORE tend to feel LESS creative
   - **p < 0.001** = This relationship is statistically significant (not random)
   - **Moderate strength** = The relationship is noticeable but not extremely strong

2. **AI Usage ↔ Authorship (r = 0.444)**
   - **Positive correlation** = Students who use AI MORE feel MORE ownership
   - **p < 0.001** = Statistically significant
   - **Moderate-strong** = This is a fairly strong relationship

3. **Creativity ↔ Authorship (r = -0.170)**
   - **Negative correlation** = Students who feel MORE creative feel LESS ownership (or vice versa)
   - **p = 0.013** = Statistically significant but weaker relationship
   - **Weak** = The relationship exists but is not very strong

---

## Key Findings (What the Data Shows)

### 1. AI Usage Patterns
- Average AI usage score: ~2.0 (on a 1-5 scale, where 1 = never, 5 = always)
- Students use AI most for **editing/proofreading** (mean = 2.86)
- Students use AI least for **drafting full paragraphs** (mean = 2.06)
- Most students use AI **sometimes**, not all the time

### 2. Creativity Feelings
- Average creativity score: ~3.8 (students generally feel creative)
- Students are confident in their ability to generate ideas without AI (mean = 4.07)
- Students don't think AI makes them MORE creative (mean = 2.15)

### 3. Authorship/Authenticity
- Students generally feel their work is their own (mean = 4.34)
- Students are somewhat comfortable taking credit for AI-assisted work (mean = 2.64)
- Students don't worry much about getting caught (mean = 1.83)

### 4. Relationships Found
- **More AI use → Less general creativity** (but this might be because creative students use AI less, not that AI makes them less creative)
- **More AI use → More feelings of ownership** (surprising! Students who use AI more feel MORE like the work is theirs)
- **More creativity → Slightly less ownership** (weak relationship)

---

## Technical Details

### Data Structure
- **212 students** responded to the survey
- **28 columns** of data (demographics + survey questions)
- **Scale**: Most questions use a 1-5 Likert scale
  - 1 = Strongly Disagree / Never
  - 5 = Strongly Agree / Always

### Missing Data
- Some students didn't answer all questions (shown as NaN)
- The code handles this by only using complete responses for calculations

### Statistical Methods Used
1. **Descriptive Statistics** - Mean, median, standard deviation
2. **Cronbach's Alpha** - Internal consistency reliability
3. **Pearson Correlation** - Linear relationships between variables
4. **Item Analysis** - Testing which questions work best together

---

## What's Missing or Could Be Improved

### 1. Visualizations
- The code imports `matplotlib` but doesn't create any plots
- **Could add**: Bar charts, scatter plots, correlation heatmaps

### 2. Advanced Statistics
- No regression analysis (predicting one variable from another)
- No group comparisons (e.g., do boys vs. girls use AI differently?)
- No factor analysis (finding underlying patterns in questions)

### 3. Data Cleaning
- No handling of outliers
- No checking for response patterns (e.g., students who answer "5" to everything)

### 4. Documentation
- Limited comments explaining the "why" behind decisions
- No explanation of why certain items were reversed or excluded

---

## How to Use This Code

### To Run the Analysis:
1. Make sure you have Python installed
2. Install required packages: `pip install pandas numpy matplotlib`
3. Open the notebook: `jupyter notebook v1_analysis_notebook.ipynb`
4. Run all cells (Cell → Run All)

### To Understand the Results:
1. Look at the composite scores - these are the main outcomes
2. Check Cronbach's alpha - make sure your scales are reliable (>0.7)
3. Examine correlations - see what relationships exist
4. Review descriptive statistics - understand what students are saying

---

## Summary

This code is a **psychometric analysis** of survey data about AI usage in student writing. It:

1. ✅ Loads and cleans survey data
2. ✅ Organizes questions into meaningful categories
3. ✅ Creates composite scores for AI usage, creativity, and authorship
4. ✅ Tests the reliability of these scales
5. ✅ Finds relationships between the three main concepts

**Main Finding:** Students who use AI more tend to feel LESS creative but MORE ownership over their work - which is an interesting and somewhat counterintuitive result that might be worth exploring further!

---

## Questions You Might Have

**Q: Why are there multiple data files (v1, v2, v3)?**
A: These are likely different versions of the survey or data collected at different times. The code uses v3, which appears to be the most recent.

**Q: What does "index_col=0" mean?**
A: It tells pandas to use the first column (Timestamps) as row identifiers instead of creating new row numbers.

**Q: Why reverse some items?**
A: Some questions are worded negatively. Reversing them ensures all questions in a scale point in the same direction (higher = better).

**Q: Is this analysis complete?**
A: It's a solid foundation, but could be expanded with visualizations, more advanced statistics, and deeper interpretation of the results.

---

*Report generated from analysis of v1_analysis_notebook.ipynb*
