# Final Project Plan
Rosarys Esquilin \
Carey Business School, Johns Hopkins University \
BU.330.760.41.SP26: Generative AI \
Dr. Harang Ju \
April 17th, 2026

## 1. Project Title
**Data to Insights Generator**

## 2. Target User, Workflow, & Business Value
**User:** A freelance analytics consultant.

**Workflow:** The consultant inputs a business question & a small structured dataset into the generator. The system calculates relevant metrics from the dataset & uses those grounded results to generate an insight brief for review.

**The Process:** 
- Begins: The consultant inputs a structured dataset & business question to investigate. 
- Ends: The consultant receives a draft insight brief containing key findings, supporting metrics, limitations, & suggested follow-up questions for review.

**Business Value:** This workflow reflects a realistic analytics task in which the consultant must quickly translate data into clear, business-facing observations. Improving this step matters because it can save time, create a more consistent first-pass at interpretation, & help the analyst move more efficiently from raw data to supporting materials. The value is not in replacing analysis, but in supporting early-stage insight generation in a controlled, evaluable way.

## 3. Problem Statement & GenAI Fit
This project will build a GenAI app for a freelance analytics consultant who is launching a consulting business & needs a more efficient way to turn client data into usable insights. The app will take a small structured dataset & a focused business question as input, compute descriptive metrics, & generate a first-pass insight brief for review. The goal is not to automate analysis end to end, but to support the interpretation & communication stage of the workflow in a more efficient way.

This workflow is a strong fit for GenAI because the final task is communication-heavy. Once the underlying metrics are calculated, the system must organize those results into a business-facing summary, highlight notable patterns, identify limitations, & suggest reasonable follow-up questions. A simpler non-GenAI tool could compute the descriptive metrics, but it would be less effective at turning the results into a readable insight brief that supports the early stage of a freelance consultant’s service workflow, which could later develop into dashboard builds, predictive analysis, or prescriptive analytics based on the client’s goals.

## 4. Planned System Design & Baseline
**Expected Workflow:**  
The system will be built as a Streamlit web app that supports one narrow workflow: a user uploads a small structured CSV file & a focused business question. The app will first inspect the dataset & calculate relevant descriptive metrics based on the available fields, such as counts, totals, averages, & basic changes over time where applicable. Those computed results will then be passed into an LLM with a prompt that asks the model to generate a first-pass insight brief. This creates a simple multi-step workflow in which deterministic code handles the quantitative calculations & the LLM handles the business-facing interpretation & communication.

**Course Concepts:**
1. **Tool Use or Function Calling:**  
A Python script will be used as a tool layer to calculate the underlying descriptive metrics before the LLM generates the written output. This keeps the system grounded in computed results rather than asking the model to infer unsupported numbers directly from the raw dataset.

2. **Evaluation Design: Rubrics, Test Sets, Baselines, Model-As-Judge:**  
Outputs will be assessed using a rubric focused on faithfulness to the data, usefulness, completeness, & clarity, with a spot-check of whether the written findings accurately reflect the computed results.

**Alternative:**  
The alternative will be a simpler prompt-only workflow. In that version, the model will receive a dataset summary & business question without the structured metric-calculation step. Comparing the two versions will help show whether the more grounded design improves output quality, usefulness, & trustworthiness.

**The App Experience:**  
The app will include a file uploader for the dataset, a text box for the business question, & a "Go" button to generate the output. After the user submits both inputs, the system will calculate descriptive metrics, pass the results into the LLM, & display a draft insight brief on the screen. The output will include:
- The Business Question
- Key Findings
- Supporting Metrics
- Limitations 
- & Suggested Follow-Up Questions

The interface will remain simple so the app stays focused on one clear task: <span style="color:seagreen">*turning a dataset & business question into a first-pass insight brief for review*.</span>

## 5. Evaluation Plan
Success for this workflow means that the system produces an insight brief that is useful to the freelance analyst, faithful to the computed results, clear in its wording, & appropriately limited in its claims (no hallucinations).

I plan to evaluate the system using the following dimensions:
- **Faithfulness:** Are the stated findings consistent with the computed metrics?
- **Usefulness:** Would the output help the freelance analyst begin interpreting the dataset?
- **Completeness:** Does the brief include the main findings, supporting numbers, limitations, & follow-up questions?
- **Clarity:** Is the output organized & well-written for review?
- **Boundaries:** Does the system avoid unsupported causal or predictive claims when the workflow is limited to descriptive analytics only? Does it hallucinate?
- **Usability:** Is the app responsive enough for practical use in a demo setting?

The test set will consist of about 3 structured datasets & focused business questions. The examples will be designed to reflect realistic descriptive analytics tasks such as segment comparison, trend summary, or category performance review.

The system will be compared against the prompt-only LLM (e.g., ChatGPT, Claude) on the same examples. I will use a rubric to score both versions & review whether the app produces more faithful & useful outputs than the chosen LLM.

## 6. Example Inputs & Failure Cases
**Use Cases:**
1. A transaction dataset with the question: *“How did average order value and order volume differ across product categories?”*
2. A customer activity dataset with the question: *“What patterns appear repeatedly versus one-time customer behavior?”*
3. A month-over-month transaction dataset with the question: *“How did revenue & product popularity change from Month 1 to Month 3?”*

**Failure Cases:**
1. The dataset is too messy, incomplete, or poorly structured for reliable metric calculation.
2. The business question is too broad, vague, or asks for causal or predictive conclusions that the system is not designed to support.

## 7. Risks & Governance
**Where The System Could Fail** \
The main risk is that the system could lead users to make overly conclusive observations based on descriptive metrics alone. While the app is intended to summarize patterns in the data, descriptive results by themselves do not explain causality or justify stronger strategic conclusions without further analysis. For that reason, the output should be treated as a first-pass interpretive aid rather than a standalone basis for decision-making.

**Where It Should Not Be Trusted** \
The system should not be trusted for causal claims, predictive conclusions, or high-stakes business decisions without human review. It should also not hallucinate missing values, hidden drivers, or unsupported explanations.

**Expected Controls, Refusal Rules, or Human-Review Boundaries** \
To manage those risks, the app will include clear human-review boundaries. It will frame the output as a draft insight brief rather than a final recommendation. The system will also be instructed to note limitations, avoid unsupported claims, & acknowledge if the question cannot be fully addressed with the available data.

**Data, Privacy, or Cost Concerns** \
For data, privacy, & cost considerations, I plan to use publicly available datasets from Kaggle & the UCI Machine Learning Repository. If I need a more controlled example, I will create a synthetic dataset generated with ChatGPT. To manage cost, I plan to use **Google AI Studio** for its free API usage across multiple available models. For security, my API Key will be stored in an .env file and excluded from the repository through .gitignore.

## 8. Plan for the Week 6 Check-In
By the Week 6, I expect to have:
- A finalized dataset & business question.
- A working Python script that calculates the descriptive metrics.
- An initial prompt & output structure for the draft insight brief.
- An early prototype of the workflow.
- A comparison prompt for evaluating the LLM-generated output.

## 9. Track My Progress Here!
**Github Repository**: https://github.com/ro-esq7/Data_To_Insights_Generator
