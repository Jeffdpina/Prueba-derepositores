
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}

provider "azurerm" {
  features {

  }
}


# create a resource group
resource "azurerm_resource_group" "rg" {
  name = "rg-storageaccount-file-uploader-rx"
  location = "East US"
}

# Create an storage account

resource "azurerm_storage_account" "storage_account" {
  name = "demox2025uploaderx"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  account_tier = "Standard"
  account_replication_type = "LRS"
}