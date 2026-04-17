# Data to Insights Generator
## Rosarys Esquilin


---
## Introduction
This project explores the development of a small GenAI application designed to support a real-world analytics workflow. The goal of the app is to take a business question & a dataset as input, then generate a first-pass set of insights for review. Rather than replacing analysis, the system is intended to assist with early-stage interpretation by organizing computed results into a clear insight brief.

This project will be built as a runnable Streamlit web application. The final system will be evaluated against a simpler baseline to assess usefulness, faithfulness to the underlying data, & appropriate trust boundaries.


---
## Project Plan Workflow
- **User:** A freelance analytics consultant.  

- **Workflow:** The consultant inputs a business question & a small structured dataset into the generator. The system calculates relevant metrics from the dataset & uses those grounded results to generate an insight brief for review.  

- **Expected Output:** A draft insight brief containing key findings, supporting metrics, limitations, & suggested follow-up questions.  

- **Why:** I selected this workflow because it reflects a realistic analytics use case, aligns closely with my background, & keeps the system focused on a narrow business task.


---
## Business Question & Dataset 
### (TBD)
The final business question & dataset are still being determined & will be updated as the project develops. The current plan is to use a small structured dataset & pair it with a focused business question that can support a narrow analytics workflow.

**Potential Questions**:
- Which customer segments contributed the most revenue during the selected period, and how did revenue, order volume, and average order value differ across those groups?
- Based on the available customer and transaction data, which customers or segments appear most likely to return for a future purchase?


---
## Git Workflow Summary
This project will be developed incrementally using GitHub for version control & documentation throughout the process. **GitHub Desktop** will be used to manage commits & track project milestones, while **Python** will be used to build the prototype for the generator. **OpenAI's Codex** will support selected coding tasks during development, particularly for setup, iteration, & refinement.

The project will begin with planning and repository setup & project plan, followed by exploratory development of the metric calculation & insight-generation workflow. As the project progresses, the core logic will be incorporated into a Streamlit application so the final deliverable is a runnable web app. Commits will be used regularly to document progress, preserve working versions, & support a reproducible development process.


---
## Commit Log
- **Repository Setup**: Created the project repository with the required starter files.
- **Project Plan Submission**: Uploaded the project plan for instructor & TA review.
