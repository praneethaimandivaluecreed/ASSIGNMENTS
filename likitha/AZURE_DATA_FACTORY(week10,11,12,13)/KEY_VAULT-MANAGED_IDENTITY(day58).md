# Secrets, Connections and Integration Runtimes in Azure Data Factory

## 1. Azure Key Vault

### 1.1 What is Azure Key Vault?
- Azure Key Vault is a cloud service used to securely store and manage sensitive information.
- It prevents hardcoding credentials inside applications, pipelines and configuration files.
- ADF can retrieve credentials from Key Vault whenever it needs to connect to a data source.

**Example:** Instead of directly storing a database password inside a Linked Service, store it in Azure Key Vault and reference it from the Linked Service.

### 1.2 What can we store in Key Vault?

| Component | Purpose |
|---|---|
| Secrets | Passwords, API keys, connection strings and tokens |
| Keys | Encryption and decryption operations |
| Certificates | Digital certificates for authentication and secure communication |

### 1.3 Why do we use Azure Key Vault?
1. Centralized storage – Stores sensitive credentials in one secure location.
2. Secret rotation – Allows credentials to be updated or rotated without hardcoding them in applications.
3. Security – Only authorized identities can access secrets.
4. Auditing – Tracks access and operations performed on the vault.
5. Reduced secret exposure – Avoids storing passwords directly inside pipelines and configuration files.

### 1.4 How does Key Vault control access?

Before allowing anyone to access a secret, Azure checks:
1. Authentication – Who is requesting access?
2. Authorization – Does that identity have permission?

Azure uses Microsoft Entra ID (formerly Azure Active Directory) to identify users and applications.

**Two permission models:**

**A. Vault Access Policies (Traditional method)**
- Permissions are configured directly inside Key Vault.
- We specify which identity can perform which operations.
- Example: Allow ADF to read secrets.

**B. Azure Role-Based Access Control (RBAC)**
- Permissions are assigned using predefined Azure roles.
- Roles can be assigned to users, groups and Managed Identities.
- Provides centralized permission management.
- Recommended for modern Key Vault deployments.

**Common Key Vault RBAC roles:**

| Role | Permission |
|---|---|
| Key Vault Administrator | Full vault data-plane access and management |
| Key Vault Secrets Officer | Create, update and delete secrets |
| Key Vault Secrets User | Read secret contents |

**Remember:** ADF Managed Identity generally needs the `Key Vault Secrets User` role to retrieve secret values when using Azure RBAC.

---

## 2. Linked Services in ADF

### 2.1 What is a Linked Service?
- A Linked Service is a connection configuration in ADF.
- It tells ADF how to connect to a data source or destination.
- It contains connection details and authentication information.
- It can specify the Integration Runtime used for connectivity.

**Examples:**
- LS_AzureSQL → Connection to Azure SQL Database.
- LS_ADLS → Connection to Azure Data Lake Storage.
- LS_AzureKeyVault → Connection to Azure Key Vault.

### 2.2 Authentication types in Linked Services

| Authentication Type | Meaning |
|---|---|
| Managed Identity | Uses an Azure-managed identity without storing passwords |
| Service Principal | Uses a Microsoft Entra ID application identity |
| SQL / Basic Authentication | Uses username and password |
| Account Key | Uses a storage account access key |

**Service Principal requires:**
- Tenant ID
- Application (Client) ID
- Client Secret or Certificate

**Managed Identity requires:**
- No manually stored password.
- Azure manages the identity and token generation.

---

## 3. Managed Identity

### 3.1 What is Managed Identity?
- Managed Identity is an identity automatically managed by Azure for an Azure resource.
- It provides a digital identity to resources such as Azure Data Factory.
- It allows ADF to access other Azure services without storing usernames, passwords or client secrets.
- Azure handles token generation through Microsoft Entra ID.

**Example: ADF accessing ADLS**

1. ADF uses its Managed Identity.
2. Azure authenticates the identity through Microsoft Entra ID.
3. Entra ID issues an access token.
4. ADLS checks whether that identity has the required permissions.
5. If permission exists, ADF can access the files.

