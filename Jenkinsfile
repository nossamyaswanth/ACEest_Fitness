pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '7337432133/aceest_fitness'
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '. venv/bin/activate && pytest -v --disable-warnings'
            }
        }

        stage('Code Quality (SonarQube)') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh """
                    sonar-scanner \
                      -Dsonar.projectKey=ACEest_Fitness \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_HOST_URL \
                      -Dsonar.login=$SONAR_AUTH_TOKEN
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:${BUILD_NUMBER} .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_IMAGE:${BUILD_NUMBER}
                    docker tag $DOCKER_IMAGE:${BUILD_NUMBER} $DOCKER_IMAGE:latest
                    docker push $DOCKER_IMAGE:latest
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG_FILE
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/aceest-fitness
                    '''
                }
            }
        }
    }

    post {
        success { echo '✅ Pipeline completed successfully!' }
        failure { echo '❌ Pipeline failed! Check logs for errors.' }
    }
}
