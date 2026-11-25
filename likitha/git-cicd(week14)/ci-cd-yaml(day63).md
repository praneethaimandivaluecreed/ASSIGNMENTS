# Azure Pipelines: Running and Reading CI

## 1. Understanding CI/CD in ADF

CI/CD stands for **Continuous Integration and Continuous Delivery/Deployment**.

In Azure Data Factory, we develop pipelines in one environment, such as Development, and then move them to other environments, such as Test and Production.

For example, instead of manually creating the same ADF pipeline again in every environment, we can automate the process of moving the ADF resources using ARM templates and Azure DevOps.

- **Continuous Integration (CI):** Validates the changes made by developers and prepares the deployment files.
- **Continuous Delivery/Deployment (CD):** Takes the prepared files and deploys them to the target environment.

Moving an ADF pipeline from Development to Test or Production is called **deployment**.

### Traditional ADF CI/CD approach

After creating our ADF pipelines and connecting ADF Studio to Azure DevOps Git:

1. Developers make changes in their feature branches.
2. They create a pull request to merge their changes into the collaboration branch.
3. After merging, developers can use ADF Studio's Publish option.
4. ADF validates the resources and generates ARM templates.
5. The generated templates are pushed to the `adf_publish` branch.
6. A Release pipeline can use these templates to deploy ADF resources to Test or Production.

We can also deploy manually by uploading the ARM templates, but using Azure DevOps Release pipelines makes the process automated.

**Important:** `adf_publish` is a special publishing branch used in the traditional ADF publishing workflow. It is not the same as the collaboration branch.

### Classic Release pipeline

In Azure DevOps, we can create a Release pipeline separately from an ADF pipeline.

The basic flow is:

1. Go to **Pipelines → Releases** and create a release pipeline.
2. Add an artifact. For example, select the Azure Repo or build artifact containing the ARM templates.
3. Add stages such as Development, Test and Production.
4. Each stage represents a target environment.
5. Inside a stage, create a job and add the required deployment task.
6. Use the **Azure Resource Group Deployment** task to deploy the ARM template to the selected resource group.

The task generally requires:

- Azure subscription/service connection
- Resource group
- ARM template file: `ARMTemplateForFactory.json`
- ARM template parameters file: `ARMTemplateParametersForFactory.json`

We can also use the **Override template parameters** option to provide environment-specific values, such as the target factory name and other resource settings.

### Service connection and service principal

When configuring the Azure subscription in the deployment task, we need an authorized service connection.

A service connection allows Azure DevOps to authenticate with Azure and access the required resources.

Behind the scenes, it may use a service principal (an application identity in Microsoft Entra ID) or another supported identity.

A service principal can be associated with an App Registration.

**Important:** Clicking Authorize does not automatically mean the identity has every permission. The identity must have the required Azure RBAC permissions on the target resource or resource group.

For example, if the pipeline needs to deploy an ARM template, its identity must have the permissions required for that deployment.

### Release pipeline jobs

- **Agent job:** Runs tasks on an agent machine, such as a Microsoft-hosted or self-hosted agent.
- **Server/Agentless job:** Runs supported tasks on Azure DevOps' orchestration side without using an agent machine.
- **Empty job:** Creates a job without predefined tasks. We can add the required tasks ourselves.

We can create a release manually, schedule it, or configure continuous deployment so that a new release is created when a new artifact version becomes available.

---

## 2. Understanding a YAML pipeline

YAML is a human-readable format used to write configuration files. In Azure DevOps, a YAML pipeline tells Azure DevOps what to run, when to run it and where to run it.

The main sections are:

| Section | Purpose |
|---|---|
| `trigger` | WHEN should the pipeline run? |
| `pool` | WHERE should it run? |
| `stages` | WHAT major phases should happen? |
| `jobs` | WHO/what unit of work should execute? |
| `steps` | HOW should the work be performed? |
| `variables` | Which reusable values should be used? |

### 2.1 Trigger – When should the pipeline run?

A trigger decides when Azure DevOps should automatically start a pipeline.

Example:

```yaml
trigger:
  branches:
    include:
      - main
      - develop
    exclude:
      - feature/*
```

Here, the pipeline runs when changes are pushed to `main` or `develop`. Changes pushed to feature branches are excluded.

We can also write:

```yaml
trigger: none
```

This disables the YAML CI push trigger.

**Important trigger points:**

