pipeline {
    agent any

    environment {
        // Fetches the secret from Jenkins Credentials manager (ID: hf-token-secret)
        HF_TOKEN = credentials('hf-token-secret')
        IMAGE_NAME = 'cloudops-copilot-app'
        CONTAINER_NAME = 'cloudops-app-container'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Dannyyy7/Cloudops-copilot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    echo "Stopping old container if running..."
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"

                    echo "Starting new container with HF_TOKEN..."
                    sh """
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p 8501:8501 \
                          -e HF_TOKEN=${HF_TOKEN} \
                          --restart unless-stopped \
                          ${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful! App is running at http://<EC2_PUBLIC_IP>:8501"
        }
        failure {
            echo "Pipeline failed. Check build logs for details."
        }
    }
}
