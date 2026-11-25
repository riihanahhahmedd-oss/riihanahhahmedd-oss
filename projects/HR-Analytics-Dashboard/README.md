# HR Analytics Executive Dashboard

An HR analytics project built with **Microsoft Excel** and a self-contained **interactive HTML dashboard**. It explores workforce composition, compensation, hiring patterns, and employee exits to turn HR data into practical business questions.

## Live preview

- [Open the interactive dashboard](https://htmlpreview.github.io/?https://raw.githubusercontent.com/riihanahhahmedd-oss/riihanahhahmedd-oss/main/projects/HR-Analytics-Dashboard/dashboard.html)
- [View the dashboard source](./dashboard.html)

The original Excel workbook is supplied separately. The public dashboard uses verified aggregate metrics from a de-identified copy of its Employee Directory; employee names and IDs are not published.

## Business questions

1. How is the workforce distributed across departments and countries?
2. Which departments have the largest headcount and payroll?
3. How do average and median salaries differ by department?
4. Which departments have exit rates above the overall rate?
5. What does the age, tenure, and gender composition look like?

## Verified findings

| Metric | Result |
|---|---:|
| Employee records | 1,000 |
| Active employees | 915 (91.5%) |
| Exited employees | 85 (8.5%) |
| Annual salary payroll | $112,801,802 |
| Average annual salary | $112,802 |
| Median annual salary | $111,063 |
| Average total compensation | $122,798 |
| Average age | 43.2 years |
| Average tenure | 16.5 years |
| Gender distribution | 50.1% female / 49.9% male |

## Department comparison

| Department | Headcount | Average salary | Exited | Exit rate |
|---|---:|---:|---:|---:|
| Accounting | 96 | $122,372 | 7 | 7.3% |
| Engineering | 158 | $108,486 | 17 | 10.8% |
| Finance | 120 | $122,545 | 9 | 7.5% |
| Human Resources | 125 | $117,364 | 11 | 8.8% |
| IT | 241 | $97,661 | 16 | 6.6% |
| Marketing | 120 | $129,405 | 15 | 12.5% |
| Sales | 140 | $110,519 | 10 | 7.1% |

## Analyst storytelling

- **IT is the largest department**, representing 24.1% of all employee records, and has the highest department payroll.
- **Marketing has the highest observed exit rate** (12.5%), followed by Engineering (10.8%). These patterns suggest where HR could investigate further; they do not explain why employees leave.
- **IT has the lowest average salary** among departments, while Marketing has the highest. A fair compensation comparison would need to control for job title, seniority, and location.
- The workforce is concentrated in the **United States (641 records)**, followed by China (229) and Brazil (130).

## Tools and techniques

- **Excel:** structured employee table, KPI dashboard, formulas, charts, and pivot-style summaries.
- **HTML, CSS, JavaScript:** interactive dashboard interface and department filter.
- **Data analysis:** descriptive statistics, workforce segmentation, compensation analysis, and exit-rate comparison.
- **Storytelling:** translating metrics into follow-up business questions without making unsupported causal claims.

## Project files

- [dashboard.html](./dashboard.html) — interactive browser dashboard.
The original Excel workbook is provided separately as a downloadable project file; this public repository page focuses on the interactive dashboard and verified analysis story.

## Interpretation notes

- This is descriptive analysis of the supplied dataset; it does not establish causal reasons for employee exits.
- Department salary comparisons are not adjusted for job title, seniority, or location.
- The public-facing dashboard does not expose employee-level names or IDs.

---

**Created by Rihanah Ahmed** · [GitHub](https://github.com/riihanahhahmedd-oss) · [LinkedIn](https://www.linkedin.com/in/rihanah-ahmedd-772823392)