- Triggers can be configured in the YAML file or through Azure DevOps UI settings.
- If the UI option to override the YAML CI trigger is enabled, the UI configuration takes precedence over the YAML `trigger` section.
- If it is not enabled, the YAML trigger configuration is used.
- In Azure Repos Git, PR validation is normally configured through the target branch's **Build Validation branch policy**, rather than relying on a YAML `pr:` trigger.
- Scheduled triggers can be configured using `schedules:` in YAML or through the UI. When YAML schedules are defined, they take precedence over UI-defined schedules.

It is generally easier to maintain triggers in YAML because the configuration is stored in Git along with the pipeline code.

### 2.2 Pool – Where does the pipeline run?

A pool specifies which agent should execute the job.

An **agent** is a machine that runs our pipeline jobs and steps.

There are two main types:

**1. Microsoft-hosted agent**

Microsoft provides and manages the machine.

```yaml
pool:
  vmImage: 'ubuntu-latest'
```

Other examples include Windows and macOS images.

**2. Self-hosted agent**

We create and manage our own agent machine and register it with Azure DevOps.

```yaml
pool:
  name: 'MyCompanyPool'
```

A self-hosted agent is useful when we need access to private networks, specific software or custom configurations.

### 2.3 Stages – What are the major phases?

A stage represents a major phase of the pipeline.

For example:

```yaml
stages:
  - stage: Build
    displayName: 'Build Stage'

  - stage: DeployTest
    displayName: 'Deploy to Test'

  - stage: DeployProduction
    displayName: 'Deploy to Production'
```

- `Build`, `DeployTest` and `DeployProduction` are stage identifiers.
- `displayName` is the human-readable name shown in the Azure DevOps UI.
- The stage identifier is used internally when referring to a stage in `dependsOn` or stage output references.

By default, stages run sequentially when they are listed one after another. We can use `dependsOn` to control their order.

For example:

```yaml
- stage: DeployProduction
  dependsOn: DeployTest
```

This means Production deployment waits for the Test stage to finish successfully.

If we write `dependsOn: []`, the stage has no dependency on the previous stage and can run independently, subject to available resources and conditions.

### 2.4 Jobs – What units of work should execute?

A job is a unit of work inside a stage. It contains one or more steps and normally runs on an agent.

For example, in the Build stage, we may have two responsibilities:

- Validate ADF resources.
- Export ARM templates.

We can create separate jobs for them:

```yaml
stages:
  - stage: Build
    jobs:
      - job: ValidateADF
        steps:
          - script: echo "Validating ADF"

      - job: ExportTemplate
        steps:
          - script: echo "Exporting ARM template"
```

By default, jobs in the same stage can run in parallel if no dependency is defined.

We can use `dependsOn` to make one job wait for another:

```yaml
- job: ExportTemplate
  dependsOn: ValidateADF
```

Now, `ExportTemplate` waits for `ValidateADF` to complete successfully.

Actual parallel execution also depends on the parallel-job capacity available to the Azure DevOps organization.

### 2.5 Steps – What actions should be performed?

Steps are individual actions inside a job.

Steps run sequentially by default.

In YAML, every item starting with `-` under `steps:` represents a step.

A step can be:

- A task: `- task: ...`
- A shell command: `- script: ...`
- A Bash command: `- bash: ...`
- A PowerShell command: `- pwsh: ...`

Example:

```yaml
steps:
  - task: UseNode@1
    inputs:
      version: '20.x'
    displayName: 'Install Node.js'

  - script: echo "ADF validation started"
    displayName: 'Start validation'
```

Here, `UseNode@1` is a task available in Azure Pipelines. We specify the task name and provide its required inputs.

**Classic Release UI vs YAML:**

In a Classic Release pipeline, we add tasks directly to a job through the UI. In YAML, everything under `steps:` is called a step, and `task` is just one type of step.

### 2.6 Variables – How do we store reusable values?

Variables help us store values that we want to reuse instead of writing the same value repeatedly.

Example:

```yaml
variables:
  environment: 'Development'
  resourceGroup: 'ADF-Dev-RG'
  factoryName: 'my-adf-dev'
```

We can access a variable using macro syntax:

```yaml
steps:
  - script: echo "Deploying to $(environment)"
```

`$(environment)` is Azure DevOps macro-variable syntax.

Variables can be defined at pipeline, stage or job level. We can also create reusable variable groups under:

**Pipelines → Library → Variable groups**

Variable groups are useful for sharing values across pipelines. They can also contain secret variables or link to Azure Key Vault, depending on the configuration and permissions.

### Parameters vs variables

