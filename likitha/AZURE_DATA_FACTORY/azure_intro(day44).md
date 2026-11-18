Azure Essentials for ADF Users
Topic: Incremental Load Patterns – Azure Essentials
1. Navigating Azure Portal
- Subscription: Billing and management boundary where Azure resources are created.
- Resource Group: A logical container used to organize related resources (ADF, Storage Account, SQL Database).
- Region: Geographical location where a resource is deployed (Central India, South India, etc.).
- To find ADF or Storage Account, check the correct subscription → resource group → resource name.
- Resources inside the same resource group can exist in different regions. Resource group region and resource region need not be the same.
- Azure CLI commands:
az account list --output table   # List subscriptions
az account show                 # Current subscription
az account set --subscription "ID"  # Switch subscription


2. Azure Storage Basics
Azure Storage is used to store raw files and processed data in data engineering pipelines.
- Container: A logical storage area inside a storage account.
- Folder: Used to organize files inside a container (often represented as a path, not a real folder).
- File: Actual data stored, such as CSV, JSON, Parquet, etc.
Example storage structure:
Storage Account
   └── Container: raw
         └── Folder: sales
               ├── customers.csv
               └── orders.csv


- Azure Storage Explorer: A tool used to browse storage accounts, containers, folders and files, upload/download files and check whether pipeline output exists.
3. Permissions (RBAC)
- RBAC (Role-Based Access Control): Controls who can access Azure resources and what actions they can perform.
- Storage Blob Data Contributor: Allows reading, writing and deleting blob data in Azure Storage at the assigned scope.
- A Data Factory's Managed Identity is its automatically managed identity used to access other Azure services without storing passwords.
- If ADF uses Managed Identity to access Storage, that identity must have the required storage permissions.
- Having access to ADF does NOT automatically give access to Storage Account.
Common Azure roles:
- Reader → View resources.
- Contributor → Create, update and delete Azure resources, but cannot generally assign RBAC roles.
- Owner → Full resource management, including assigning roles.
- Storage Blob Data Contributor → Read, write and delete blob data.
4. When an Azure Resource Is Missing
Check these before assuming the resource is deleted:
1. Subscription: Are you searching in the correct subscription?
2. Resource Group: Is the resource inside another resource group?
3. Resource Name: Are you using the correct name?
4. Region: Is the resource deployed in another region?
Important: A resource group and its resources can have different regions. Resources in one resource group do not have to be in the same region.
5. Debugging 403 vs 404 Errors
Error	Meaning	What to check
403 Forbidden	Insufficient permission	RBAC role, identity and permission scope
404 Not Found	Requested resource/path not found	Resource name, endpoint, container, folder and file path

- 403: Check which identity is accessing the resource and whether it has the required permission. For example, assign Storage Blob Data Contributor to the ADF Managed Identity if required.
- 404: Check whether the resource or requested file actually exists and whether the endpoint or path is correct.
- A 404 does not always mean the entire Azure resource is missing; sometimes only the file or endpoint is missing.
- Always identify whether the error comes from Azure Resource Manager, Storage or an API.
6. Azure Housekeeping
Naming conventions: Use meaningful and consistent names.

Examples:
- rg-sales-dev → Resource Group
- adf-sales-dev → Data Factory
- stsalesdev001 → Storage Account
Use dev, test, prod to identify environments. Follow individual Azure resource naming rules.

Tags: Key-value pairs attached to resources to organize and track them.

Examples:
- Environment = Dev
- Project = Sales
- Owner = DataTeam
Tags help with cost tracking, resource organization and ownership. They are metadata, not resource names. Resource group tags are NOT automatically inherited by resources. Never store passwords or secrets in tags.

Deleting resources:
- Deleting an individual resource → Only that resource is deleted.
- Deleting a resource group → All resources inside it are deleted.
- Before deleting, check important data, dependencies, backups, resource locks and permissions. Deletion may be irreversible.

Important Points to Remember ⭐
1. Subscription = Management and billing boundary; Resource Group = Resource container.
2. Resource group location and resource location can be different.
3. ADF Managed Identity needs appropriate permissions to access Storage.
4. Storage Blob Data Contributor = Read + Write + Delete blob data.
5. 403 = Permission issue; 404 = Resource, file, path or endpoint not found.
6. ADF access does not automatically mean Storage access.
7. Naming makes resources identifiable; Tags help organize and track them.
8. Deleting a resource group deletes everything inside it.