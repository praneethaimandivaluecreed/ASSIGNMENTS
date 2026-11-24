# ADF Git Integration in Practice – Running Notes

## 1. Introduction to ADF Git Integration

Azure Data Factory (ADF) supports Git integration using:

- Azure DevOps Git repository
- GitHub repository

Git integration helps developers maintain ADF code, track changes, work in teams and manage different versions of pipelines.

**Important points:**

- One Azure Data Factory can be connected to one Git repository at a time.
- Multiple developers can work on the same repository using different branches.
- ADF resources are stored as JSON files in the repository.
- Git stores the definitions of pipelines and other resources, not the actual data processed by them.

### Azure DevOps hierarchy

To use Azure DevOps, we first create an account at https://dev.azure.com.

The basic hierarchy is:

**Organization → Projects → Repositories (Repos) → Branches**

- Organization: The top-level space for managing projects.
- Project: A workspace for a particular application or team.
- Repository: Stores the project's code and files.
- Branch: A separate version of the code where developers can work independently.

---

## 2. Connect ADF Studio to an Azure DevOps Repository

To connect ADF with Azure DevOps:

1. Open Azure Data Factory Studio.
2. Go to Manage → Git configuration.
3. Select Azure DevOps Git.
4. Select the Azure DevOps organization.
5. Select the project and repository.
6. Select the collaboration branch (usually `main`).
7. Provide the root folder if required.
8. Save the configuration.

After connecting, ADF Studio displays Git-related options.

We can now create pipelines, datasets, linked services and other resources while tracking their changes through Git.

**Important:** ADF can be connected to either GitHub or Azure DevOps Git. The basic Git workflow is similar, but the PR interface and repository management experience differ.

---

## 3. Collaboration Branch and Feature Branches

### A. Collaboration Branch

The collaboration branch is the main branch where approved development changes are combined.

Usually, it is named `main` or `master`.

Think of it as the final development code of the application.

- It contains the approved ADF resource definitions.
- Developers create their changes in separate feature branches.
- Changes are merged into the collaboration branch through Pull Requests.
- Publishing is performed from the collaboration branch.

### B. Feature Branch

A feature branch is a separate branch created for developing a particular feature or making changes.

Example:

- `main` – Collaboration branch
- `feature/employee-pipeline` – Feature branch
- `feature/customer-load` – Another feature branch

Developers can work independently without directly disturbing the collaboration branch.

### C. Save vs Publish – Very Important

These two operations are different.

**1. Save / Save All**

- When we create or modify an ADF resource, we click Save or Save All.
- ADF saves the resource JSON definitions into the currently selected Git branch.
- If we are working in a feature branch, the changes are saved in that feature branch.
- Saving does NOT deploy the changes to the live ADF service.

**2. Publish**

- Publishing is allowed only from the configured collaboration branch.
- We cannot directly publish from a feature branch.
- If we try to publish from a feature branch, ADF asks us to merge the changes into the collaboration branch first.
- Publishing validates the resources, generates ARM templates and updates the live ADF service.

**Remember:**

Save = Save changes to Git.

Publish = Publish the collaboration branch changes to the live ADF service.

---

## 4. Create a Pull Request and Merge Changes

A Pull Request (PR) is used to request the merging of changes from one branch into another.

Example:

Developer A creates a pipeline in `feature/employee-pipeline`.

The workflow is:

1. Create a feature branch from the collaboration branch.
2. Develop the pipeline, datasets and linked services.
3. Click Save All to save the JSON definitions into the feature branch.
4. Open the Git/PR option in ADF Studio.
5. Create a Pull Request.
6. Select the collaboration branch (`main`) as the target branch.
7. Review the changes and resolve any conflicts.
8. Get approval if required.
9. Complete the Pull Request and merge the changes into `main`.

ADF Studio can provide a link to create or view the Pull Request in GitHub or Azure DevOps, depending on the repository provider.

**Important:** Creating a Pull Request does not mean the changes are already merged. The PR must be reviewed and completed.

After merging, the approved changes become part of the collaboration branch.

---

## 5. What Is Stored in the Git Repository?

ADF stores its resource definitions as separate JSON files.

The important resource types are:

### A. Pipeline JSON

A pipeline contains the execution logic of the data workflow.

It defines:

- Activities (Copy, Lookup, ForEach, etc.).
- Activity dependencies.
- Source and sink dataset references.
- Parameters and variables.

Example: `CopyEmployeeData.json`

### B. Dataset JSON

A dataset describes the data we want to access.

It contains information such as:

- Data location.
- File name or table name.
- File format.
- Linked Service reference.
- Dataset parameters.

Example: `EmployeeSource.json`

### C. Linked Service JSON

A Linked Service contains the connection configuration required to connect to an external system.

Examples:

