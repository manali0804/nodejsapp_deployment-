pipeline {
    agent any

    environment {
        IMAGE_NAME = "manalitekawade0804/devops-api"
        IMAGE_TAG  = "1.0"
        NAMESPACE  = "devops-demo"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running application tests...'
                sh '''
                    python3 -m py_compile app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build --network=host \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Test') {
            steps {
                echo 'Verifying Docker image...'
                sh '''
                    docker image inspect ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging in to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhubcred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'

                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying application to Kubernetes...'

                sh '''
                    kubectl apply -f k8/namespace.yaml
                    kubectl apply -f k8/deployment.yaml
                    kubectl apply -f k8/service.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Checking Kubernetes deployment...'

                sh '''
                    kubectl rollout status deployment/devops-api \
                        -n ${NAMESPACE} \
                        --timeout=120s

                    kubectl get pods -n ${NAMESPACE}
                    kubectl get service -n ${NAMESPACE}
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Jenkins logs.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
