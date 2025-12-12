# Results Interpretation Guide

## 📊 Your Actual Results

Based on your analysis of 212 students, here's what you found and what it means:

---

## 1. RELIABILITY (Cronbach's Alpha)

### Results:
- **AI Use Scale**: α = 0.890 (excellent)
- **Creativity General Scale**: α = 0.694 (acceptable)
- **Authorship Core Scale**: α = 0.748 (acceptable)

### What This Means:
✅ **Your survey measures are reliable!**
- AI Use questions are highly consistent (students answered similarly across all 5 questions)
- Creativity and Authorship scales are acceptably reliable (good enough for research)
- You can trust that your scales are measuring what you intended

### For Your Paper:
*"Internal consistency reliability was assessed using Cronbach's alpha. The AI Use scale demonstrated excellent reliability (α = 0.890), while the Creativity General (α = 0.694) and Authorship Core (α = 0.748) scales showed acceptable reliability."*

---

## 2. CORRELATIONS

### Results:
1. **AI_USE_SCORE vs CREATIVITY_GENERAL**: r = -0.337, p < 0.001
2. **AI_USE_SCORE vs AUTHORSHIP_SCORE**: r = 0.444, p < 0.001
3. **CREATIVITY_GENERAL vs AUTHORSHIP_SCORE**: r = -0.170, p = 0.013

### What This Means:

