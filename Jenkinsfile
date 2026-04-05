pipeline {
    agent any
    
    environment {
        ARM_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        ARM_CLIENT_ID       = credentials('AZURE_CLIENT_ID')
        ARM_CLIENT_SECRET   = credentials('AZURE_CLIENT_SECRET')
        ARM_TENANT_ID       = credentials('AZURE_TENANT_ID')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Pobieram najnowszy kod z GitHub...'
                git branch: 'main', url: 'https://github.com/k1marzec/devops-portfolio-app.git'
            }
        }

        stage('Setup Terraform') {
            steps {
                echo 'Przygotowuję binarkę Terraforma...'
                sh '''
                    curl -LO https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    
                    unzip -o terraform_1.5.7_linux_amd64.zip -d terraform/
                '''
            }
        }
        
        stage('Terraform Init & Plan') {
            steps {
                echo 'Uruchamiam planowanie infrastruktury na Azure...'
                sh '''
                    cd terraform/
                    
                    chmod +x terraform
                    
                    ./terraform init 
                    ./terraform plan
                    ./terraform apply --auto-approve
                '''
            }
        }
    }
}
