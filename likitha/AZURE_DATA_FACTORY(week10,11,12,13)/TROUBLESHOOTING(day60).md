1. Debugging Process
1. Read the error message in Monitor.
2. Identify the failed activity.
3. Inspect activity Input and Output.
4. Reproduce the issue using Debug.
5. Find and fix the root cause.
6. Rerun the pipeline and verify the output.
2. Common Errors
Error	What to check
Authentication	Credentials, expired secrets, Managed Identity
Permission (403)	RBAC roles, ADLS ACLs, firewall
Schema mismatch	Column names, data types, mapping
Timeout	Activity duration, query, IR performance
Throttling (429)	Parallelism, batch count, retry
Expression error	Syntax, brackets, item(), parameters

3. ADF Best Practices
- Naming: Use meaningful names (PL_Copy_Trades, DS_Source_Trades).
- Folders: Organize pipelines, datasets, linked services and triggers.
- Annotations: Add project, purpose and ownership details.
- Parameters: Avoid hard-coded table names, paths and values.
- Reusable pipelines: Use Lookup → ForEach → Parameterized Copy instead of creating duplicate pipelines.
4. Cost and Performance
- Stop Mapping Data Flow debug sessions when not needed.
- Avoid Data Flows for simple copy operations.
- Set trigger frequency according to business requirements.
- Use sensible ForEach batch count to avoid overloading services.
- Prefer incremental loading over repeated full loads when possible.
- Copy only required data.
5. Final Revision
ADF troubleshooting flow:

Identify → Inspect → Reproduce → Fix → Rerun → Verify

Main goal: Build pipelines that are reusable, easy to debug, reliable and cost-efficient.