terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "test_rg" {
  name     = "rg-terraform-karolina"
  location = "West Europe"
}

resource "random_integer" "suffix" {
  min = 10000
  max = 99999
}

resource "azurerm_service_plan" "todo_plan" {
  name                = "plan-todo-app-free"
  resource_group_name = azurerm_resource_group.test_rg.name
  location            = azurerm_resource_group.test_rg.location
  os_type             = "Linux"
  sku_name            = "F1" 
}

resource "azurerm_linux_web_app" "todo_app" {
  name                = "todo-app-karolina-${random_integer.suffix.result}" 
  resource_group_name = azurerm_resource_group.test_rg.name
  location            = azurerm_resource_group.test_rg.location
  service_plan_id     = azurerm_service_plan.todo_plan.id

  site_config {
    always_on = false 
    application_stack {
      docker_image_name = "k1marzec/devops-portfolio-app:latest"
    }
  }

  app_settings = {
    "WEBSITES_PORT" = "5000" 
  }
}



output "app_url" {
  value = "https://${azurerm_linux_web_app.todo_app.default_hostname}"
}
