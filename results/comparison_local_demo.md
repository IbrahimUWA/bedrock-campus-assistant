# Model comparison

10 questions, 3 run(s) each, through the full agent loop (guardrail, knowledge base, tools).
**Local stand-in run.** The models are open models on one workstation GPU and retrieval is local, because the AWS account's Bedrock model quota was still 0. The guardrail (ApplyGuardrail) and the Lambda tools are the deployed AWS resources. Latency and tokens are not Bedrock figures and there is no cost.

| | qwen3-8b | qwen3-14b |
| --- | --- | --- |
| Model | local/Qwen3-8B | local/Qwen3-14B |
| Questions passed | 27/30 | 24/30 |
| Knowledge base questions | 18/21 | 15/21 |
| Tool questions | 6/6 | 6/6 |
| Unanswerable question handled | 3/3 | 3/3 |
| Errors | 0 | 0 |
| Median latency (s) | 4.33 | 6.19 |
| Slowest (s) | 16.25 | 44.55 |
| Mean input tokens | 1689 | 1471 |
| Mean output tokens | 70 | 77 |
| Cost per question (USD) | None | None |
| Cost per 1,000 questions (USD) | None | None |

## Per question

| Model | Id | Kind | Pass | Latency (s) | In | Out | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen3-8b | q01 | kb | no | 16.25 | 1861 | 49 | Results are released on Monday 7 December 2026 after the mid-year exam period. |
| qwen3-8b | q01 | kb | no | 4.32 | 1861 | 49 | Results are released on Monday 7 December 2026 after the mid-year exam period. |
| qwen3-8b | q01 | kb | no | 4.02 | 1861 | 49 | Results are released on Monday 7 December 2026 after the mid-year exam period. |
| qwen3-8b | q02 | kb | yes | 6.57 | 1935 | 93 | The centrally scheduled exam period in November for Semester 2 2026 is from Monday 9 November to Friday 20 November 2026. For Semester 2 202 |
| qwen3-8b | q02 | kb | yes | 5.33 | 1935 | 93 | The centrally scheduled exam period in November for Semester 2 2026 is from Monday 9 November to Friday 20 November 2026. For Semester 2 202 |
| qwen3-8b | q02 | kb | yes | 6.15 | 1935 | 93 | The centrally scheduled exam period in November for Semester 2 2026 is from Monday 9 November to Friday 20 November 2026. For Semester 2 202 |
| qwen3-8b | q03 | kb | yes | 4.02 | 1999 | 69 | The last date to apply for alternative exam arrangements in Semester 1 2027 is Friday 23 April 2027. |
| qwen3-8b | q03 | kb | yes | 5.14 | 1999 | 69 | The last date to apply for alternative exam arrangements in Semester 1 2027 is Friday 23 April 2027. |
| qwen3-8b | q03 | kb | yes | 6.06 | 1999 | 69 | The last date to apply for alternative exam arrangements in Semester 1 2027 is Friday 23 April 2027. |
| qwen3-8b | q04 | kb | yes | 8.97 | 1635 | 125 | You can pay your fees online using PayPoint, the university's payment page, with a credit or debit card. Card payments have a surcharge of 0 |
| qwen3-8b | q04 | kb | yes | 8.54 | 1635 | 125 | You can pay your fees online using PayPoint, the university's payment page, with a credit or debit card. Card payments have a surcharge of 0 |
| qwen3-8b | q04 | kb | yes | 8.1 | 1635 | 125 | You can pay your fees online using PayPoint, the university's payment page, with a credit or debit card. Card payments have a surcharge of 0 |
| qwen3-8b | q05 | kb | yes | 5.22 | 1674 | 68 | Wattlebrook University has its highest world ranking in the subject of mineral and mining engineering, where it is ranked 31st globally acco |
| qwen3-8b | q05 | kb | yes | 4.33 | 1674 | 68 | Wattlebrook University has its highest world ranking in the subject of mineral and mining engineering, where it is ranked 31st globally acco |
| qwen3-8b | q05 | kb | yes | 4.12 | 1674 | 68 | Wattlebrook University has its highest world ranking in the subject of mineral and mining engineering, where it is ranked 31st globally acco |
| qwen3-8b | q06 | kb | yes | 3.89 | 1748 | 60 | The Harcourt Special Collections Library at the Riverbend campus is open by appointment only. You need to book at least two working days in  |
| qwen3-8b | q06 | kb | yes | 4.09 | 1748 | 60 | The Harcourt Special Collections Library at the Riverbend campus is open by appointment only. You need to book at least two working days in  |
| qwen3-8b | q06 | kb | yes | 3.99 | 1748 | 60 | The Harcourt Special Collections Library at the Riverbend campus is open by appointment only. You need to book at least two working days in  |
| qwen3-8b | q07 | kb | yes | 4.79 | 1686 | 64 | The phone number for the Campus Safety Team is (08) 5550 0142. You can contact them at any time, day or night. |
| qwen3-8b | q07 | kb | yes | 5.84 | 1686 | 64 | The phone number for the Campus Safety Team is (08) 5550 0142. You can contact them at any time, day or night. |
| qwen3-8b | q07 | kb | yes | 4.03 | 1686 | 64 | The phone number for the Campus Safety Team is (08) 5550 0142. You can contact them at any time, day or night. |
| qwen3-8b | q08 | tool | yes | 4.87 | 1329 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q08 | tool | yes | 3.93 | 1329 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q08 | tool | yes | 5.22 | 1329 | 63 | The assessments for unit DEMO2002 are: - Programming assignment (30%) - Group project (30%) - Final exam (40%) |
| qwen3-8b | q09 | tool | yes | 4.05 | 1341 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q09 | tool | yes | 3.09 | 1341 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q09 | tool | yes | 3.55 | 1341 | 50 | You need to have completed DEMO2002 before you can take DEMO3003. |
| qwen3-8b | q10 | abstain | yes | 4.07 | 1679 | 57 | The search results do not provide information about parking costs at the Riverbend campus. For more details, please contact student services |
| qwen3-8b | q10 | abstain | yes | 4.27 | 1679 | 57 | The search results do not provide information about parking costs at the Riverbend campus. For more details, please contact student services |
| qwen3-8b | q10 | abstain | yes | 3.72 | 1679 | 57 | The search results do not provide information about parking costs at the Riverbend campus. For more details, please contact student services |
| qwen3-14b | q01 | kb | no | 44.55 | 1861 | 136 | Results are typically released one week after the centrally scheduled exam period. For example, in Semester 2 2026, results were released on |
| qwen3-14b | q01 | kb | no | 10.32 | 1861 | 136 | Results are typically released one week after the centrally scheduled exam period. For example, in Semester 2 2026, results were released on |
| qwen3-14b | q01 | kb | no | 11.84 | 1861 | 136 | Results are typically released one week after the centrally scheduled exam period. For example, in Semester 2 2026, results were released on |
| qwen3-14b | q02 | kb | yes | 8.1 | 1935 | 103 | The centrally scheduled exam period in November is from Monday 8 November to Friday 19 November for Semester 2 2027. For other years or seme |
| qwen3-14b | q02 | kb | yes | 7.82 | 1935 | 103 | The centrally scheduled exam period in November is from Monday 8 November to Friday 19 November for Semester 2 2027. For other years or seme |
| qwen3-14b | q02 | kb | yes | 7.94 | 1935 | 103 | The centrally scheduled exam period in November is from Monday 8 November to Friday 19 November for Semester 2 2027. For other years or seme |
| qwen3-14b | q03 | kb | yes | 7.42 | 1998 | 98 | The last date to apply for alternative exam arrangements in Semester 1 2027 is **Friday 23 April 2027**.   You can find more information abo |
| qwen3-14b | q03 | kb | yes | 8.87 | 1998 | 98 | The last date to apply for alternative exam arrangements in Semester 1 2027 is **Friday 23 April 2027**.   You can find more information abo |
| qwen3-14b | q03 | kb | yes | 8.3 | 1998 | 98 | The last date to apply for alternative exam arrangements in Semester 1 2027 is **Friday 23 April 2027**.   You can find more information abo |
| qwen3-14b | q04 | kb | yes | 11.68 | 1633 | 127 | You can pay your fees online using PayPoint, the university's payment page, with a credit or debit card. There is a surcharge of 0.9 per cen |
| qwen3-14b | q04 | kb | yes | 11.63 | 1633 | 127 | You can pay your fees online using PayPoint, the university's payment page, with a credit or debit card. There is a surcharge of 0.9 per cen |
| qwen3-14b | q04 | kb | yes | 11.01 | 1633 | 127 | You can pay your fees online using PayPoint, the university's payment page, with a credit or debit card. There is a surcharge of 0.9 per cen |
| qwen3-14b | q05 | kb | yes | 6.04 | 1674 | 67 | Wattlebrook University has its highest world ranking in **mineral and mining engineering**, where it is ranked 31st globally according to th |
| qwen3-14b | q05 | kb | yes | 6.2 | 1674 | 67 | Wattlebrook University has its highest world ranking in **mineral and mining engineering**, where it is ranked 31st globally according to th |
| qwen3-14b | q05 | kb | yes | 5.55 | 1674 | 67 | Wattlebrook University has its highest world ranking in **mineral and mining engineering**, where it is ranked 31st globally according to th |
| qwen3-14b | q06 | kb | yes | 5.63 | 1748 | 69 | The Harcourt Special Collections Library, located on the Riverbend campus in Building 200, is open by appointment only. You need to book at  |
| qwen3-14b | q06 | kb | yes | 5.51 | 1748 | 69 | The Harcourt Special Collections Library, located on the Riverbend campus in Building 200, is open by appointment only. You need to book at  |
| qwen3-14b | q06 | kb | yes | 5.4 | 1748 | 69 | The Harcourt Special Collections Library, located on the Riverbend campus in Building 200, is open by appointment only. You need to book at  |
| qwen3-14b | q07 | kb | no | 2.54 | 595 | 22 | I don't have this information. Please check the university's official website or contact Student Services for assistance. |
| qwen3-14b | q07 | kb | no | 2.37 | 595 | 22 | I don't have this information. Please check the university's official website or contact Student Services for assistance. |
| qwen3-14b | q07 | kb | no | 2.38 | 595 | 22 | I don't have this information. Please check the university's official website or contact Student Services for assistance. |
| qwen3-14b | q08 | tool | yes | 6.87 | 1329 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q08 | tool | yes | 6.67 | 1329 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q08 | tool | yes | 6.18 | 1329 | 70 | The assessments for unit DEMO2002 (Machine Learning Foundations) are as follows:  - Programming assignment (30%) - Group project (30%) - Fin |
| qwen3-14b | q09 | tool | yes | 5.37 | 1341 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q09 | tool | yes | 5.18 | 1341 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q09 | tool | yes | 5.2 | 1341 | 56 | Before you can take DEMO3003 (Generative AI Engineering), you need to have completed DEMO2002. |
| qwen3-14b | q10 | abstain | yes | 2.37 | 596 | 26 | I don't have information on parking costs at the Riverbend campus. You may want to contact student services for details. |
| qwen3-14b | q10 | abstain | yes | 2.15 | 596 | 26 | I don't have information on parking costs at the Riverbend campus. You may want to contact student services for details. |
| qwen3-14b | q10 | abstain | yes | 2.47 | 596 | 26 | I don't have information on parking costs at the Riverbend campus. You may want to contact student services for details. |
