# Deploying ADF to Test and Production

After developing and validating our ADF pipelines in Development, we need to move them to Test and Production. We use Azure DevOps Release/Deployment pipelines to automate this process using ARM templates.

## 1. Run a Release – ARM Template Deployment

In CI, we validate our ADF resources and export the ARM template. The generated template is published as a pipeline artifact.

Now, in CD, the Release pipeline takes this artifact and deploys it to the target environment.

Two important files are:

- `ARMTemplateForFactory.json` – Contains the ADF resource configuration that needs to be deployed.
- `ARMTemplateParametersForFactory.json` – Contains the parameter values supplied to the ARM template.

In Azure DevOps, we use the **Azure Resource Group Deployment** task to deploy the ARM template.

Inside the deployment task, we provide:
- Azure subscription / service connection
- Target resource group
- ARM template file
- ARM template parameter file

The service connection provides an identity for Azure DevOps to authenticate with Azure. That identity must also have the required Azure RBAC permissions to deploy resources.

## 2. Parameter Files for Each Environment

We have some values that are different for different environments. For example:

| Setting | Development | Test | Production |
|---|---|---|---|
| Data Factory | adf-dev | adf-test | adf-prod |
| Resource Group | ADF-Dev-RG | ADF-Test-RG | ADF-Prod-RG |
| SQL Server | dev-sql-server | test-sql-server | prod-sql-server |
| Database | DevDB | TestDB | ProdDB |

Instead of creating different ARM templates for each environment, we use the same template with different parameter files.

**YAML parameters tell the pipeline what values it can accept. Parameter files provide the actual values for each environment.**

Example folder structure:

```text
CI-CD/
│
├── ARMTemplateForFactory.json
│
├── Parameters/
│   ├── dev.parameters.json
│   ├── test.parameters.json
│   └── prod.parameters.json
│
└── azure-pipelines.yml
```

### How do we map the parameter file to an environment?

Inside each deployment stage in YAML, we specify the ARM template and the corresponding parameter file.

Example:

```yaml
- stage: DeployTest
  jobs:
    - job: Deploy
      steps:
        - task: AzureResourceManagerTemplateDeployment@3
          inputs:
            csmFile: 'ARMTemplateForFactory.json'
            csmParametersFile: 'Parameters/test.parameters.json'
```

For Production, we use:

```yaml
csmParametersFile: 'Parameters/prod.parameters.json'
```

So, the mapping is:

- DeployTest stage → Test parameter file.
- DeployProduction stage → Production parameter file.

The same ARM template is deployed with different environment-specific values.

**Important:** Parameter files must contain the correct parameter names expected by the ARM template. Never store plain-text passwords or secrets in them.

## 3. Pre- and Post-Deployment Script

Before deploying ADF resources, we need to handle triggers carefully.

Imagine a trigger is scheduled to run every day at 10 AM. If it starts while we are updating the ADF resources, it may execute a pipeline when its configuration is not fully updated.

To avoid this, we use a pre- and post-deployment script.

The generated script is:

`PrePostDeploymentScript.ps1`

It contains logic to manage triggers around deployment.

### Deployment sequence

**1. Pre-deployment script – Before deployment**

- Stops the relevant triggers in the target Data Factory.
- Prevents new scheduled or event-based pipeline runs during deployment.

**2. Deployment – Deploy ARM template**

- Deploys the new ARM template.
- Updates ADF resources such as pipelines, datasets and linked services.

**3. Post-deployment script – After deployment**

- Starts the relevant triggers again.
- Allows normal scheduled or event-based executions to continue.

Why do we stop triggers? Because we don't want them to start pipeline executions while ADF resources are being updated.

Why do we restart them? Because normal automated executions should resume after deployment.

**Important:** The script being present in the artifact does not mean it runs automatically. We must configure the deployment pipeline to execute it before and after the ARM deployment task.

## 4. Approvals, Checks, Variable Groups and Key Vault

### Approvals and checks

Suppose we are deploying changes to Production. We may not want the deployment to happen immediately after the Test deployment.

We can configure approvals and checks so that an authorized person reviews the deployment before it proceeds.

For example:

- Development → Test: Deployment can happen automatically.
- Test → Production: Team lead approval may be required.

Approvals and checks help control when a deployment is allowed to proceed. They can be configured on protected resources such as environments and service connections.

### Variable groups

Variable groups are available under:

**Azure DevOps → Pipelines → Library → Variable groups**

They help us store reusable values such as:
- Resource group names
- Data Factory names
- Environment-specific settings

We can reuse these variables in our YAML pipeline.

### Azure Key Vault

We should not store passwords, connection strings or other sensitive information directly in YAML or parameter files.

Instead, we can store secrets in Azure Key Vault and connect it to Azure DevOps through a variable group.

The pipeline can then access the required secrets securely, provided the required permissions are configured.

## 5. Verify After Deployment

After deploying the ARM template, we should verify whether the resources were deployed correctly in the target Data Factory.

I will check three important things:

**1. Pipelines**

Go to Target Data Factory → Author → Pipelines.

Check:
- Are all expected pipelines present?
- Are all activities configured correctly?
- Are the dataset and linked service references correct?

**2. Triggers**

Go to Target Data Factory → Manage → Triggers.

Check:
- Are all expected triggers present?
- Are their schedules or event conditions correct?
- Are they in the expected state (Started or Stopped)?

**3. Linked Services**

Go to Target Data Factory → Manage → Linked Services.

Check:
- Are all required linked services present?
- Are they pointing to the correct environment?
- Are credentials, Key Vault references and managed identities configured correctly?
- Does the connection test succeed, where supported?

For example, the Test Data Factory should point to `test-sql-server`, not `dev-sql-server`.

Finally, we can run a safe test pipeline and check its execution in ADF Monitor.

## 6. Debugging Deployment Issues

**1. Deployment error messages**

If deployment fails:
- Open the Azure DevOps pipeline run.
- Find the failed deployment task.
- Read the error message in its logs.
- Check the ARM template, parameter file, resource references and permissions.
- Fix the actual issue and redeploy.

**2. Trigger still running or not restarted**

- Open the target Data Factory → Manage → Triggers.
- Check whether the trigger is Started or Stopped.
- Check the pre/post-deployment script logs.
- If necessary, correct the trigger state after confirming deployment is complete.

**3. Linked service pointing to the wrong environment**

Suppose Test is using the Development SQL Server.

- Open the linked service in the Test factory.
- Check the server and database names.
- Check the Test parameter file and deployment overrides.
- Correct the values and redeploy.

### Interview Scenario

**Interviewer:** Your ARM template deployment succeeded, but your pipeline fails when it runs in the Test environment. What will you check?

**Answer:**

First, I will check whether the pipeline and its activities were deployed correctly. Then I will verify the linked services to ensure they point to the Test environment and that their credentials, Key Vault references and managed identity permissions are correct. I will also check Integration Runtime and network connectivity if the connection fails. Finally, I will verify trigger configuration and run history in Monitor.

---

### Quick Revision

- **ARM template** → What resources should be deployed?
- **Parameter file** → What values should those resources use in each environment?
- **Pre-deployment script** → Stop triggers.
- **Deployment task** → Deploy ARM template.
- **Post-deployment script** → Restart triggers.
- **Approvals and checks** → Control whether deployment can proceed.
- **Variable groups** → Store reusable pipeline values.
- **Key Vault** → Securely store secrets.
- **Post-deployment verification** → Check pipelines, triggers and linked services.