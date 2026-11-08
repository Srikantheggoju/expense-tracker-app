pipeline {
    agent any

    environment {
        IMAGE_NAME = "srikantheggoju/expense-tracker"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Srikantheggoju/expense-tracker-app.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=expense-tracker \
                    -Dsonar.sources=.
                    '''
                }
            }
        }

        stage('Trivy FS Scan') {
            steps {
                sh 'trivy fs .'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh 'trivy image $IMAGE_NAME:$IMAGE_TAG'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                docker push $IMAGE_NAME:latest
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
