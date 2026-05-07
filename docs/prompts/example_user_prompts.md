# Example User Prompts

Below are some example natural language prompts that users can provide to the ValidateAI platform for dashboard validation workflows.

---

## 1. AWPer Validation for Canada

```text
Hey, can you validate the Tableau Overall dashboard data for all AWPer players from Canada in the Preprod environment? I specifically want to compare the T Target Last12 and CT Target Last12 metrics between the UI dashboard and backend database records. Ignore any players where the team filter is not available, and make sure this is done using row-level comparison logic.
```

---

## 2. Support Role Validation

```text
Please run a validation on the Tableau dashboard for Support role players from the NRG team in the Prod environment. I want to verify whether the CT Last12 Delta values shown on the UI exactly match the backend values stored in the database. Use the Overall screen and perform a row-level validation with the default tolerance.
```

---

## 3. Player Specific Validation

```text
I need to validate dashboard data for player oSee on the Tableau Overall screen in Preprod. Please compare the T Last12 Delta and CT Last12 Delta metrics from the frontend dashboard against the backend database data. This validation should only target the United States records and should ignore any missing optional filters.
```

---

## 4. HLTV WR and Age Validation

```text
Can you validate all Opener players available on the Tableau dashboard for the Overall screen in the QA environment? I want to compare the HLTV WR and Age metrics displayed on the dashboard against backend records and make sure the values are aligned within the configured tolerance.
```

---

## 5. Multi-Metric Validation

```text
Please perform a validation for players belonging to the Liquid team on the Tableau Overall dashboard in the Staging environment. I want to verify T Target Last12, CT Target Last12, and CT Last12 Delta metrics against backend database values using row-level validation.
```

---

## 6. Delta Metric Validation

```text
Run a dashboard validation for all Support players from Canada on the Tableau Overall dashboard in Preprod. Compare the T Last12 Delta and CT Last12 Delta values between UI and backend systems. If any metric is missing in the backend, mark the validation as failed in the comparison report.
```

---

## 7. Twistzz Player Validation

```text
I want to validate player Twistzz from the FaZe team on the Tableau dashboard. Use the Overall screen in the Prod environment and compare the T Target Last12, CT Target Last12, and HLTV WR metrics shown on the UI with backend database records.
```

---

## 8. United States AWPer Validation

```text
Please validate all AWPer role players from the United States in the Tableau Overall dashboard. Compare CT Last12 Delta and T Last12 Delta values between frontend and backend systems in the Preprod environment and provide row-level validation output.
```

---

## 9. Team M80 Validation

```text
Can you run a backend reconciliation for all players from team M80 on the Tableau dashboard in QA? I want to validate the Age, HLTV WR, and CT Target Last12 metrics displayed in the UI against the database values. Use the Overall screen and default validation tolerance settings.
```

---

## 10. Complete Enterprise Validation Workflow

```text
Please perform a complete validation workflow for AWPer players from Canada and team NRG on the Tableau Overall dashboard in Prod. I need to compare T Target Last12, CT Target Last12, T Last12 Delta, and CT Last12 Delta metrics between the frontend UI and backend database tables. Use row-level comparison logic and generate the validation result for each matched player record.
```