- Azure SQL Database.
- Azure Data Lake Storage.
- Azure Blob Storage.
- REST API.

It can contain server names, database names, authentication configuration and Key Vault secret references.

**Important:** Avoid storing passwords or sensitive credentials directly in Git. Use Key Vault references or Managed Identity wherever appropriate.

### D. Trigger JSON

A trigger defines when a pipeline should execute.

Examples:

- Schedule trigger – Runs at a particular time.
- Tumbling window trigger – Runs at fixed, continuous time windows.
- Storage event trigger – Runs when a file event occurs.

**Important:** A trigger definition being saved or deployed does not automatically mean it is started. Trigger state must be managed separately.

### How are these resources connected?

Example: Copy employee data from SQL Server to ADLS.

- Pipeline: `CopyEmployeeData`
- Source Dataset: `EmployeeSource`
- Sink Dataset: `EmployeeSink`
- Source Linked Service: `AzureSqlDB`
- Sink Linked Service: `ADLSConnection`

Relationship:

Pipeline → Dataset → Linked Service → Actual data source/destination.

**Key takeaway:** ADF resources are stored as separate JSON files, but they are connected through references.

Changing or renaming one resource can affect other resources. For example, if we rename a dataset but the pipeline still refers to its old name, validation or publishing may fail.

### Typical Git repository structure

- `pipeline/` – Pipeline JSON files
- `dataset/` – Dataset JSON files
- `linkedService/` – Linked Service JSON files
- `trigger/` – Trigger JSON files
- `dataflow/` – Data Flow definitions
- `integrationRuntime/` – Integration Runtime definitions
- `factory/` – Factory-level configuration

The exact structure can vary depending on the ADF Git root folder and resources used.

---

## 6. What Is the adf_publish Branch?

This is one of the most important concepts in ADF Git integration.

When we publish changes from the collaboration branch, ADF generates ARM templates and stores them in a separate branch called `adf_publish` by default.

### First, understand ARM templates

ARM stands for Azure Resource Manager.

ARM templates are JSON files that contain instructions for creating or updating Azure resources.

ADF converts its resource definitions into ARM templates so that the factory configuration can be deployed to other environments.

### Difference between main and adf_publish

**1. Collaboration Branch (main)**

- Contains individual ADF resource JSON definitions.
- Stores pipelines, datasets, linked services, triggers, etc.
- Used for development, collaboration and code reviews.
- Contains the actual development definitions.

**2. adf_publish Branch**

- Contains generated ARM deployment templates.
- Used mainly for CI/CD deployment.
- Contains files such as:
  - `ARMTemplateForFactory.json`
  - `ARMTemplateParametersForFactory.json`
- May also contain a `linkedTemplates` folder when templates are split into smaller files.

### Easy way to remember

- `main` = Raw ingredients / blueprint sketches.
- ARM template = Ready-to-use assembly instructions.
- `adf_publish` = Shelf where the generated deployment instructions are stored.

Developers work with the original ADF JSON definitions in the collaboration branch, while release pipelines can take the generated ARM templates from `adf_publish`.

This provides a cleaner separation between development files and deployment files.

### What exactly happens when we click Publish?

1. ADF validates the resources and their dependencies.
2. ADF generates ARM deployment templates.
3. The generated templates are committed to the configured publish branch (`adf_publish` by default).
4. ADF applies the published configuration to the live Data Factory service.

**Important:** The collaboration branch and publish branch are not two copies of the same content.

- Collaboration branch → Individual ADF resource definitions.
- Publish branch → Generated ARM templates.

Also, merging changes into `main` does NOT automatically update the live ADF service. Publishing or an automated deployment process is required.

### When does adf_publish matter?

It is especially important when we have multiple environments:

DEV → TEST → PROD.

Example workflow:

1. Develop and test pipelines in DEV.
2. Merge approved changes into the collaboration branch.
3. Publish the changes.
4. Generate ARM templates in `adf_publish`.
5. Azure DevOps release pipeline takes those ARM templates.
6. Deploy the templates into TEST and then PROD.

**Important nuances:**

- `adf_publish` is not the actual deployment pipeline. It stores deployment templates.
- We normally should not manually edit ADF-generated templates or treat this branch as a development branch.
- Publishing is not the same as deploying to TEST or PROD.
- ADF's normal Publish operation publishes the collaboration branch changes as a whole; it does not provide selective publishing of individual resources.
- Large factories can use linked ARM templates, containing a master template and smaller child templates.

### Environment-friendly overrides

We generally maintain one pipeline design but use different environment configurations.

Example:

- DEV → `devserver.database.windows.net`
- TEST → `testserver.database.windows.net`
- PROD → `prodserver.database.windows.net`

During deployment, environment-specific values can be supplied through ARM template parameters and other deployment configurations.