- **Parameters** are useful when we want to pass values into a pipeline or template when it is run or expanded.
- **Variables** are useful for storing reusable values during pipeline execution. They can also be updated during a run using supported tasks.

Example parameter:

```yaml
parameters:
  - name: DataFactory
    type: string
    default: 'my-adf-dev'
```

---

## 3. YAML syntax and safe editing

When editing YAML, we need to be careful because indentation and structure are important.

Important syntax rules:

1. Indentation is important. Use spaces, not tabs.
2. A colon `:` separates a key and its value.
3. A hyphen `-` represents an item in a list.
4. Strings can be written inside single or double quotes.
5. Boolean values are `true` and `false`; `null` represents no value.
6. Use consistent indentation throughout the file.

To write multiple commands inside one script, we can use the pipe symbol `|`.

```yaml
steps:
  - script: |
      echo "First command"
      echo "Second command"
      echo "Third command"
```

All three commands execute as part of the same script step.

### Safe editing approach

Whenever we need to make a small change to an existing YAML pipeline:

1. First understand the existing structure.
2. Identify the exact section that needs modification.
3. Make only the required change.
4. Check indentation and list alignment.
5. Verify task names, inputs and variable references.
6. Validate the YAML and pipeline configuration.
7. Run the pipeline and inspect the logs.

We should avoid changing multiple unrelated sections at once because it makes debugging harder.

---

## 4. CI for ADF using azure-data-factory-utilities

In the automated ADF CI process, we use the npm package:

`@microsoft/azure-data-factory-utilities`

This package runs using Node.js and helps us validate ADF resources and generate ARM templates.

### Traditional Publish vs automated CI

Earlier, we used ADF Studio's **Validate All** and **Publish** options.

With ADF Utilities, we can perform similar validation and ARM template export through an Azure DevOps YAML pipeline.

The important commands are:

- `validate` – Validates the ADF resources in the repository.
- `export` – Validates the resources and generates ARM templates.

**Important:** Exporting an ARM template does not deploy it to the live factory. Deployment is a separate CD step.

### Basic project setup

A good practice is to keep CI/CD files in a separate folder in the Git repository, instead of mixing them with ADF resources.

Example structure:

```text
Repository/
│
├── package.json
├── ADF/
│   ├── pipeline/
│   ├── dataset/
│   ├── linkedService/
│   └── factory/
│
└── CI-CD/
    └── azure-pipelines.yml
```

The exact ADF folder name depends on the Git configuration in ADF Studio.

We create a `package.json` file in the folder where we want to manage the npm package.

Example:

```json
{
  "scripts": {
    "build": "node node_modules/@microsoft/azure-data-factory-utilities/lib/index"
  },
  "dependencies": {
    "@microsoft/azure-data-factory-utilities": "^1.0.0"
  }
}
```

This declares the ADF Utilities npm dependency and defines a reusable build command.

### Main steps in the CI YAML pipeline

**Step 1: Install Node.js**

```yaml
- task: UseNode@1
  inputs:
    version: '20.x'
  displayName: 'Install Node.js'
```

The package needs Node.js to execute.

**Step 2: Install npm packages**

```yaml
- task: Npm@1
  inputs:
    command: 'install'
    workingDir: '$(Build.Repository.LocalPath)/<package-folder>'
    verbose: true
  displayName: 'Install npm package'
```

This installs the dependencies declared in `package.json`.

`workingDir` points to the folder containing the `package.json` file.

**Step 3: Validate ADF resources**

```yaml
- task: Npm@1
  inputs:
    command: 'custom'
    workingDir: '$(Build.Repository.LocalPath)/<package-folder>'
    customCommand: 'run build validate $(Build.Repository.LocalPath)/<ADF-root-folder> /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DataFactory/factories/<factory-name>'
  displayName: 'Validate ADF'
```

This validates the ADF resources in the specified repository folder against the source factory information.

It performs checks similar to ADF Studio's **Validate All**.

**Step 4: Validate and export ARM templates**

```yaml
- task: Npm@1
  inputs:
    command: 'custom'
    workingDir: '$(Build.Repository.LocalPath)/<package-folder>'
    customCommand: 'run build export $(Build.Repository.LocalPath)/<ADF-root-folder> /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.DataFactory/factories/<factory-name> "ArmTemplate"'
  displayName: 'Validate and Generate ARM template'
```

The export command validates the resources and generates ARM templates in the `ArmTemplate` destination folder.

We do not need to run both `validate` and `export` if our only requirement is to validate and export, because `export` already performs validation.

