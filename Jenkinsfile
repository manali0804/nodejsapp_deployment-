ipipeline {

    agent any

    environment {
        DOCKER_IMAGE = "YOUR_DOCKERHUB_USERNAME/devops-app"
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."

                sh """
                    docker build \
                    -t ${DOCKER_IMAGE}:${DOCKER_TAG} \
                    -t ${DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging into Docker Hub..."

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                        -u "$DOCKER_USERNAME" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Pushing Docker image to Docker Hub..."

                sh """
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes..."

                sh """
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    kubectl set image deployment/devops-app \
                    devops-app=${DOCKER_IMAGE}:${DOCKER_TAG}

                    kubectl rollout status deployment/devops-app
                """
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
            echo "Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }

        failure {
            echo "Pipeline failed. Check Jenkins console logs."
        }

        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
