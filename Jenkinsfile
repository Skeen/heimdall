pipeline {
  agent {
    docker {
      image 'debian:stretch'
      args '--user 0:0'
    }
    
  }
  stages {
    stage('Prepare for provisioning') {
      parallel {
        stage('Prepare for provisioning') {
          steps {
            echo 'Preparing machine for provisioning'
            sh 'echo "deb http://ftp.debian.org/debian stretch-backports main" > /etc/apt/sources.list.d/strecth-backports.list'
            sh 'apt-get update'

            timeout(time: 5, unit: 'MINUTES') {
              sh 'apt-get install -t stretch-backports -y ansible'
            }
            sh 'ansible --version'

            timeout(unit: 'MINUTES', time: 3) {
              sh 'apt-get install -y git'
            }
            sh 'git --version'

            echo 'Preparing django user'
            sh '''
                apt-get install sudo
                useradd -m django
                usermod -a -G sudo django
            '''

            echo 'Chmodding workspace'
            sh '''
                chown django:django -R *
            '''
          }
        }
        stage('Are we UNIX?') {
          steps {
            isUnix()
          }
        }
        stage('Setting GitHub statuses pending') {
          steps {
            githubNotify(context: 'Documentation', description: "Pipeline build ${env.JOB_NAME} #${env.BUILD_ID} in progress...", status: 'PENDING')
            githubNotify(context: 'Checking', description: "Pipeline build ${env.JOB_NAME} #${env.BUILD_ID} in progress...", status: 'PENDING')
            githubNotify(context: 'Unit-Tests', description: "Pipeline build ${env.JOB_NAME} #${env.BUILD_ID} in progress...", status: 'PENDING')
            githubNotify(context: 'Coverage', description: "Pipeline build ${env.JOB_NAME} #${env.BUILD_ID} in progress...", status: 'PENDING')
            githubNotify(context: 'E2E-Tests', description: "Pipeline build ${env.JOB_NAME} #${env.BUILD_ID} in progress...", status: 'PENDING')
          }
        }
      }
    }
    stage('Provisioning') {
      steps {
        echo '# Install the playbook requirements'
        sh '''
            # Ansible variables
            ROLES_PATH=$PWD/ansible/roles/
            REQUIREMENTS_PATH=$PWD/ansible/requirements.yml

            # Install the playbook requirements
            ANSIBLE_STDOUT_CALLBACK=debug ANSIBLE_ROLES_PATH=$ROLES_PATH PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true \\
            ansible-galaxy install -r $REQUIREMENTS_PATH
        '''

        echo '# Run the playbook'
        sh '''
            PLAYBOOK=test.yml

            # Ansible variables
            ROLES_PATH=$PWD/ansible/roles/
            PLAYBOOK_PATH=$PWD/ansible/playbooks/$PLAYBOOK

            # Run the playbook
            ANSIBLE_STDOUT_CALLBACK=debug ANSIBLE_ROLES_PATH=$ROLES_PATH PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true \\
            ansible-playbook --timeout=30 -vv -i "localhost," -c local $PLAYBOOK_PATH \\
                -e virtualenv_user=django \\
                -e pip_req_path=$PWD/src \\
                -e project_source=$PWD/src/ \\
                -e nodejs_user=django \\
                -e adminapp_packagejson_folder=$PWD/src/adminapp/frontend \\
                -e webapp_packagejson_folder=$PWD/src/webapp/frontend
        '''
      }
    }
    stage('Unit-Testing') {
      parallel {
        stage('Unit-Tests') {
          steps {
            script {
              TESTS_PASSED = sh([
                script: '''
                    cd src/
                    . /home/django/venv/bin/activate
                    TASK=UBS ../jenkins/inside_vm.sh
                ''',
                returnStatus: true
              ]) == 0
              if ( TESTS_PASSED ) {
                  githubNotify(context: 'Unit-Tests', description: "Unit-Tests passed", status: 'SUCCESS')
              } else {
                  githubNotify(context: 'Unit-Tests', description: "Unit-Tests failed", status: 'ERROR')
                  script {
                      error 'FAIL'
                  }
              }
            }

            script {
              COVERAGE_PERCENT = sh([
                script: '''
                    cd src/
                    . /home/django/venv/bin/activate
                    coverage report | grep "TOTAL" | grep -o "[0-9]*%"
                ''',
                returnStdout: true
              ]).trim()
              if ( COVERAGE_PERCENT == "100%" ) {
                  githubNotify(context: 'Coverage', description: "100% Code Coverage", status: 'SUCCESS')
              } else {
                  githubNotify(context: 'Coverage', description: "${COVERAGE_PERCENT} Code Coverage", status: 'ERROR')
                  /*script {
                      error 'FAIL'
                  }*/
              }
            }

            junit 'reports/test/'
            cobertura(coberturaReportFile: 'reports/coverage.xml')
            publishHTML(target: [
              allowMissing: false,
              alwaysLinkToLastBuild: false,
              keepAll: true,
              reportDir: 'reports/coverage_html',
              reportFiles: 'index.html',
              reportName: "Coverage",
              reportTitles: "Coverage"
            ])
          }
        }
      }
    }
    stage('Testing') {
      parallel {
        stage('Documentation') {
          steps {
            script {
              DOCUMENTATION_OK = sh([
                script: '''
                    cd src/
                    . /home/django/venv/bin/activate
                    TASK=Documentation ../jenkins/inside_vm.sh
                ''',
                returnStatus: true
              ]) == 0
              if ( DOCUMENTATION_OK ) {
                  githubNotify(context: 'Documentation', description: "Checking passed", status: 'SUCCESS')
              } else {
                  githubNotify(context: 'Documentation', description: "Checking failed", status: 'ERROR')
            script {
            error 'FAIL'
            }
              }
            }

            publishHTML(target: [
              allowMissing: false,
              alwaysLinkToLastBuild: false,
              keepAll: true,
              reportDir: 'reports/docs/html',
              reportFiles: 'index.html',
              reportName: "Documentation",
              reportTitles: "Documentation"
            ])
          }
        }
        stage('E2E-Tests') {
          steps {
            script {
              TESTS_PASSED = sh([
                script: '''
                    set +e

                    cd src/
                    . /home/django/venv/bin/activate

                    python manage.py EndToEndTests
                    TEST_STATUS=$?

                    echo "Moving test report"
                    mv adminapp/frontend/res.xml ../reports/e2e-test.xml

                    echo "Exiting with test status"
                    exit $TEST_STATUS
                ''',
                returnStatus: true
              ]) == 0
              if ( TESTS_PASSED ) {
                  githubNotify(context: 'E2E-Tests', description: "E2E-Tests passed", status: 'SUCCESS')
              } else {
                  githubNotify(context: 'E2E-Tests', description: "E2E-Tests failed", status: 'ERROR')
                  script {
                      error 'FAIL'
                  }
              }
            }

            junit 'reports/e2e-test.xml'
          }
        }
        stage('Checking') {
          steps {
            script {
              CHECKING_OK = sh([
                script: '''
                    cd src/
                    . /home/django/venv/bin/activate
                    TASK=Checking ../jenkins/inside_vm.sh
                ''',
                returnStatus: true
              ]) == 0
              if ( CHECKING_OK ) {
                  githubNotify(context: 'Checking', description: "Checking passed", status: 'SUCCESS')
              } else {
                  githubNotify(context: 'Checking', description: "Checking failed", status: 'ERROR')
                  script {
                      error 'FAIL'
                  }
              }
            }
          }
        }
      }
    }
    stage('error') {
      steps {
        cleanWs(cleanWhenAborted: true, cleanWhenFailure: true, cleanWhenNotBuilt: true, cleanWhenSuccess: true, cleanWhenUnstable: true, cleanupMatrixParent: true, deleteDirs: true, notFailBuild: true)
      }
    }
  }
  post {
    always {
      echo "Cleaning up the workspace"
      cleanWs()
    }
    success {
      echo 'I succeeeded!'
    }
    unstable {
      echo 'I am unstable :/'
    }
    failure {
      echo 'I failed :('
    }
    changed {
      echo 'Things were different before...'
    }
  }
  environment {
    DEBIAN_FRONTEND = 'noninteractive'
  }
}
