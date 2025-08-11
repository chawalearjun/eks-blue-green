pipeline {
    agent any
    environment {
        DOCKER_USER = "arjun16"  // Change this
        AWS_REGION = "us-east-1"
        SERVICE_NAME = "demo-service"
    }
    stages {
        stage('Detect Live Version') {
            steps {
                script {
                    // Get current live version from Kubernetes Service
                    LIVE_VERSION = sh(
                        script: "kubectl get service ${SERVICE_NAME} -o jsonpath='{.spec.selector.version}'",
                        returnStdout: true
                    ).trim()

                    if (LIVE_VERSION == "blue") {
                        IDLE_VERSION = "green"
                    } else if (LIVE_VERSION == "green") {
                        IDLE_VERSION = "blue"
                    } else {
                        error "Unknown live version: ${LIVE_VERSION}"
                    }

                    echo "Current live version: ${LIVE_VERSION}"
                    echo "Idle version to update: ${IDLE_VERSION}"
                }
            }
        }

        stage('Build Docker Image for Idle Version') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_USER}/${IDLE_VERSION}-app:${BUILD_NUMBER} app/${IDLE_VERSION}"
                    sh "docker push ${DOCKER_USER}/${IDLE_VERSION}-app:${BUILD_NUMBER}"
                }
            }
        }

        stage('Update Idle Deployment') {
            steps {
                script {
                    sh "kubectl set image deployment/app-${IDLE_VERSION} node-app=${DOCKER_USER}/${IDLE_VERSION}-app:${BUILD_NUMBER} --record"
                }
            }
        }

        stage('Switch Traffic to Idle Version') {
            steps {
                script {
                    sh "python scripts/setup_all.py --switch ${IDLE_VERSION}"
                    echo "Traffic switched to ${IDLE_VERSION} version"
                }
            }
        }
    }
}
