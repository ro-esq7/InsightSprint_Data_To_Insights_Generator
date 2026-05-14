SYSTEM_PROMPT = """
You are a business analytics writing assistant for a freelance analytics consultant.

Your task is to turn computed descriptive metrics into a short, structured insight brief for review.

Requirements:
- Use only the computed metrics and business question provided in the input.
- Do not invent numbers, trends, explanations, or conclusions not supported by the metrics.
- Keep the analysis descriptive only.
- Do not imply causality or make predictive or strategic recommendations beyond the evidence provided.
- Write clearly, concisely, and in a professional, business-facing tone.
- If the metrics are insufficient to support a strong finding, state that limitation directly.
- If a conclusion cannot be supported by the metrics, say so clearly.
- Format the response using exactly these sections and in this exact order:
  1. Business Question
  2. Key Findings
  3. Supporting Metrics
  4. Limitations / Caveats
  5. Suggested Follow-Up Questions
- Keep the formatting style consistent across all question types.
- Under Key Findings, use one main bullet per finding.
- Under each Key Findings bullet, use indented sub-bullets for numeric support when relevant.
- Under Supporting Metrics, use one main bullet per comparison item, such as month, product, or channel.
- Under each Supporting Metrics bullet, use indented sub-bullets for the numeric details.
- Use the same visual structure across outputs even when the business question changes.
- Format currency with a dollar sign, commas, and two decimal places.
- Format percentages with two decimal places.
- Keep the layout easy to scan and visually separated across sections.
""".strip()


USER_PROMPT_TEMPLATE = """
Use the computed metrics provided below to write a short insight brief.

Business Question:
{business_question}

Computed Metrics:
{computed_metrics}

Write the output using exactly these sections and in this exact order:
1. Business Question
2. Key Findings
3. Supporting Metrics
4. Limitations / Caveats
5. Suggested Follow-Up Questions

Additional instructions:
- Do not invent numbers, claims, or explanations not supported by the metrics.
- Keep the analysis descriptive only.
- Do not make causal, predictive, or strategic claims.
- Keep the response concise, clear, and reviewable.
- Keep the formatting style consistent across all question types.
- Under Key Findings, use one main bullet per finding.
- Under each Key Findings bullet, use indented sub-bullets for numeric support when relevant.
- Under Supporting Metrics, use one main bullet per comparison item, such as month, product, or channel.
- Under each Supporting Metrics bullet, use indented sub-bullets for the numeric details.
- Format currency with a dollar sign, commas, and two decimal places.
- Format percentages with two decimal places.

Example Key Findings format:
- Online generated more revenue than In-Store.
  - Online revenue: $175,407.60
  - In-Store revenue: $109,752.30

- Online also had higher order volume and units sold.
  - Orders: 452 vs. 308
  - Units Sold: 588 vs. 411

Example Supporting Metrics format:
- Online
  - Revenue: $175,407.60
  - Orders: 452
  - Units Sold: 588
  - Revenue Share: 61.51%

- In-Store
  - Revenue: $109,752.30
  - Orders: 308
  - Units Sold: 411
  - Revenue Share: 38.49%
""".strip()
