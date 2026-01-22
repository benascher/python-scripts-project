pipeline {
    agent any

    environment {
        S3_BUCKET = "python-scripts12"
        LAMBDA_CSV = "convert_csv_to_excel"
        LAMBDA_WIKI = "wiki_fetcher"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Detect Changes') {
            steps {
                script {
                    // Find which files changed in the last commit
                    changedFiles = sh(
                        script: "git diff --name-only HEAD~1 HEAD",
                        returnStdout: true
                    ).trim().split("\n")

                    echo "Changed files: ${changedFiles}"

                    // Conditions
                    UI_CHANGED = changedFiles.any { it.startsWith("website/") }
                    LAMBDA_CHANGED = changedFiles.any { it.startsWith("lambda_function/") }

                    echo "UI_CHANGED=${UI_CHANGED}"
                    echo "LAMBDA_CHANGED=${LAMBDA_CHANGED}"
                }
            }
        }

        stage('Run Tests (Only if Lambda Changed)') {
            when {
                expression { LAMBDA_CHANGED }
            }
            steps {
			  sh """
              export PYTHONPATH=\$PYTHONPATH:$(pwd)
              pytest tests/
              """
            }
        }

        stage('Package Lambda (Only if Lambda Changed)') {
            when {
                expression { LAMBDA_CHANGED }
            }
            steps {
                sh '''
                cd lambda
                zip -r lambda.zip .
                '''
            }
        }

        stage('Deploy Lambda (Only if Lambda Changed)') {
            when {
                expression { LAMBDA_CHANGED }
            }
            steps {
                sh '''
                aws lambda update-function-code \
                    --function-name $LAMBDA_CSV \
                    --zip-file fileb://lambda/lambda.zip
                '''
            }
        }

        stage('Deploy UI (Only if UI Changed)') {
            when {
                expression { UI_CHANGED }
            }
            steps {
                sh """
                aws s3 sync website/ s3://$S3_BUCKET/ --delete
                """
            }
        }
    }

    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}

