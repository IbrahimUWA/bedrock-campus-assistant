# Model comparison

10 questions, 3 run(s) each, through the full agent loop (guardrail, knowledge base, tools).
**Local stand-in run.** The models are open models on one workstation GPU and retrieval is local, because the AWS account's Bedrock model quota was still 0. The guardrail (ApplyGuardrail) and the Lambda tools are the deployed AWS resources. Latency and tokens are not Bedrock figures and there is no cost.

| | qwen3-8b | qwen3-14b |
| --- | --- | --- |
| Model | local/Qwen3-8B | local/Qwen3-14B |
| Questions passed | 15/30 | 18/30 |
| Knowledge base questions | 9/21 | 9/21 |
| Tool questions | 6/6 | 6/6 |
| Unanswerable question handled | 0/3 | 3/3 |
| Errors | 0 | 0 |
| Median latency (s) | 3.34 | 3.84 |
| Slowest (s) | 16.87 | 21.35 |
| Mean input tokens | 1916 | 1739 |
| Mean output tokens | 71 | 63 |
| Cost per question (USD) | None | None |
| Cost per 1,000 questions (USD) | None | None |

## Per question

| Model | Id | Kind | Pass | Latency (s) | In | Out | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen3-8b | q01 | kb | no | 16.87 | 2205 | 159 | Results are typically released on the following dates after the mid-year exam period:  - **16 February 2027** (for the mid-year exam period  |
| qwen3-8b | q01 | kb | no | 7.55 | 2205 | 159 | Results are typically released on the following dates after the mid-year exam period:  - **16 February 2027** (for the mid-year exam period  |
| qwen3-8b | q01 | kb | no | 6.82 | 2205 | 159 | Results are typically released on the following dates after the mid-year exam period:  - **16 February 2027** (for the mid-year exam period  |
| qwen3-8b | q02 | kb | no | 3.07 | 2215 | 62 | The centrally scheduled exam period in November is from **31 May to 11 June**. For more details, you can refer to the academic calendar. |
| qwen3-8b | q02 | kb | no | 3.16 | 2215 | 62 | The centrally scheduled exam period in November is from **31 May to 11 June**. For more details, you can refer to the academic calendar. |
| qwen3-8b | q02 | kb | no | 4.48 | 2215 | 62 | The centrally scheduled exam period in November is from **31 May to 11 June**. For more details, you can refer to the academic calendar. |
| qwen3-8b | q03 | kb | no | 4.43 | 2383 | 67 | The last date to apply for alternative arrangements for the mid-year exams is 22 January 2027. For more information, contact Services Access |
| qwen3-8b | q03 | kb | no | 3.14 | 2383 | 67 | The last date to apply for alternative arrangements for the mid-year exams is 22 January 2027. For more information, contact Services Access |
| qwen3-8b | q03 | kb | no | 2.68 | 2383 | 67 | The last date to apply for alternative arrangements for the mid-year exams is 22 January 2027. For more information, contact Services Access |
| qwen3-8b | q04 | kb | yes | 4.21 | 2226 | 106 | To pay your fees online, you can use the **Curtin ePay** portal. Visit the [Curtin ePay page](https://www.curtin.edu.au/students/essentials/ |
| qwen3-8b | q04 | kb | yes | 6.46 | 2226 | 106 | To pay your fees online, you can use the **Curtin ePay** portal. Visit the [Curtin ePay page](https://www.curtin.edu.au/students/essentials/ |
| qwen3-8b | q04 | kb | yes | 6.42 | 2226 | 106 | To pay your fees online, you can use the **Curtin ePay** portal. Visit the [Curtin ePay page](https://www.curtin.edu.au/students/essentials/ |
| qwen3-8b | q05 | kb | no | 1.88 | 590 | 37 | I don't have access to real-time world university rankings. For the most accurate and up-to-date information, please visit Curtin University |
| qwen3-8b | q05 | kb | no | 1.6 | 590 | 37 | I don't have access to real-time world university rankings. For the most accurate and up-to-date information, please visit Curtin University |
| qwen3-8b | q05 | kb | no | 1.51 | 590 | 37 | I don't have access to real-time world university rankings. For the most accurate and up-to-date information, please visit Curtin University |
| qwen3-8b | q06 | kb | yes | 3.43 | 2321 | 44 | The John Curtin Prime Ministerial Library is open by appointment only. |
| qwen3-8b | q06 | kb | yes | 3.37 | 2321 | 44 | The John Curtin Prime Ministerial Library is open by appointment only. |
| qwen3-8b | q06 | kb | yes | 3.08 | 2321 | 44 | The John Curtin Prime Ministerial Library is open by appointment only. |
| qwen3-8b | q07 | kb | yes | 3.87 | 2235 | 66 | The phone number for the Safer Community Team is 08 9266 4444. You can call them for concerns about safety, security, or wellbeing. |
| qwen3-8b | q07 | kb | yes | 3.0 | 2235 | 66 | The phone number for the Safer Community Team is 08 9266 4444. You can call them for concerns about safety, security, or wellbeing. |
| qwen3-8b | q07 | kb | yes | 4.0 | 2235 | 66 | The phone number for the Safer Community Team is 08 9266 4444. You can call them for concerns about safety, security, or wellbeing. |
| qwen3-8b | q08 | tool | yes | 4.45 | 1315 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q08 | tool | yes | 3.85 | 1315 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q08 | tool | yes | 2.47 | 1315 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q09 | tool | yes | 2.1 | 1327 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q09 | tool | yes | 2.61 | 1327 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q09 | tool | yes | 3.31 | 1327 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q10 | abstain | no | 2.43 | 2342 | 56 | The search results do not provide information about parking costs per hour at the Bentley campus. For more details, please contact student s |
| qwen3-8b | q10 | abstain | no | 4.57 | 2342 | 56 | The search results do not provide information about parking costs per hour at the Bentley campus. For more details, please contact student s |
| qwen3-8b | q10 | abstain | no | 2.96 | 2342 | 56 | The search results do not provide information about parking costs per hour at the Bentley campus. For more details, please contact student s |
| qwen3-14b | q01 | kb | no | 21.35 | 2194 | 81 | Results are typically released 30 days after the mid-year exam period. For example, if the mid-year exam period is in June, results are usua |
| qwen3-14b | q01 | kb | no | 4.85 | 2194 | 81 | Results are typically released 30 days after the mid-year exam period. For example, if the mid-year exam period is in June, results are usua |
| qwen3-14b | q01 | kb | no | 3.87 | 2194 | 81 | Results are typically released 30 days after the mid-year exam period. For example, if the mid-year exam period is in June, results are usua |
| qwen3-14b | q02 | kb | no | 3.37 | 2215 | 63 | The centrally scheduled exam period in November is not listed in the provided information. You may want to check the academic calendar for m |
| qwen3-14b | q02 | kb | no | 3.03 | 2215 | 63 | The centrally scheduled exam period in November is not listed in the provided information. You may want to check the academic calendar for m |
| qwen3-14b | q02 | kb | no | 4.51 | 2215 | 63 | The centrally scheduled exam period in November is not listed in the provided information. You may want to check the academic calendar for m |
| qwen3-14b | q03 | kb | no | 3.17 | 2384 | 64 | The last date to apply for alternative exam arrangements for the mid-year exams is **18 June**. For more information, contact AccessAbility  |
| qwen3-14b | q03 | kb | no | 3.53 | 2384 | 64 | The last date to apply for alternative exam arrangements for the mid-year exams is **18 June**. For more information, contact AccessAbility  |
| qwen3-14b | q03 | kb | no | 3.85 | 2384 | 64 | The last date to apply for alternative exam arrangements for the mid-year exams is **18 June**. For more information, contact AccessAbility  |
| qwen3-14b | q04 | kb | yes | 5.4 | 2226 | 79 | You can pay your fees online using Curtin ePay, which is a quick and secure online payment portal. To access it, visit the [Curtin ePay page |
| qwen3-14b | q04 | kb | yes | 4.85 | 2226 | 79 | You can pay your fees online using Curtin ePay, which is a quick and secure online payment portal. To access it, visit the [Curtin ePay page |
| qwen3-14b | q04 | kb | yes | 3.65 | 2226 | 79 | You can pay your fees online using Curtin ePay, which is a quick and secure online payment portal. To access it, visit the [Curtin ePay page |
| qwen3-14b | q05 | kb | no | 2.19 | 590 | 40 | I don't have specific information about Curtin University's world rankings. For the most accurate and up-to-date information, I recommend ch |
| qwen3-14b | q05 | kb | no | 2.64 | 590 | 40 | I don't have specific information about Curtin University's world rankings. For the most accurate and up-to-date information, I recommend ch |
| qwen3-14b | q05 | kb | no | 2.79 | 590 | 40 | I don't have specific information about Curtin University's world rankings. For the most accurate and up-to-date information, I recommend ch |
| qwen3-14b | q06 | kb | yes | 5.04 | 2321 | 71 | The John Curtin Prime Ministerial Library is open by appointment only. For more information, you can visit the [Curtin University Library we |
| qwen3-14b | q06 | kb | yes | 4.93 | 2321 | 71 | The John Curtin Prime Ministerial Library is open by appointment only. For more information, you can visit the [Curtin University Library we |
| qwen3-14b | q06 | kb | yes | 3.83 | 2321 | 71 | The John Curtin Prime Ministerial Library is open by appointment only. For more information, you can visit the [Curtin University Library we |
| qwen3-14b | q07 | kb | yes | 3.93 | 2235 | 85 | The phone number for the Safer Community Team is **08 9266 4444**. You can call this number if you have concerns about the safety, security, |
| qwen3-14b | q07 | kb | yes | 5.43 | 2235 | 85 | The phone number for the Safer Community Team is **08 9266 4444**. You can call this number if you have concerns about the safety, security, |
| qwen3-14b | q07 | kb | yes | 3.88 | 2235 | 85 | The phone number for the Safer Community Team is **08 9266 4444**. You can call this number if you have concerns about the safety, security, |
| qwen3-14b | q08 | tool | yes | 3.07 | 1315 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q08 | tool | yes | 4.7 | 1315 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q08 | tool | yes | 4.76 | 1315 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q09 | tool | yes | 4.02 | 1327 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q09 | tool | yes | 3.12 | 1327 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q09 | tool | yes | 3.04 | 1327 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q10 | abstain | yes | 1.56 | 587 | 22 | I don't have information on parking costs at the Bentley campus. You may contact student services for details. |
| qwen3-14b | q10 | abstain | yes | 1.23 | 587 | 22 | I don't have information on parking costs at the Bentley campus. You may contact student services for details. |
| qwen3-14b | q10 | abstain | yes | 1.21 | 587 | 22 | I don't have information on parking costs at the Bentley campus. You may contact student services for details. |