**Step 5: Publish the ARM template as an artifact**

```yaml
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(Build.Repository.LocalPath)/<package-folder>/ArmTemplate'
    artifact: 'ArmTemplates'
    publishLocation: 'pipeline'
```

This publishes the generated ARM template folder as a pipeline artifact.

The Release/deployment pipeline can then download and use this artifact.

### Important CI points

- `UseNode@1` installs the required Node.js version.
- `Npm@1` runs npm commands.
- `npm install` installs dependencies from `package.json`.
- `validate` checks ADF resource configurations.
- `export` validates and generates ARM templates.
- `PublishPipelineArtifact@1` publishes the generated templates for the next stage or pipeline.
- The `PrePostDeploymentScript.ps1` file is included in the generated ARM template output when produced by the export workflow. It helps manage trigger handling during deployment.

The pre/post-deployment script is useful for stopping and starting triggers around deployment. We may need to customize or maintain it depending on our deployment requirements.

**Preview export:** A preview build command such as `build-preview` may be used with the appropriate package script and supported options. It is intended for preview deployment behavior, including handling modified triggers. We must configure the matching script in `package.json` before using it.

### What happens after CI?

A typical automated flow is:

1. Developer makes changes in a feature branch.
2. Developer creates a PR.
3. Branch build validation runs.
4. After the PR is approved and merged, the CI pipeline runs on the target branch.
5. CI validates ADF resources and generates ARM templates.
6. The templates are published as a pipeline artifact.
7. The CD/Release pipeline deploys the artifact to Test or Production.

The deployment identity and its Azure permissions are checked during deployment, not simply by ADF JSON validation.

---

## 5. Branch policies: Build validation and required reviewers

Branch policies are rules that protect important branches such as `main` or the ADF collaboration branch.

They prevent incorrect or unreviewed changes from entering the protected branch.

For example, an organization may require:

- At least two reviewers to approve a PR.
- Build validation to succeed.
- All review comments to be resolved.

Only after satisfying the required policies can the PR be completed.

### How PR validation works

1. Developer creates a feature branch.
2. Developer makes changes and pushes them.
3. Developer creates a pull request to the protected branch.
4. Azure DevOps runs the configured build validation pipeline.
5. Reviewers examine the changes.
6. If all required policies pass, the PR can be completed and merged.

### Build validation

Build validation is a branch policy that automatically runs a selected pipeline when a PR is created or updated.

For ADF, we can configure this pipeline to run ADF Utilities and validate the ADF resource JSON/configuration.

- **Required build validation:** The PR cannot be completed until the build succeeds.
- **Optional build validation:** The build can run, but its result does not block PR completion.

Important: Branch validation itself is not a separate ADF validation engine. It is a policy that runs whichever pipeline we configure. If that pipeline uses ADF Utilities, it can perform ADF resource validation.

### Required reviewers

Required reviewers are the people or teams whose approval is needed before the PR can be completed.

Common review responses include:

- **Approve:** The reviewer accepts the changes.
- **Approve with suggestions:** The reviewer approves but suggests improvements.
- **Wait for author:** The reviewer wants the author to make changes.
- **Reject:** The reviewer does not approve the changes.

### Common branch policy settings

| Setting | Purpose |
|---|---|
| Minimum number of reviewers | Number of approvals required |
| Check for comment resolution | Requires review comments to be resolved |
| Build validation | Selects the pipeline that must run and pass |
| Automatically included reviewers | Adds specific people or teams as reviewers |
| Reset code reviewer votes | Controls whether approvals are reset when new changes are pushed |

We can configure these under:

**Azure DevOps → Repos → Branches → Select the protected branch → Branch policies**

### Important distinction

- Build validation = Machine checks.
- Required reviewers = Human checks.
- Branch policies = Rules that control whether a PR can be completed.

Branch policies protect PR completion. Direct push restrictions are controlled separately through branch permissions.

---

## 6. Reading pipeline logs and debugging failures

Whenever a pipeline fails, we should not randomly change the YAML file.

First, identify which stage, job and step failed.

### How to read pipeline logs

1. Open Azure DevOps → Pipelines.
2. Open the failed pipeline run.
3. Identify the failed stage and job.
4. Open the failed step.
5. Start reading from the error near the bottom of that step.
6. Read the earlier lines in the same step to understand what happened before the error.
7. If necessary, inspect the previous steps to find the original cause.

The final error message is not always the root cause, so we should read the surrounding logs.

