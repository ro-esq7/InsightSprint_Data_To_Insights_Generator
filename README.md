# InsightSprint
*From Retail Transaction Data to Reviewable Insights* \
*Rosarys Esquilin*


## Deployed App
***InsightSprint Streamlit App:** https://insightsprint.streamlit.app*


## Introduction
**InsightSprint** is a GenAI-powered descriptive analytics workflow designed to support a freelance analytics consultant serving a small retail client. The app takes a structured retail transaction dataset & one supported business question as input, computes grounded descriptive metrics in Python, & then generates a first-pass insight brief for review.

Rather than replacing analysis, the goal of the system is to make the early stage of insight development more efficient, more consistent, & easier to communicate. The final output is a reviewable insight brief that remains grounded in computed results rather than unsupported model-generated claims.


## Toolkit
This project was built using the following tools:

- **Python**
- **Streamlit Community Cloud**
- **ChatGPT**
- **OpenAI API**
- **OpenAI Codex**
- **GitHub Desktop**

**Note on Deployment:** For this project, **Python 3.11+** was needed to deploy successfully with Streamlit Community Cloud.


## Target User, Workflow, & Business Value
### **User:** 
A freelance analytics consultant serving a small retail client. 

### **Workflow:** 
The user uploads a retail transaction dataset & selects one supported descriptive business question. The app then computes the relevant descriptive metrics in Python & uses those grounded results to generate a first-pass insight brief for review. 

### **Supported Business Questions**
1. Which product was the most popular each month?
2. How did total revenue chnage from Month 1 to Month 3?
3. Which channel generated more revenue: Online or In-Store?

### **Expected Output:** 
A structured insight brief with the following sections:
1. Business Question  
2. Key Findings  
3. Supporting Metrics  
4. Limitations / Caveats  
5. Suggested Follow-Up Questions   

### **Business Value** 
This workflow reflects a realistic consulting task in which early descriptive findings need to be translated into a clear, business-facing format. **InsightSprint** helps make that process more efficient & consistent by combining deterministic metric calculation with structured LLM-generated communication. The value of the system is not in replacing the analysis, but in supporting early-stage insight development in a more scalable way.


## Evaluation

The table below summarizes the small evaluation set used to compare the full InsightSprint workflow against a simpler prompt-only baseline.

| Test Case | Full InsightSprint Workflow | Prompt-Only Baseline | Result |
|---|---|---|---|
| Most Popular Product by Month | Correctly identified the top product in each month using computed metrics & presented the results in the required structured format. | More variable in formatting & more dependent on how the summary was written into the prompt. | Workflow was more grounded & consistent |
| Revenue Change from Month 1 to Month 3 | Correctly summarized month-over-month revenue change using Python-calculated metrics & structured supporting evidence. | Could summarize the trend, but was less reliable in presenting detailed numeric support consistently. | Workflow produced clearer & more faithful output. |
| Online vs. In-Store Revenue | Correctly identified the higher-revenue channel & supported the result with revenue share, orders, & units sold. | Could identify the general pattern, but formatting & supporting detail were less consistent. | Workflow was more reliable & easier to review. |


## How the Agent Works
**InsightSprint** follows a narrow descriptive analytics workflow:

1. The user uploads a CSV file containing the retail transaction data.
2. The app validates that the required columns are present.
3. The dataset is previewed in the Streamlit interface.
4. The user is prompted to select one supported business question.
5. Python computes the relevant descriptive metrics.
6. The computed metrics are passed into a constrained prompt.
7. The OpenAI model generates a structured insight brief for review.
8. If an API key is unavailable or the request fails, the app falls back to a grounded demo output built directly from the computed metrics.

This design keeps the quantitative logic in Python & reserves the LLM for summarization, explanation, & business-facing communication.


## Building the Agent & Streamlit App
This project was built in stages:

### 1. Project Definition
The workflow was narrowed from a broad analytics assistant idea into one focused use case: 
- **A freelance consultant working with synthetic retail transaction data & a small set of supported descriptive questions.**

