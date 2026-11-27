# CI/CD Troubleshooting, Rollback and Review

## 1. End-to-End Troubleshooting Checklist

Follow the complete flow to find where the problem occurred:

1. **ADF Studio:** Check pipeline configuration, activities, expressions and references.
2. **Git Repository:** Check whether changes are saved, committed, pushed and merged into the correct branch.
3. **CI Pipeline:** Check validation, Node.js/npm installation, ARM template generation and artifact publishing.
4. **CD Pipeline:** Check the correct artifact, environment parameter file, service connection, permissions and deployment logs.
5. **Target Factory:** Verify pipelines, triggers, linked services, credentials, Integration Runtime and actual execution.

**Remember:** Find the stage where the problem first occurred and fix it there.

## 2. Rollback and Hotfix

### Rollback – Go back to a previous working version.

**Method 1: Redeploy previous build**
1. Find the previous successful CI build.
2. Use its ARM template artifact.
3. Select the correct environment parameter file.
4. Run CD deployment again.
5. Verify the target factory.

**Method 2: Revert a Pull Request**
1. Identify the PR that introduced the problem.
2. Create a revert PR to undo its changes.
3. Review and merge the revert.
4. Run CI/CD to deploy the reverted configuration.

### Hotfix – Make an urgent Production correction.

**Process:**
1. Identify the Production issue.
2. Create a hotfix branch from the appropriate release baseline.
3. Make the required fix.
4. Create a PR and run CI validation.
5. Deploy the fix to Production through CD.
6. Verify the fix and merge it back into the collaboration branch.

**Remember:** Rollback restores an earlier version; Hotfix introduces an urgent correction.

## 3. Basic Testing Before Release

Before releasing ADF changes, follow these checks:

1. **ADF Validation:** Validate pipelines and check activities, expressions, parameters, datasets and linked service references.
2. **Python Testing:** Use `pytest` to check whether Python functions produce expected results.
3. **Dev Test Run:** Execute the pipeline in Development using Debug or Trigger Now.
4. **Monitor:** Check pipeline/activity status, input, output and error messages.
5. **Data Verification:** Confirm expected records are loaded correctly without missing or duplicate data.

**Remember:** Validation checks configuration; Dev runs check actual execution.

## 4. Release Habits

Follow these practices while working on a team:

1. **Small Changes:** Make one meaningful change at a time. Easier to review, test and debug.
2. **Clear PR Description:** Explain what changed, why it changed, testing done and possible impact.
3. **Tags / Versions:** Give important releases version labels to identify them later.

Example: `v1.0.0`, `v1.1.0`, `v1.1.1`

- MAJOR – Big/breaking changes
- MINOR – New features
- PATCH – Bug fixes

**Remember:** A Git tag identifies a release commit; it does not deploy the project by itself.

## 5. CI/CD Review – Practical Knowledge Check

Practise troubleshooting intentionally broken pipelines and failed deployments.

| Problem | What to check |
|---|---|
| Pipeline not triggering | Trigger and branch filters |
| ADF validation failed | JSON, expressions and missing references |
| CI failed | Node.js, npm, validation and artifact logs |
| CD failed | ARM template, parameter file and permissions |
| Wrong environment deployed | Environment parameter mapping |
| Triggers remain stopped | Post-deployment script |
| Target pipeline fails | Linked services, credentials, IR and connectivity |

**Troubleshooting process:**

Identify problem → Check logs → Find root cause → Fix issue → Run again → Verify results.

### Quick Revision

- Troubleshooting: Studio → Repo → CI → CD → Target Factory.
- Rollback: Redeploy previous build or revert PR.
- Hotfix: Urgent Production fix through a separate branch and PR.
- Testing: Validate → pytest → Dev run → Verify data.
- Release habits: Small changes → Clear PR → Tags/versions.
- Review: Practise fixing broken pipelines and failed deployments.