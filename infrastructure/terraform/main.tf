provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "edu" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Academic Hub (Shared Services) ---

resource "azurerm_virtual_network" "hub" {
  name                = "vnet-academic-hub-${var.environment}"
  location            = azurerm_resource_group.edu.location
  resource_group_name = azurerm_resource_group.edu.name
  address_space       = ["10.0.0.0/16"]
}

# --- Governance Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "edu_k8s" {
  name                = "aks-edu-governance-${var.environment}"
  location            = azurerm_resource_group.edu.location
  resource_group_name = azurerm_resource_group.edu.name
  dns_prefix          = "edu-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Institutional Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "edu" {
  name                   = "psql-edu-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.edu.name
  location               = azurerm_resource_group.edu.location
  version                = "13"
  administrator_login    = "eduadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Secure Institutional Vault (Key Vault) ---

resource "azurerm_key_vault" "vault" {
  name                        = "kv-edu-${var.environment}"
  location                    = azurerm_resource_group.edu.location
  resource_group_name         = azurerm_resource_group.edu.name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}

# --- Research Compute Storage (AWS S3) ---

resource "aws_s3_bucket" "research_data" {
  bucket = "db-edu-research-data-${var.environment}"
}