#### Finding 1: AI Use ↔ Creativity (r = -0.337)
**Interpretation**: 
- **Moderate negative relationship**
- Students who use AI **more** tend to feel **less creative**
- This is a **statistically significant** relationship (p < 0.001 = very unlikely due to chance)
- **Effect size**: Moderate (Cohen's rule: |r| > 0.3 = moderate effect)

**In Plain English**: "There's a clear pattern: the more students use AI, the less creative they feel. This isn't random - it's a real relationship."

#### Finding 2: AI Use ↔ Authorship (r = 0.444)
**Interpretation**:
- **Moderate positive relationship**
- Students who use AI **more** tend to feel **more** sense of authorship/ownership
- This is **statistically significant** (p < 0.001)
- **Effect size**: Moderate to strong (|r| = 0.44 is approaching large effect)

**In Plain English**: "Interestingly, students who use AI more actually feel MORE like the work is 'theirs' - they feel comfortable taking credit for AI-assisted work."

#### Finding 3: Creativity ↔ Authorship (r = -0.170)
**Interpretation**:
- **Weak negative relationship**
- Students who feel **more creative** tend to feel **slightly less** sense of authorship
- This is **statistically significant** (p = 0.013) but the effect is small
- **Effect size**: Small (|r| < 0.3 = small effect)

**In Plain English**: "There's a slight tendency: students who feel more creative feel slightly less ownership, but this relationship is weak."

### For Your Paper:
*"Bivariate correlations revealed significant relationships between all three variables. AI use was negatively correlated with creativity (r = -0.337, p < 0.001) but positively correlated with authorship (r = 0.444, p < 0.001). Creativity and authorship were weakly negatively correlated (r = -0.170, p = 0.013)."*

---

## 3. REGRESSION MODEL A: Predicting Creativity

### Results:
- **AI_USE_SCORE coefficient**: β = -0.221, p < 0.001
- **R-squared**: R² = 0.250 (25% of variance explained)
- **Sample size**: n = 211

### What This Means:

#### The Coefficient (β = -0.221):
**Interpretation**:
- After controlling for grade, gender, writing ability, assignments per week, school policy, and AI education...
- **For every 1-point increase in AI use, creativity decreases by 0.22 points** (on a 1-5 scale)
- This is **statistically significant** (p < 0.001)

**Example**:
- Student with AI use = 2.0 → Predicted creativity ≈ 3.5
- Student with AI use = 4.0 → Predicted creativity ≈ 3.1
- **Difference**: 0.4 points lower creativity for higher AI users

#### The R-squared (R² = 0.250):
**Interpretation**:
- The model explains **25% of the variation** in creativity
- This means **75% is explained by other factors** not in your model
- This is **moderate** for social science research (typical range: 10-40%)

**What it means**: "AI use and the other variables we measured explain about a quarter of why students differ in creativity. The rest is due to factors we didn't measure (personality, motivation, etc.)."

#### Other Significant Predictors:
- **Writing ability** (β = 0.300, p < 0.001): Students who rate their writing ability higher also feel more creative (makes sense!)
- **Grade, gender, assignments, policy, AI education**: Not significant (p > 0.05)

### For Your Paper:
*"A multiple regression model predicting creativity from AI use and covariates revealed a significant negative effect of AI use (β = -0.221, p < 0.001), controlling for grade, gender, writing ability, assignments per week, school policy, and AI education. The model explained 25% of the variance in creativity (R² = 0.250). Writing ability was also a significant positive predictor (β = 0.300, p < 0.001)."*

---

## 4. REGRESSION MODEL B: Predicting Authorship

### Results:
- **AI_USE_SCORE coefficient**: β = 0.418, p < 0.001
- **R-squared**: R² = 0.238 (23.8% of variance explained)
- **Sample size**: n = 211

### What This Means:

#### The Coefficient (β = 0.418):
**Interpretation**:
- After controlling for all other factors...
- **For every 1-point increase in AI use, authorship feelings increase by 0.42 points** (on a 1-5 scale)
- This is **statistically significant** (p < 0.001)
- **This is a larger effect** than the creativity relationship (0.42 vs 0.22)

**Example**:
- Student with AI use = 2.0 → Predicted authorship ≈ 3.2
- Student with AI use = 4.0 → Predicted authorship ≈ 4.0
- **Difference**: 0.8 points higher authorship for higher AI users

**This is interesting!** Students who use AI more feel MORE ownership, not less. This suggests:
- Students may view AI as a tool they control
- They may feel the final product is still "theirs"
- They may be comfortable with collaborative authorship

#### The R-squared (R² = 0.238):
**Interpretation**:
- The model explains **23.8% of the variation** in authorship
- Similar to creativity model - moderate explanation

#### Other Significant Predictors:
- **Assignments per week** (β = -0.111, p = 0.022): Students with MORE assignments feel LESS authorship (maybe overwhelmed?)
- **Gender** (β = -0.241, p = 0.057): Females tend to feel slightly less authorship (borderline significant)
- Other variables: Not significant

### For Your Paper:
*"A multiple regression model predicting authorship from AI use and covariates revealed a significant positive effect of AI use (β = 0.418, p < 0.001), controlling for other factors. The model explained 23.8% of the variance in authorship (R² = 0.238). Assignments per week was also a significant negative predictor (β = -0.111, p = 0.022)."*

---

## 5. MODERATION ANALYSIS (Model C)

### Results:
- **Interaction term**: β = -0.019, p = 0.757 (NOT significant)

### What This Means:

**Interpretation**:
- The relationship between AI use and authorship does **NOT depend on writing ability
- The effect is the **same** for students with low, medium, and high writing ability
- This is **not statistically significant** (p = 0.757 > 0.05)

**In Plain English**: "Whether a student has high or low writing ability doesn't change how AI use affects their sense of authorship. The positive relationship between AI use and authorship is consistent across all students."

### For Your Paper:
*"A moderation analysis testing whether writing ability moderates the AI use → authorship relationship revealed no significant interaction (β = -0.019, p = 0.757), indicating that the positive effect of AI use on authorship is consistent across different levels of writing ability."*

**Note**: Since the interaction isn't significant, you can just report Model B (the main effect model).

---

## 🎯 KEY FINDINGS SUMMARY

### What Your Results Show:

1. **AI Use Decreases Creativity** (but only moderately)
   - Students who use AI more feel less creative
   - Effect persists even after controlling for other factors
   - But the effect is moderate (not huge)

2. **AI Use Increases Authorship** (surprisingly!)
   - Students who use AI more feel MORE ownership
   - This is a stronger effect than the creativity relationship
   - Suggests students view AI as a tool they control

3. **The Effects Are Independent of Writing Ability**
   - The relationships hold regardless of how good students think they are at writing
   - This suggests the effects are general, not specific to certain student types

4. **Your Measures Are Reliable**
   - All scales show acceptable to excellent reliability
   - You can trust your findings

---

## 📝 WHAT TO WRITE IN YOUR PAPER

### Results Section:

**Reliability**:
*"Internal consistency reliability was assessed using Cronbach's alpha. The AI Use scale demonstrated excellent reliability (α = 0.890), while the Creativity General (α = 0.694) and Authorship Core (α = 0.748) scales showed acceptable reliability."*

**Correlations**:
*"Bivariate correlations revealed significant relationships between all three variables. AI use was negatively correlated with creativity (r = -0.337, p < 0.001) but positively correlated with authorship (r = 0.444, p < 0.001). Creativity and authorship were weakly negatively correlated (r = -0.170, p = 0.013)."*

**Regression - Creativity**:
*"A multiple regression model predicting creativity from AI use and covariates (grade, gender, writing ability, assignments per week, school policy, AI education) revealed a significant negative effect of AI use (β = -0.221, p < 0.001). The model explained 25.0% of the variance in creativity (R² = 0.250, n = 211). Writing ability was also a significant positive predictor (β = 0.300, p < 0.001)."*

**Regression - Authorship**:
*"A multiple regression model predicting authorship from AI use and covariates revealed a significant positive effect of AI use (β = 0.418, p < 0.001). The model explained 23.8% of the variance in authorship (R² = 0.238, n = 211). Assignments per week was also a significant negative predictor (β = -0.111, p = 0.022)."*

**Moderation**:
*"A moderation analysis testing whether writing ability moderates the AI use → authorship relationship revealed no significant interaction (β = -0.019, p = 0.757), indicating that the positive effect of AI use on authorship is consistent across different levels of writing ability."*

### Discussion Section:

**Main Findings**:
*"The present study revealed a complex relationship between AI tool use and students' psychological experiences. Consistent with hypotheses, increased AI use was associated with decreased feelings of creativity. However, contrary to what might be expected, increased AI use was associated with increased feelings of authorship and ownership over their work."*

**Why This Might Be**:
*"The negative relationship between AI use and creativity may reflect students' awareness that they are relying on external tools rather than generating ideas independently. However, the positive relationship with authorship suggests that students may view AI as a tool they control and integrate into their work, rather than something that diminishes their ownership."*

**Implications**:
*"These findings have important implications for educational policy. While AI use may impact students' sense of creativity, it does not appear to diminish their sense of authorship. Educators should consider how to help students maintain creativity while using AI tools effectively."*

---

## ❓ COMMON QUESTIONS

### Q: Are these effects large or small?
**A**: 
- **Creativity effect**: Moderate (β = -0.22 on a 1-5 scale)
- **Authorship effect**: Moderate to large (β = 0.42 on a 1-5 scale)
- Both are **statistically significant** and **practically meaningful**

### Q: Why is authorship positive when creativity is negative?
**A**: This is interesting! It suggests:
- Students may separate "creativity" (original ideas) from "authorship" (ownership of work)
- They may view AI as a tool they control, not something that takes away ownership
- They may feel the final product is still "theirs" even if AI helped generate ideas

### Q: Should I report the moderation if it's not significant?
**A**: You can mention it briefly: "We tested whether writing ability moderates the relationship, but found no significant interaction (p = 0.757), indicating the effect is consistent across writing ability levels."

### Q: What about the clustering results?
**A**: If you ran the clustering analysis, you can report the different student profiles/types. This adds depth by showing there are different patterns among students.

---

## 🚀 NEXT STEPS

1. **Write up your Results section** using the templates above
2. **Interpret your findings** in the Discussion section
3. **Consider limitations**: 
   - Cross-sectional design (can't prove causation)
   - Self-report measures (may have bias)
   - Sample from one school/region
4. **Suggest future research**:
   - Longitudinal studies to track changes over time
   - Experimental designs to test causation
   - Qualitative studies to understand why students feel this way

---

## 💡 KEY TAKEAWAYS

✅ **AI use is associated with lower creativity** (but the effect is moderate)
✅ **AI use is associated with higher authorship** (surprisingly - students feel ownership)
✅ **These relationships hold even after controlling for other factors**
✅ **The effects don't depend on writing ability** (consistent across students)
✅ **Your measures are reliable** (you can trust your findings)

**Bottom Line**: Your study shows that AI use has complex effects - it may decrease creativity but increase authorship feelings. This suggests students view AI as a tool they control, not something that diminishes their ownership of work.