**Important:** Managed Identity handles authentication, but it does not automatically provide permissions to access other Azure resources.

We must explicitly grant the required permissions.

### 3.2 Types of Managed Identity

**A. System-Assigned Managed Identity**
- Created directly inside an Azure resource.
- Tied to that particular resource.
- Cannot be shared with other resources.
- Automatically deleted when the associated resource is deleted.

Example: ADF1 has its own System-Assigned Identity. If ADF1 is deleted, its identity is also deleted.

**B. User-Assigned Managed Identity**
- Created as a separate Azure resource.
- Can be attached to multiple Azure resources.
- Exists independently of the resources using it.
- Must be deleted separately when no longer required.

Example: One User-Assigned Identity can be attached to ADF1 and ADF2.

### 3.3 System-Assigned vs User-Assigned

| Feature | System-Assigned | User-Assigned |
|---|---|---|
| Creation | Automatically created when enabled | Created separately |
| Ownership | One Azure resource | Independent identity |
| Sharing | No | Yes |
| Lifecycle | Deleted with associated resource | Independent |
| Reusability | No | Yes |

**Easy way to remember:**
- System-assigned → Belongs to one resource.
- User-assigned → Separate identity that can be reused.

### 3.4 What happens when Managed Identity permission is missing?

Example: ADF tries to access ADLS using Managed Identity, but the identity does not have storage permissions.

Result: Access Denied (often HTTP 403).

**How to fix it:**
1. Identify the Managed Identity used by ADF.
2. Open the target Azure resource.
3. Go to Access Control (IAM).
4. Select Add role assignment.
5. Assign the appropriate role to the ADF Managed Identity.
6. Save and test the connection again.

**Common roles:**

| Resource | Required Access |
|---|---|
| ADLS / Blob Storage | Storage Blob Data Reader |
| ADLS / Blob Storage | Storage Blob Data Contributor |
| Key Vault | Key Vault Secrets User |
| Azure SQL | Appropriate database user and SQL permissions |

**Note:** Azure SQL permissions are generally granted inside the database, not simply by assigning a storage-style RBAC role.

### 3.5 Managed Identity as Federated Identity Credential (FIC)

- Federated Identity Credentials allow an application to trust an external identity provider without storing a client secret.
- A supported Managed Identity can be used as a trusted identity source for workload federation.
- This allows applications to obtain tokens without managing long-lived credentials.

**Remember:** Workload identity federation is not the same as directly granting an ADF Managed Identity access to ADLS or Key Vault.

---

## 4. Store Credentials in Key Vault and Reference Them from Linked Service

### 4.1 Practical implementation

**Goal:** Store a Storage Account connection string in Azure Key Vault and use it in an ADF Linked Service.

**Step 1: Create Azure Key Vault**
1. Open Azure Portal.
2. Search for Azure Key Vault.
3. Select Create.
4. Enter subscription, resource group, vault name and region.
5. Select the appropriate permission model.
6. Review and create the vault.

**Step 2: Store credentials as a Secret**
1. Open the Storage Account.
2. Go to Security + Networking → Access keys.
3. Copy the connection string (for this account-key authentication example).
4. Open Azure Key Vault.
5. Go to Objects → Secrets.
6. Select Generate/Import.
7. Enter a secret name, e.g. `StorageConnectionString`.
8. Paste the connection string as the secret value.
9. Create the secret.

**Step 3: Give ADF permission to read the secret**

If using Azure RBAC:
1. Open Key Vault.
2. Go to Access Control (IAM).
3. Select Add role assignment.
4. Select Key Vault Secrets User.
5. Select Managed Identity.
6. Choose the required Data Factory.
7. Review and assign.

If using Access Policies:
1. Open Key Vault → Access Policies.
2. Add an access policy.
3. Select Get (and List if required) under Secret permissions.
4. Select the ADF Managed Identity.
5. Save the policy.

**Step 4: Create a Key Vault Linked Service in ADF**
1. Open ADF Studio.
2. Go to Manage → Linked Services.
3. Select New.
4. Search for Azure Key Vault.
5. Select the Key Vault.
6. Configure authentication using ADF Managed Identity.
7. Select the required Key Vault URL.
8. Test the connection and create the Linked Service.