### 2. Synthetic Dataset Design
A synthetic jewelry transaction dataset was created across three months with realistic retail fields, including:
- `customer_id`
- `customer_status`
- `order_channel`
- `order_date`
- `order_id`
- `order_month`
- `order_revenue`
- `product_category`
- `product_name`
- `region`
- `sku_id`
- `units_sold`

### 3. Descriptive Question Logic
A reusable Python script was created to compute the metrics needed to answer the three supported questions:
- `analyze_most_popular_item_per_month()`
- `analyze_revenue_change_month1_to_month3()`
- `analyze_channel_revenue()`

The script also saves the output CSV files used for testing & validation.

### 4. Prompt Design
The prompt structure was split into:
- `prompts.py` for the working prompt variables used in the app
- `insightsprint_prompt_file.md` for prompt documentation in the repository

The prompts were constrained to:
- Only use computed metrics.
- Avoid unsupported claims.
- Remain descriptive only.
- Return a fixed five-section insight brief.

### 5. Streamlit App Development
The Streamlit App was then built to:
- Upload the CSV.
- Validate required columns.
- Preview the dataset.
- Let the user choose one supported business question.
- Compute the Descriptive Metrics.
- Generate the Insight Brief.

### 6. OpenAI Integration
**OpenAI** was integrated into the app so the computed metrics could be transformed into a structured insight brief. A fallback demo mode was also built so the app could still function when an API key was missing or unavailable.

### 7. UI Styling & Deployment
The app was styled using my favorite custom palette centered on:
- Slate: `#37474F`
- Dark Teal: `#64BEB6`
- Light Gray: `#F5F5F5`

After local testing, the app was deployed to **Streamlit Community Cloud** & verified end to end.


## Git Workflow Summary
This project was developed incrementally using **GitHub Desktop** for version control and documentation throughout the build process. The workflow began with repository setup and project planning, followed by environment configuration, dataset preparation, **Python** question logic, prompt design, **Streamlit App** development, **OpenAI** integration, UI styling, and deployment.

Commits were used throughout the project to preserve each major milestone & document how the system evolved from an initial plan into a deployed application. This staged workflow made it easier to test individual components, troubleshoot deployment issues, and keep the final product reproducible.


## Commit Log
- **Initial Commit**: Created the first repository checkpoint.
- **Repository Setup**: Created the project repository with the required starter files.
- **Project Plan Submission**: Uploaded the project plan for instructor and TA review.
- **Project Plan Refinement**: Refined the project plan to the final InsightSprint workflow and descriptive analytics scope.
- **Repository Structure**: Created the initial InsightSprint repository structure and organized the core project files.
- **.gitignore Setup**: Saved `.gitignore`.
- **Repository Cleanup**: Removed tracked environment and system files from the repository.
- **Environment Setup**: Added environment setup and protected the API key with `.gitignore`.
- **Requirements Update**: Updated requirements for the Streamlit app and OpenAI integration.
- **Question Logic & Outputs**: Built the InsightSprint question logic script and output generation workflow.
- **Prompt Files**: Updated `prompts.py` and `insightsprint_prompt_file.md` for InsightSprint’s insight brief generation.
- **OpenAI Integration**: Integrated OpenAI generation with demo fallback into the InsightSprint Streamlit app.
- **Test Outputs**: Saved app test outputs for review.
- **App Styling & Workflow**: Finalized InsightSprint app styling, prompt structure, and OpenAI workflow.
- **Deployment**: Deployed and verified the InsightSprint Streamlit app with OpenAI integration.
- **Final Polish**: Applied final polish updates to the deployed app.
- **Updated README**: Completed `README` with deployed app link, toolkit notes, workflow summary, & commit log.
- **Tool Evaluation**: Added evaluation summary & baseline comparison for **InsightSprint**.


## Repository Contents
- `app.py` – Main Streamlit Application
- `prompts.py` – System Prompt & User Prompt Template
- `insightsprint_question_logic.py` – Descriptive Analytics Functions
- `data/` – Synthetic Jewelry Transaction Dataset
- `outputs/` – Computed CSV Outputs for the Supported Questions
- `docs/` – Prompt Documentation & Project Planning Materials
- `requirements.txt` – Required Packages for Local Setup & Deployment