# HR Analytics Executive Dashboard

An HR analytics portfolio project built with **Microsoft Excel** and a self-contained **interactive HTML dashboard**. The project explores workforce composition, compensation, hiring patterns, and employee exits.

## Live interactive dashboard

- [Open the interactive dashboard](https://htmlpreview.github.io/?https://raw.githubusercontent.com/riihanahhahmedd-oss/riihanahhahmedd-oss/main/projects/HR-Analytics-Dashboard/dashboard.html)
- [View the dashboard source](./dashboard.html)

The interactive dashboard includes six connected filters: **Department, Country, Business Unit, Gender, Ethnicity, and Employment Status**. Every filter updates all KPI cards, charts, and the department comparison table together. Filter choices respond to the current selection, and a Reset Filters control restores the full dataset.

## Dashboard visuals

- Payroll budget by department
- Average salary benchmark by department
- Workforce hiring trend (1995–2021)
- Workforce distribution by country
- Gender and employment-status composition
- Department workforce and compensation table

The desktop layout is designed to fit in one viewport at common laptop/desktop resolutions. Smaller screens switch to a scrollable responsive layout.

## Verified business metrics

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
| Gender distribution | 501 female (50.1%) / 499 male (49.9%) |

## Department comparison

| Department | Headcount | Average salary | Median salary | Exited | Exit rate |
|---|---:|---:|---:|---:|---:|
| Accounting | 96 | $122,372 | $123,147 | 7 | 7.3% |
| Engineering | 158 | $108,486 | $109,035 | 17 | 10.8% |
| Finance | 120 | $122,545 | $122,803 | 9 | 7.5% |
| Human Resources | 125 | $117,364 | $118,058 | 11 | 8.8% |
| IT | 241 | $97,661 | $97,790 | 16 | 6.6% |
| Marketing | 120 | $129,405 | $129,663 | 15 | 12.5% |
| Sales | 140 | $110,519 | $111,050 | 10 | 7.1% |

## Analyst storytelling

- **IT is the largest department**, with 241 employees (24.1% of all records) and the highest total salary payroll.
- **Marketing has the highest observed exit rate** (12.5%), followed by Engineering (10.8%). These are signals for further investigation, not evidence of why employees leave.
- **Marketing has the highest average salary**, while IT has the lowest. A fair compensation comparison should control for job title, seniority, and location.
- The workforce is concentrated in the **United States (641 records)**, followed by China (229) and Brazil (130).

## Data quality checks

- 1,000 employee records and 1,000 unique employee IDs; no duplicate employee IDs.
- No missing values in Department, Country, Business Unit, Gender, Employment Status, Annual Salary, Age, or Tenure.
- Employment Status agrees with Exit Date for all 1,000 records.
- **Ethnicity is blank for all 1,000 records.** The dashboard therefore exposes the filter as “Not Provided” and does not invent an ethnicity breakdown.
- The Executive Dashboard department summary and Pivot Analytics summaries were recalculated from the Employee Directory source rows. This corrected stale country, hiring-year, and salary summary values in the original workbook.

## Privacy and interpretation

The public interactive dashboard uses **grouped aggregate data** only. Employee names and employee IDs are not published. This is descriptive analysis and does not establish causal reasons for employee exits. Department salary comparisons are not adjusted for job title, seniority, or location.

## Tools and techniques

- **Excel:** structured employee table, KPI dashboard, formulas, charts, and recalculated summary tables.
- **HTML, CSS, JavaScript:** responsive dashboard, six synchronized filters, dynamic KPI calculations, and SVG charts.
- **Data analysis:** descriptive statistics, workforce segmentation, compensation analysis, hiring trends, and exit-rate comparison.
- **Storytelling:** translating workforce metrics into practical business questions without making unsupported causal claims.

---

**Created by Rihanah Ahmed** · [GitHub](https://github.com/riihanahhahmedd-oss) · [LinkedIn](https://www.linkedin.com/in/rihanah-ahmed-772823392)
