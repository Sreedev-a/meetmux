# MeetMux / PlaceMux Codex Batch Instructions

You are working inside the user's existing MeetMux / PlaceMux Git repository.

## Source of truth
- Read `TASK_ORDER.md` first.
- Read each PDF completely before implementing that task.
- Phase and task numbers in the PDF are authoritative.
- Task numbering restarts across phases when the source material says so.
- Phase 2 Task 10 is intentionally skipped. Never create a Task 10 placeholder.
- Ignore duplicate PDFs and unrelated non-PlaceMux assignments.

## Protect existing work
- Inspect existing completed task folders before creating new ones.
- Do not delete, rename, overwrite, or reorganize already completed tasks unless absolutely required.
- For new work, use unambiguous folder names such as `Phase2_Task01_<short_title>` and `Phase3_Task21_<short_title>` when needed to avoid collisions.
- Never rewrite Git history and never force-push.

## Required workflow for every task
1. Read the complete PDF and identify objective, deliverables, tools, steps, verification criteria, and submission expectations.
2. Inspect relevant earlier tasks and reuse artifacts/pipelines only when technically appropriate.
3. Create a dedicated task folder following the repository's existing style while preserving phase/task identity.
4. Implement all required code, notebooks, configs, data samples, APIs, plots, models, metadata, and documentation.
5. Use real execution results. Never invent metrics, plots, model outputs, API responses, screenshots, or test results.
6. Install dependencies when needed. Prefer a task-local or existing project virtual environment as appropriate. Never commit virtual environments.
7. Run the implementation end-to-end and debug failures.
8. Verify requested output files actually exist and are readable.
9. Create `WRITTEN_ANSWER.md` containing a concise, professional, submission-ready written answer.
10. Create `SUBMISSION.md` containing: task number/title, what was implemented, files to submit, run commands, expected outputs, and any screenshots the user may need to take manually.
11. Add a small `README.md` when it materially helps the task run independently.
12. Check for secrets before staging files.
13. Run `git status`, stage only appropriate files, commit the task, and push to the existing remote/current branch.
14. Continue immediately to the next task in `TASK_ORDER.md`. Do not wait for routine confirmation.

## Git commit naming
Use:
`Complete Phase <P> Task <T> - <task title>`

Examples:
- `Complete Phase 1 Task 19 - Application Model Serializing`
- `Complete Phase 2 Task 1 - Company Onboarding & Marketplace Data Model`
- `Complete Phase 3 Task 21 - DPDP Consent & Security Foundations`

## Never commit
- `.venv/`, `venv/`
- `__pycache__/`, `*.pyc`
- `.env` or credential files
- API keys, tokens, passwords, private keys
- OS metadata such as `.DS_Store`
- `_task_pdfs/` unless the user explicitly requests the PDFs in Git

## Failure handling
Do not stop the whole batch because one task has a problem.

If a task is blocked by a genuinely external dependency (credentials, unavailable external service, human-only portal action, missing data that cannot be reasonably mocked):
- Complete everything that can be completed honestly.
- Create `BLOCKED.md` explaining the exact blocker, what is finished, and the minimum user action needed later.
- Commit the usable work if appropriate.
- Continue to the next task.

If GitHub push fails:
- Keep the local commit.
- Continue with the batch.
- Retry all pending pushes near the end.

## Quality rules
- Follow the PDF first, existing repository conventions second.
- Keep solutions appropriate for an AI/ML Engineer training assignment; do not over-engineer small tasks.
- Reuse shared utilities when useful, but each task must remain understandable and demoable.
- Use fixed random seeds for ML experiments when applicable.
- Record library versions/metrics when the PDF asks for reproducibility or traceability.
- Test APIs with automated requests/curl-equivalent commands when required.
- Validate saved model artifacts by loading them in a fresh process when serialization/deployment is involved.

## Batch completion
At the end create `TASK_BATCH_SUMMARY.md` with a table:
`Phase | Task | Title | Status | Folder | Main files | Output verified | Written answer | Commit | Push status | Blocker`

Then:
- Recheck `git status`.
- Retry any unpushed commits.
- Commit the summary.
- Push it.
- Report completed tasks, blocked tasks, and anything the user must do manually.