This avoids maintaining completely separate pipeline designs for each environment.

---

## 7. Debugging and Common Issues

### A. Publish Failure

**How to debug:**

1. Open the validation/publish error details.
2. Identify the resource causing the failure.
3. Check the JSON definition and resource references.
4. Correct the missing or invalid configuration.
5. Validate the factory again.
6. Publish after fixing the issue.

### B. JSON Merge Conflicts

When two developers modify the same JSON file, Git may report a merge conflict.

Example:

```text
<<<<<<< HEAD
"source": "EmployeeSource_New"
=======
"source": "EmployeeSource_Updated"
>>>>>>> feature_branch
```

These are Git conflict markers. They are not valid JSON properties.

**How to resolve:**

1. Compare both versions.
2. Understand what each developer changed.
3. Discuss which changes are required.
4. Combine the correct changes.
5. Remove all conflict markers.
6. Validate JSON syntax.
7. Check ADF resource references.
8. Commit the resolved changes and complete the merge.

**Important:** Valid JSON does not always mean valid ADF configuration. A pipeline can contain valid JSON but still reference a dataset that doesn't exist.

Never blindly select Accept Current or Accept Incoming.

### C. Publish Branch Out of Date

This means the generated deployment templates and the current ADF/Git configuration may be out of sync.

**Two recovery approaches:**

**Option 1: Overwrite Live Mode**

- Use the collaboration branch as the source of truth.
- Overwrite the live factory with the definitions from Git.
- Use this when Git is correct and the live factory is outdated.

**Option 2: Disconnect and Reconnect Git**

- Disconnect the Git repository.
- Reconnect using the same repository configuration.
- Import the existing live ADF resources into the collaboration branch.
- Review and merge the imported changes.

Use this when the live factory contains valid changes that are missing from Git.

**Important:** Never blindly overwrite live mode. First identify which version contains the correct changes.

### D. Resource Already Exists

During deployment, we may encounter a resource that already exists in the target environment.

**Important:** An existing resource does not automatically mean deployment will fail. ARM deployments generally support create-or-update behaviour for compatible resources.

**How to debug:**

1. Identify the exact resource mentioned in the error.
2. Check whether it already exists in the target ADF.
3. Compare its name, type and configuration with the ARM template.
4. Check whether the attempted update is supported.
5. Check its dependencies.
6. Correct the configuration and redeploy.

Don't immediately delete an existing resource. Other pipelines may depend on it.

---

## 8. Important Additional Points to Remember

1. Debug and Trigger Now are different:
   - Debug uses the current authoring definition.
   - Trigger Now and scheduled triggers use the live factory definition.
   - Therefore, a pipeline may work in Debug but fail when triggered if the latest changes haven't been published.

2. If publishing fails, the previous successfully generated publish templates normally remain in `adf_publish`. A failed publish does not mean new templates were successfully generated.

3. Publishing and deployment are different:
   - Publish → Updates the live development factory and generates ARM templates.
   - Deployment → Uses ARM templates to update another environment, such as TEST or PROD.

4. ADF does not normally support publishing just one selected resource. It publishes the collaboration branch changes as a whole.

5. Triggers may need to be stopped before deployment and restarted afterward. This is commonly handled using pre-deployment and post-deployment scripts in CI/CD.

6. ADF can generate linked ARM templates for large factories to avoid template size limitations. The deployment pipeline should use the master template and make the child templates accessible.

---

## 9. Quick Revision – Interview Points

| Topic | Remember |
|---|---|
| Git integration | Azure DevOps or GitHub |
| Collaboration branch | Main development branch |
| Feature branch | Independent development |
| Save All | Saves JSON changes into the current Git branch |
| Pull Request | Requests merging into collaboration branch |
| Publish | Publishes collaboration branch changes to live ADF |
| Pipeline JSON | Activity and execution definitions |
| Dataset JSON | Data location and format |
| Linked Service JSON | Connection configuration |
| Trigger JSON | Execution schedule or event |
| adf_publish | Stores generated ARM templates |
| ARM template | Deployment instructions |
| Merge conflict | Compare, resolve and validate changes |
| Publish branch out of date | Identify the correct source of truth |
| Resource already exists | Check identity, type and configuration |
| Debug vs Trigger Now | Authoring definition vs live definition |

**Final understanding:**

The complete ADF Git workflow is:

Create Feature Branch → Develop ADF Resources → Save All → Create Pull Request → Review and Merge into Collaboration Branch → Publish → Generate ARM Templates in adf_publish → Deploy to TEST/PROD using Azure DevOps CI/CD.

Remember these three things:

- Git manages and tracks our ADF development changes.
- ADF Publish generates deployment templates and updates the live development factory.
- Azure DevOps CI/CD uses those templates to deploy changes across different environments.