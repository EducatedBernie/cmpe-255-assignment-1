# Prompts and Agent-Assisted Process

## Disclosure

This project was developed with OpenAI Codex as an agentic coding assistant. The assistant helped read the assignment sources, design the experiment, write tests and code, run the analysis, inspect generated figures, and draft the documentation. The author remains responsible for reviewing, understanding, recording, and submitting the work.

This is a process record, not a fabricated verbatim transcript. The original Codex task can be shared separately through the Codex app if the instructor requires the complete conversation.

## Source prompts reviewed

- Instructor assignment: [CMPE 255 Assignment 1, Fall 2026](https://docs.google.com/document/d/1NMl64CxIyq3BznMgAFotEsp0fHpEkQe4b7Oi98SEjaA/edit?tab=t.0)
- Instructor worked example: Adult Income analysis organized around CRISP-DM
- Reference prompt catalog: [`dlmastery/data_science_examples/PROMPTS.md`](https://github.com/dlmastery/data_science_examples/blob/main/PROMPTS.md)

The reference catalog currently contains 15 numbered examples. This submission maps six of them to focused, reproducible experiments rather than copying their full-stack interfaces wholesale.

## Adapted master prompt

> Build a reproducible, end-to-end CRISP-DM project on the Adult/Census Income dataset. Include data understanding, validation, cleaning, leakage-safe preprocessing, a dummy baseline, logistic regression, random forest, appropriate classification metrics, clustering, anomaly detection, interpretable visual evidence, and a responsible-use audit. Use fixed random seeds, test the non-trivial data logic, generate all artifacts from one command, and explain weak or negative findings instead of overstating them.

## Reference-theme adaptations

1. **Project 03 — Customer segmentation:** adapted clustering to Adult numerical attributes with MiniBatch K-means and a sampled silhouette score.
2. **Project 04 — Associative pattern mining:** treated Adult categorical values as baskets and mined support, confidence, and lift rules.
3. **Project 06 — Anomaly detection:** used Isolation Forest and documented that the selected contamination rate controls the cutoff.
4. **Project 07 — AutoML:** automatically compared four scikit-learn candidates using identical preprocessing and three-fold cross-validation.
5. **Project 11 — Enterprise audit:** checked leakage, deterministic seeds, tests, group metrics, data age, and deployment limitations.
6. **Project 12 — Time-series forecasting:** compared seasonal-naive and Ridge forecasts on a chronological AirPassengers holdout.

## Agent journey

1. Read the live assignment Google Doc and its linked 8,000-line worked transcript.
2. Read the public reference repository's README and prompt catalog.
3. Selected Adult Income for continuity with the instructor example and verified both its UCI source and Kaggle publication.
4. Wrote tests before production code for file loading, schema rejection, cleaning, determinism, and artifact output.
5. Ran the test once to observe the intended missing-module failure, then implemented the analysis.
6. Ran the pipeline on all 48,842 records and inspected every generated figure.
7. Wrote the conclusions from the measured output, including weak clustering and group-level limitations.
8. Added three more experiments after confirming the emailed minimum was six projects.
9. Wrote failing tests before implementing association mining, AutoML-style benchmarking, and forecasting.
10. Generated and visually inspected the three new evidence sets, then organized all six under `replications/`.

## Useful follow-up prompts

- “Explain why the dummy model's 76% accuracy is misleading.”
- “Compare random forest and logistic regression when false negatives are costly.”
- “Audit this pipeline for preprocessing leakage.”
- “Explain why a low silhouette score should change the clustering conclusion.”
- “Identify which claims are associations rather than causal conclusions.”

## Original Assignment and Conversation Log

The following text was supplied by the author and is preserved verbatim, including timestamps, typos, and historical status messages.

<details>
<summary>View the supplied assignment and Codex log</summary>

~~~text
Assignment details:
Part 1:
https://docs.google.com/document/d/1NMl64CxIyq3BznMgAFotEsp0fHpEkQe4b7Oi98SEjaA/edit?tab=t.0Links to an external site.
You can use any coding assistant or chatbot which supports agentic coding (like chatgpt or codex)
Two deliverables:
Make sure you have all artifacts captured in a nice README.md file in your github directory - make sure you organize it as assignment 1
Also upload any other artifacts in the directory of github
Make sure you give public view permission for the github 
Also do a youtube video highlighting the end2end journey and read and understand and provide a paraphrase of the output 
make sure you upload youtube video and provide the link to it in README.md
Part 2:
Replicate the data science experiments i did in your favorite coding assistant - i provided the prompts in the repository
https://github.com/dlmastery/data\_science\_examplesLinks to an external site.
make sure you publish them in github repo and walk thru these in a youtube video and upload and link to README.md
Note: use your creativity and not need to do exactly like above - improvise if possible. the minimum bar is above 
thanks
vijay eranti
Are you able to read these files just fine





Show more

11:04 AM






Worked for 2m 10s



Yes—I verified both:
- The Google Doc is publicly readable. I can read its assignment text; embedded screenshot content may require separate visual inspection.
- The GitHub repository is public and accessible. I can read its code, README.md, PROMPTS.md, and all 14 project directories.
The extra “Links to an external site” text in the pasted URLs is just Canvas formatting; I normalized the links successfully.

Google DocGoogle DocsOpen in DiaOpen in


Give feedback



11:06 AM








Go ahead and begin doing the tasks?







11:07 AM






Worked for 21m 34s



The repo-local assignment is built, verified, and committed on codex/assignment-1 at commit 8e52adf.
- Main deliverable: [README.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/README.md)
- Results and paraphrase: [RESULTS.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/docs/RESULTS.md)
- Recording script: [VIDEO_SCRIPT.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/docs/VIDEO_SCRIPT.md)
- Medium draft: [MEDIUM_ARTICLE_DRAFT.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/docs/MEDIUM_ARTICLE_DRAFT.md)
- Tests: 4/4 passing
- Full dataset: 48,842 records from UCI Adult, also published on Kaggle
- Best model: random forest, 83.82% accuracy and 0.917 ROC-AUC
I have not published it because the existing local Git repository contains an unrelated Ansible document. May I create a clean public repository named EducatedBernie/cmpe-255-assignment-1 containing only these assignment files and push it now?


11:28 AM








Can u just move all the work into a sub direcotry and make that hte git repo instead







11:33 AM






Worked for 4m 14s



Moved everything into the standalone repo:
[cmpe-255-assignment-1/README.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1/README.md)
- New repo: main, commit f9aa4f9
- Tests: 4/4 passing; full pipeline verified
- Outer repository is clean; unrelated Ansible work remains untouched


11:38 AM








What do u want me to tell the other agent so he doesn't interfere with u







12:21 PM






Worked for 11s







Send this:
Do not modify, move, delete, format, or run Git commands inside /Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1. Also do not switch/reset/clean branches in the parent SJSU Assignments repository. Work in a separate directory or Git worktree, and ask me before touching those paths.



12:22 PM








okay are we done? What's the full thing i should submit







12:43 PM






Worked for 1m 12s



The code and local artifacts are done and verified—4/4 tests pass. The assignment is not fully submitted yet because the repository, video, and article are not published.
Submit these three links:
1. Public GitHub repository
   - Entire contents of [cmpe-255-assignment-1](/Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1)
   - Central README: [README.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1/README.md)
   - It already contains Part 1, Part 2, code, tests, results, figures, paraphrased output, and the process record.
2. YouTube walkthrough
   - Record using [VIDEO_SCRIPT.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1/docs/VIDEO_SCRIPT.md)
   - Upload as Public or Unlisted.
   - Add its URL to the top of README.md.
3. Medium article
   - Personalize and publish [MEDIUM_ARTICLE_DRAFT.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1/docs/MEDIUM_ARTICLE_DRAFT.md)
   - Add your name, course, GitHub URL, and YouTube URL.
   - Add the final Medium URL to the README.
Also export/share the Codex conversation if the instructor enforces the linked document’s transcript requirement. [PROMPTS_AND_PROCESS.md](/Users/bernie/Documents/ChatGPT/SJSU Assignments/cmpe-255-assignment-1/docs/PROMPTS_AND_PROCESS.md) already provides the concise process record.
Your final Canvas submission should contain:
GitHub repository: <public GitHub URL>
YouTube walkthrough: <YouTube URL>
Medium article: <Medium URL>
AI transcript/process record: <share URL or repository file>
Do not upload .venv or the downloaded raw dataset files; Git already excludes them. The next step is publishing the GitHub repository.


12:44 PM








Is the github published?







12:59 PM






Worked for 14s



No. The local repository is clean, but it has no GitHub remote and has not been published yet.


12:59 PM
~~~

</details>
