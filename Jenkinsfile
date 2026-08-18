pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "manalitekawade0804/nodejsapp"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'

                sh """
                    docker build \
                    -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                    -t ${DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub...'

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
                echo 'Pushing image to Docker Hub...'

                sh """
                    docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying application to Kubernetes...'

                sh """
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    kubectl set image deployment/nodejsapp \
                    nodejsapp=${DOCKER_IMAGE}:${IMAGE_TAG}

                    kubectl rollout status deployment/nodejsapp
                """
            }
        }
    }

    post {

        success {
            echo "===================================="
            echo "Pipeline completed successfully!"
            echo "Docker Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            echo "===================================="
        }

        failure {
            echo "Pipeline failed. Check Jenkins console output."
        }

        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