Example name: `LS_AzureKeyVault`.

**Step 5: Create the Storage Linked Service**
1. Go to Manage → Linked Services.
2. Select New → Azure Blob Storage or ADLS Gen2, depending on the storage service.
3. Enter the storage account details.
4. Select Account Key authentication for this example.
5. Select Azure Key Vault as the credential source.
6. Select the Key Vault Linked Service (`LS_AzureKeyVault`).
7. Select the secret name (`StorageConnectionString`).
8. Save and test the connection.

Example name: `LS_ADLS`.

**Step 6: Create the Dataset**
1. Go to Author → Datasets.
2. Create a dataset for the required storage service.
3. Select the Storage Linked Service (`LS_ADLS`).
4. Configure the file system/container and file details.
5. Save the dataset.

### 4.2 Complete connection flow

ADF Pipeline → Dataset → Storage Linked Service → Key Vault Linked Service → Azure Key Vault → Azure Storage.

**Important points:**
- First create the Key Vault Linked Service.
- Then create the actual storage/database Linked Service.
- The storage Linked Service references the secret in Key Vault.
- The Dataset references the storage Linked Service.
- The Pipeline uses the Dataset.

**Main benefit:** If the credential changes, we can update the secret in Key Vault instead of hardcoding the new credential in multiple Linked Services.

**Note:** This is an account-key example. Managed Identity is generally preferable for supported Azure-to-Azure connections because it avoids storing long-lived storage credentials.

---

## 5. Integration Runtime in Practice

### 5.1 What is Integration Runtime?

- Integration Runtime (IR) is the infrastructure used by ADF to provide connectivity and execute data integration activities.
- It acts as a bridge between data sources and destinations.
- It is responsible for supported data movement and activity execution.

### 5.2 Types of Integration Runtime

| Type | Usage |
|---|---|
| Azure IR | Cloud-to-cloud data movement and supported activities |
| Self-hosted IR | On-premises and private network connectivity |
| Azure-SSIS IR | Running SSIS packages in Azure |

### 5.3 Which IR does a Linked Service use?

- A Linked Service defines how to connect to a data source.
- It can specify the Integration Runtime used for the connection.
- AutoResolve Azure IR can also be used.
- The required IR depends on the connector, source location and network architecture.

**Examples:**
- LS_AzureSQL → AutoResolve Azure IR → Azure SQL Database.
- LS_OnPremSQL → Self-hosted IR → On-premises SQL Server.

**Where to check?**
1. Open ADF Studio.
2. Go to Manage.
3. Open Integration Runtimes to view available IRs.
4. Open the required Linked Service under Manage → Linked Services.
5. Check its Integration Runtime configuration.

### 5.4 Checking Self-hosted IR Status

| Status | Meaning |
|---|---|
| Online | IR is connected and available |
| Offline | IR is unavailable or disconnected |
| Update needed | IR requires an update |

**Debugging Offline IR:**
1. Check IR status in ADF Studio.
2. Check whether the hosting machine is switched on.
3. Check whether the IR Windows service is running.
4. Check network connectivity and firewall.
5. Ask the infrastructure team to resolve the issue if required.

**Remember:** An offline Self-hosted IR can cause dependent pipeline activities to fail.

---

## 6. Debugging Connection Failures

### 6.1 Test Connection Failure

Test Connection checks whether ADF can establish a connection using the Linked Service configuration.

**Possible reasons:**
- Incorrect server or database details.
- Invalid username/password.
- Expired or disabled secret.
- Missing permissions.
- Firewall or network restrictions.
- Offline Integration Runtime.

### 6.2 Expired Secrets

**Problem:** ADF is trying to use an invalid or expired credential.

**Check:**
- Key Vault secret expiration.
- Secret enabled/disabled status.
- Whether the database password has changed.
- Whether ADF can retrieve the latest secret.

**Solution:** Update the secret and verify Key Vault permissions.

### 6.3 Firewall / Network Issues

**Problem:** ADF cannot reach the source or destination.