### Common debugging scenarios

**1. YAML indentation error**

Possible reasons:

- Incorrect indentation.
- Using tabs instead of spaces.
- Misaligned hyphens in a list.
- Putting a property under the wrong section.
- Incorrect task structure.

What to do:

- Check the line number mentioned in the error.
- Verify the indentation of the surrounding lines.
- Check whether the property belongs under `steps`, `jobs`, `stages` or `inputs`.
- Validate the YAML structure and rerun.

**2. Failed ADF Validate step**

Possible reasons:

- Invalid JSON or ADF resource configuration.
- Incorrect activity properties.
- Missing or incorrect resource references.
- Incorrect expressions.
- Dataset, linked service or pipeline dependency problems.

What to do:

- Open the failed Validate step logs.
- Identify the resource or file mentioned in the error.
- Open that ADF resource in the repository.
- Correct the configuration and commit the changes.
- Rerun the pipeline.

**Important:** Successful ADF validation does not prove that a database connection works or that external credentials are correct.

**3. Missing permissions**

Sometimes the pipeline fails with an authorization or access-denied error.

Possible reasons:

- The service connection is not authorized for the pipeline.
- The service principal or deployment identity does not have the required Azure RBAC role.
- The identity has access to the wrong resource group or subscription.
- The pipeline does not have permission to access a required resource.

What to do:

- Identify which identity the deployment task is using.
- Check whether the pipeline is authorized to use the service connection.
- Check the identity's Azure RBAC permissions and scope.
- Give only the permissions required for the task instead of unnecessarily assigning Owner.

**4. Pipeline did not trigger**

Possible reasons:

- The pushed branch is not included in the trigger.
- The branch is excluded by a filter.
- `trigger: none` is configured.
- The YAML file path is incorrect in the pipeline configuration.
- The pipeline is disabled or trigger settings are overridden in the UI.
- A PR build validation policy has not been configured on the target branch.

What to do:

- Check the `trigger` section.
- Verify branch include/exclude filters.
- Check the UI trigger override setting.
- Confirm the pipeline points to the correct YAML file.
- For Azure Repos PR validation, check the target branch's Build Validation policy.

### Branch validation vs ADF validation vs authentication

These are related, but they are not the same thing.

| Check | What it answers |
|---|---|
| ADF validation | Is my ADF configuration correct? |
| Branch build validation | Did the configured PR pipeline pass? |
| Authentication | Can the identity prove who it is? |
| Connectivity | Can ADF actually reach the external service? |
| Deployment authorization | Does the deployment identity have permission to deploy? |

For example, a linked service JSON may be perfectly valid, but its database password could still be wrong.

ADF validation checks the resource configuration. It does not automatically test the database credentials or network connectivity.

Similarly, the deployment service connection may authenticate successfully but still fail if its identity does not have the required Azure RBAC permissions.

### Quick debugging memory trick

- **No pipeline run** → Check trigger configuration.
- **YAML error** → Check syntax and indentation.
- **Validate failed** → Check ADF resource configuration.
- **Authorization failed** → Check service connection and permissions.
- **Connectivity failed** → Check credentials, Integration Runtime, firewall and network access.
- **Step skipped** → Check previous step results, conditions and dependencies.

---

## 7. Final CI/CD flow to remember

```text
Developer makes changes
          |
          v
     Feature Branch
          |
          v
    Create Pull Request
          |
          v
   Branch Build Validation
          |
          v
   Required Reviewer Approval
          |
          v
     Merge to Main
          |
          v
      CI Pipeline
          |
          v
  Install Node and npm packages
          |
          v
   Validate ADF Resources
          |
          v
   Export ARM Templates
          |
          v
  Publish Pipeline Artifact
          |
          v
     CD / Release Pipeline
          |
          v
   Deploy to Test / Production
```

**Important points to remember for interviews:**

1. Azure DevOps YAML pipelines and Azure Data Factory pipelines are different. ADF pipelines perform data workflows; Azure DevOps pipelines automate CI/CD.
2. Branch validation is a PR policy that runs a configured pipeline.
3. ADF Utilities can validate ADF resources and export ARM templates.
4. Exporting ARM templates is not the same as deploying them.
5. ARM templates are deployed using a deployment identity with the required Azure permissions.
6. ADF JSON validation does not guarantee that external connections or credentials will work.
7. Branch policies combine machine validation and human approval to protect important branches.
8. Pipeline logs should be checked from the failing step, starting with the error and then tracing backwards to find the root cause.