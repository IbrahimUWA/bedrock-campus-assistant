# Model comparison

10 questions, 3 run(s) each, through the full agent loop (guardrail, knowledge base, tools).
**Local stand-in run.** The models are open models on one workstation GPU and retrieval is local, because the AWS account's Bedrock model quota was still 0. The guardrail (ApplyGuardrail) and the Lambda tools are the deployed AWS resources. Latency and tokens are not Bedrock figures and there is no cost.

| | qwen3-8b | qwen3-14b |
| --- | --- | --- |
| Model | local/Qwen3-8B | local/Qwen3-14B |
| Questions passed | 24/30 | 21/30 |
| Knowledge base questions | 15/21 | 12/21 |
| Tool questions | 6/6 | 6/6 |
| Unanswerable question handled | 3/3 | 3/3 |
| Errors | 0 | 0 |
| Median latency (s) | 2.79 | 3.35 |
| Slowest (s) | 15.68 | 19.76 |
| Mean input tokens | 1688 | 1419 |
| Mean output tokens | 71 | 64 |
| Cost per question (USD) | None | None |
| Cost per 1,000 questions (USD) | None | None |

## Per question

| Model | Id | Kind | Pass | Latency (s) | In | Out | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen3-8b | q01 | kb | no | 15.68 | 1826 | 174 | Results are typically released on the following dates after the mid-year exam period:  - **30 December 2026** for the Open Unis Study Period |
| qwen3-8b | q01 | kb | no | 6.62 | 1826 | 174 | Results are typically released on the following dates after the mid-year exam period:  - **30 December 2026** for the Open Unis Study Period |
| qwen3-8b | q01 | kb | no | 6.62 | 1826 | 174 | Results are typically released on the following dates after the mid-year exam period:  - **30 December 2026** for the Open Unis Study Period |
| qwen3-8b | q02 | kb | no | 2.27 | 1836 | 48 | The centrally scheduled exam period in November is from 30 November to 4 December. |
| qwen3-8b | q02 | kb | no | 2.28 | 1836 | 48 | The centrally scheduled exam period in November is from 30 November to 4 December. |
| qwen3-8b | q02 | kb | no | 2.27 | 1836 | 48 | The centrally scheduled exam period in November is from 30 November to 4 December. |
| qwen3-8b | q03 | kb | yes | 2.87 | 2116 | 63 | The last date to apply for alternative exam arrangements in Semester 1 2027 is 16 April. |
| qwen3-8b | q03 | kb | yes | 2.86 | 2116 | 63 | The last date to apply for alternative exam arrangements in Semester 1 2027 is 16 April. |
| qwen3-8b | q03 | kb | yes | 2.87 | 2116 | 63 | The last date to apply for alternative exam arrangements in Semester 1 2027 is 16 April. |
| qwen3-8b | q04 | kb | yes | 3.37 | 1511 | 72 | You can pay your fees online using the Curtin ePay portal. Visit the [Curtin ePay page](https://www.curtin.edu.au/students/essentials/fees/) |
| qwen3-8b | q04 | kb | yes | 3.14 | 1511 | 72 | You can pay your fees online using the Curtin ePay portal. Visit the [Curtin ePay page](https://www.curtin.edu.au/students/essentials/fees/) |
| qwen3-8b | q04 | kb | yes | 2.99 | 1511 | 72 | You can pay your fees online using the Curtin ePay portal. Visit the [Curtin ePay page](https://www.curtin.edu.au/students/essentials/fees/) |
| qwen3-8b | q05 | kb | yes | 2.76 | 1551 | 65 | Curtin University is ranked in the top one per cent of universities worldwide according to the Academic Ranking of World Universities (ARWU) |
| qwen3-8b | q05 | kb | yes | 2.78 | 1551 | 65 | Curtin University is ranked in the top one per cent of universities worldwide according to the Academic Ranking of World Universities (ARWU) |
| qwen3-8b | q05 | kb | yes | 2.9 | 1551 | 65 | Curtin University is ranked in the top one per cent of universities worldwide according to the Academic Ranking of World Universities (ARWU) |
| qwen3-8b | q06 | kb | yes | 2.51 | 1447 | 58 | The John Curtin Prime Ministerial Library is open by appointment only. You can find out more details on the Curtin University library websit |
| qwen3-8b | q06 | kb | yes | 2.49 | 1447 | 58 | The John Curtin Prime Ministerial Library is open by appointment only. You can find out more details on the Curtin University library websit |
| qwen3-8b | q06 | kb | yes | 2.64 | 1447 | 58 | The John Curtin Prime Ministerial Library is open by appointment only. You can find out more details on the Curtin University library websit |
| qwen3-8b | q07 | kb | yes | 2.79 | 1601 | 64 | The phone number for the Safer Community Team is 08 9266 4444. You can call them for assistance with safety or security concerns. |
| qwen3-8b | q07 | kb | yes | 2.73 | 1601 | 64 | The phone number for the Safer Community Team is 08 9266 4444. You can call them for assistance with safety or security concerns. |
| qwen3-8b | q07 | kb | yes | 2.82 | 1601 | 64 | The phone number for the Safer Community Team is 08 9266 4444. You can call them for assistance with safety or security concerns. |
| qwen3-8b | q08 | tool | yes | 3.44 | 1329 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q08 | tool | yes | 2.9 | 1329 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q08 | tool | yes | 2.79 | 1329 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q09 | tool | yes | 2.34 | 1341 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q09 | tool | yes | 2.45 | 1341 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q09 | tool | yes | 2.39 | 1341 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q10 | abstain | yes | 2.67 | 2319 | 56 | The search results do not provide information about parking costs per hour at the Bentley campus. For more details, please contact student s |
| qwen3-8b | q10 | abstain | yes | 2.7 | 2319 | 56 | The search results do not provide information about parking costs per hour at the Bentley campus. For more details, please contact student s |
| qwen3-8b | q10 | abstain | yes | 2.61 | 2319 | 56 | The search results do not provide information about parking costs per hour at the Bentley campus. For more details, please contact student s |
| qwen3-14b | q01 | kb | no | 19.76 | 1826 | 92 | Results are typically released approximately one month after the centrally scheduled exam period. For example, if exams are held in June, re |
| qwen3-14b | q01 | kb | no | 4.52 | 1826 | 92 | Results are typically released approximately one month after the centrally scheduled exam period. For example, if exams are held in June, re |
| qwen3-14b | q01 | kb | no | 4.48 | 1826 | 92 | Results are typically released approximately one month after the centrally scheduled exam period. For example, if exams are held in June, re |
| qwen3-14b | q02 | kb | no | 3.23 | 1836 | 59 | The centrally scheduled exam period in November is from **30 November to 4 December**. You can find more details on the academic calendar. |
| qwen3-14b | q02 | kb | no | 3.12 | 1836 | 59 | The centrally scheduled exam period in November is from **30 November to 4 December**. You can find more details on the academic calendar. |
| qwen3-14b | q02 | kb | no | 3.22 | 1836 | 59 | The centrally scheduled exam period in November is from **30 November to 4 December**. You can find more details on the academic calendar. |
| qwen3-14b | q03 | kb | yes | 4.25 | 2115 | 72 | The last date to apply for alternative exam arrangements in Semester 1 2027 is **16 April**. For more information, contact AccessAbility Ser |
| qwen3-14b | q03 | kb | yes | 3.81 | 2115 | 72 | The last date to apply for alternative exam arrangements in Semester 1 2027 is **16 April**. For more information, contact AccessAbility Ser |
| qwen3-14b | q03 | kb | yes | 3.8 | 2115 | 72 | The last date to apply for alternative exam arrangements in Semester 1 2027 is **16 April**. For more information, contact AccessAbility Ser |
| qwen3-14b | q04 | kb | yes | 4.49 | 1505 | 95 | You can pay your fees online using Curtin ePay, which is a quick and secure payment portal. To access it, go to the [Curtin ePay page](https |
| qwen3-14b | q04 | kb | yes | 4.52 | 1505 | 95 | You can pay your fees online using Curtin ePay, which is a quick and secure payment portal. To access it, go to the [Curtin ePay page](https |
| qwen3-14b | q04 | kb | yes | 4.75 | 1505 | 95 | You can pay your fees online using Curtin ePay, which is a quick and secure payment portal. To access it, go to the [Curtin ePay page](https |
| qwen3-14b | q05 | kb | no | 1.99 | 597 | 37 | Curtin University is ranked in the top one per cent of universities globally by the QS World University Rankings. For more details, you can  |
| qwen3-14b | q05 | kb | no | 1.96 | 597 | 37 | Curtin University is ranked in the top one per cent of universities globally by the QS World University Rankings. For more details, you can  |
| qwen3-14b | q05 | kb | no | 2.07 | 597 | 37 | Curtin University is ranked in the top one per cent of universities globally by the QS World University Rankings. For more details, you can  |
| qwen3-14b | q06 | kb | yes | 2.92 | 1447 | 56 | The John Curtin Prime Ministerial Library is open by appointment only. For more information, you can visit the library's website. |
| qwen3-14b | q06 | kb | yes | 2.91 | 1447 | 56 | The John Curtin Prime Ministerial Library is open by appointment only. For more information, you can visit the library's website. |
| qwen3-14b | q06 | kb | yes | 2.92 | 1447 | 56 | The John Curtin Prime Ministerial Library is open by appointment only. For more information, you can visit the library's website. |
| qwen3-14b | q07 | kb | yes | 4.18 | 1601 | 86 | The phone number for the Safer Community Team is **08 9266 4444**. You can call this number if you have concerns about the safety, security, |
| qwen3-14b | q07 | kb | yes | 4.29 | 1601 | 86 | The phone number for the Safer Community Team is **08 9266 4444**. You can call this number if you have concerns about the safety, security, |
| qwen3-14b | q07 | kb | yes | 4.15 | 1601 | 86 | The phone number for the Safer Community Team is **08 9266 4444**. You can call this number if you have concerns about the safety, security, |
| qwen3-14b | q08 | tool | yes | 3.47 | 1329 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q08 | tool | yes | 3.54 | 1329 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q08 | tool | yes | 3.49 | 1329 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q09 | tool | yes | 2.91 | 1341 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q09 | tool | yes | 2.92 | 1341 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q09 | tool | yes | 3.11 | 1341 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q10 | abstain | yes | 1.33 | 594 | 22 | I don't have information on parking costs at the Bentley campus. You may contact student services for assistance. |
| qwen3-14b | q10 | abstain | yes | 1.38 | 594 | 22 | I don't have information on parking costs at the Bentley campus. You may contact student services for assistance. |
| qwen3-14b | q10 | abstain | yes | 1.48 | 594 | 22 | I don't have information on parking costs at the Bentley campus. You may contact student services for assistance. |
