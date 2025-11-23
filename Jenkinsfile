pipeline {
    agent any

    environment {
        // Pull BrowserStack creds from Jenkins credentials store
        BROWSERSTACK_USERNAME   = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull code from the repo Jenkins is configured with
                checkout scm
            }
        }

        stage('Set up Python env') {
            steps {
                sh '''
                  python3 -m venv env
                  . env/bin/activate

                  # Minimal dependencies – avoids the pyobjc build pain on macOS
                  pip install --upgrade pip
                  pip install pytest selenium browserstack-sdk
                '''
            }
        }

        stage('Run tests on BrowserStack') {
            steps {
                sh '''
                  . env/bin/activate
                  browserstack-sdk python -m pytest -q
                '''
            }
        }
    }

    post {
        always {
            // Optional: collect any pytest XML reports later if you add them
            archiveArtifacts artifacts: '**/pytest*.xml', allowEmptyArchive: true
        }
    }
}