**Check:**
- Firewall rules.
- Allowed IP addresses.
- Private endpoint configuration.
- DNS resolution.
- Network connectivity from the selected IR.

**Solution:** Contact the Network Administrator or Infrastructure Team.

### 6.4 Access Denied (403)

**Problem:** ADF reaches the resource but does not have the required permissions.

**Check:**
- Which Managed Identity is being used?
- Does it have the required RBAC role?
- Are the required ACLs configured?
- Does the database identity have the required SQL permissions?

**Solution:** Request the appropriate permission from the resource administrator.

### 6.5 Offline Self-hosted IR

**Problem:** ADF cannot communicate with the required Self-hosted IR.

**Check:**
- IR status.
- Hosting machine.
- IR Windows service.
- Network and firewall connectivity.
- IR version and registration.

**Solution:** Contact the Infrastructure / Server Administrator.

### 6.6 Quick Debugging Table

| Error | What to investigate |
|---|---|
| Authentication failed | Credentials and authentication method |
| Secret access failed | Key Vault permissions |
| Connection timeout | Network and firewall |
| 403 Access Denied | RBAC, ACL or SQL permissions |
| IR unavailable | Self-hosted IR status |
| DNS error | DNS and private endpoint |

**My debugging order:**
1. Check Linked Service configuration.
2. Check authentication and credentials.
3. Check Key Vault secret.
4. Check Integration Runtime.
5. Check network and firewall.
6. Check permissions.

---

## 7. Who to Ask for What?

As a Data Engineer, I may not have administrative permissions for every Azure resource.

I should identify the issue and contact the appropriate administrator.

### 7.1 Storage Access

**Problem:** ADF cannot read/write files in ADLS.

**Contact:** Storage Administrator / Cloud Infrastructure Team.

### 7.2 Database Access

**Problem:** ADF cannot read/write database tables.

**Contact:** Database Administrator (DBA).

### 7.3 Key Vault Access

**Problem:** ADF cannot retrieve secrets.

**Contact:** Key Vault Administrator / Security Team.

### 7.4 Quick Reference

| Resource | Who to contact? |
|---|---|
| ADLS / Blob Storage | Storage Administrator |
| Azure SQL Database | DBA |
| Azure Key Vault | Security / Key Vault Administrator |
| Self-hosted IR | Infrastructure / Server Administrator |
| Firewall | Network Administrator |
| Linked Service configuration | Data Engineer |

---

## 9. Final Revision – Important Things to Remember

| Concept | Remember |
|---|---|
| Azure Key Vault | Securely stores secrets, keys and certificates |
| Secret | Stores passwords, connection strings and API keys |
| Access Policy | Traditional Key Vault permission model |
| Azure RBAC | Role-based permission management |
| Managed Identity | Azure-managed identity without manually managed credentials |
| System-Assigned | Belongs to one resource |
| User-Assigned | Independent and reusable |
| Service Principal | Application identity with credentials or federation |
| Linked Service | Defines how to connect to a resource |
| Dataset | Defines the data structure and location |
| Integration Runtime | Provides connectivity and execution infrastructure |
| Self-hosted IR | Used for private network connectivity |

**My main learning:**
- Never hardcode sensitive credentials when a secure alternative is available.
- Prefer Managed Identity for supported Azure-to-Azure connections.
- Authentication and authorization are two different things.
- Always check the Linked Service, credentials, IR, network and permissions when debugging.
- Know which administrator to contact when access is missing.

## 10. Learning References

1. Azure Key Vault Tutorial – https://www.datacamp.com/tutorial/azure-key-vault-tutorial
2. Video tutorial – https://youtu.be/9BawMq0CVbs
3. Microsoft: Store credentials in Azure Key Vault – https://learn.microsoft.com/en-us/azure/data-factory/store-credentials-in-key-vault
4. Microsoft: Key Vault RBAC vs Access Policies – https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-access-policy
5. Microsoft: Integration Runtime – https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime
6. Microsoft: ADF Troubleshooting Guide – https://learn.microsoft.com/en-us/azure/data-factory/data-factory-troubleshoot-guide
