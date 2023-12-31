// Active Choices plugin required
properties([
    parameters([
        [$class: 'ChoiceParameter', 
            choiceType: 'PT_SINGLE_SELECT', 
            description: 'Select Deployment Env from the Dropdown List', 
            filterLength: 1, 
            filterable: true, 
            name: 'deploy_env', 
            randomName: 'choice-parameter-adviser-deploy-env', 
            script: [
                $class: 'GroovyScript', 
                fallbackScript: [
                    classpath: [], 
                    sandbox: false,
                    script: 
                        'return[\'Could not get deploy_env\']'
                ], 
                script: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        'return["devtest","uat","prod"]'
                ]
            ]
        ], 
        [$class: 'CascadeChoiceParameter', 
            choiceType: 'PT_SINGLE_SELECT', 
            description: 'Select kube config from the Dropdown List', 
            filterLength: 1, 
            filterable: false, 
            name: 'kubeconfigMap',
            randomName: 'choice-parameter-adviser-kubeconfigMap', 
            referencedParameters: 'deploy_env', 
            script: [
                $class: 'GroovyScript', 
                fallbackScript: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        'return[\'Could not get Environment from deploy_env Param\']'
                ], 
                script: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        ''' if (deploy_env.equals("devtest")){
                                return["kube-config-exrates-k8s-name"]
                            }
                            else if(deploy_env.equals("uat")){
                                return["kube-config-exrates-k8s-name"]
                            }
                            else if(deploy_env.equals("prod")){
                                return["kube-config-exrates-k8s-name"]
                            }
                        '''
                ]
            ]
        ],
        [$class: 'CascadeChoiceParameter', 
            choiceType: 'PT_SINGLE_SELECT', 
            description: 'Run helm rollout if deployment failed', 
            filterLength: 1, 
            filterable: false, 
            name: 'ROLLOUT_IF_FAILED', 
            randomName: 'choice-parameter-adviser-ROLLOUT_IF_FAILED', 
            referencedParameters: 'deploy_env', 
            script: [
                $class: 'GroovyScript', 
                fallbackScript: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        'return[\'Could not get Environment from deploy_env Param\']'
                ], 
                script: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        ''' if (deploy_env.equals("devtest")){
                                return["yes", "no"]
                            }
                            else if(deploy_env.equals("uat")){
                                return["yes", "no"]
                            }
                            else if(deploy_env.equals("prod")){
                                return["yes", "no"]
                            }
                        '''
                ]
            ]
        ],
        [$class: 'CascadeChoiceParameter', 
            choiceType: 'PT_SINGLE_SELECT', 
            description: 'Configure RBAC for Developers', 
            filterLength: 1, 
            filterable: false, 
            name: 'ConfigureDevRBAC', 
            randomName: 'choice-parameter-adviser-ConfigureDevRBAC', 
            referencedParameters: 'deploy_env', 
            script: [
                $class: 'GroovyScript', 
                fallbackScript: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        'return[\'Could not get Environment from deploy_env Param\']'
                ], 
                script: [
                    classpath: [], 
                    sandbox: false, 
                    script: 
                        ''' if (deploy_env.equals("devtest")){
                                return["no", "yes"]
                            }
                            else if(deploy_env.equals("uat")){
                                return["no"]
                            }
                            else if(deploy_env.equals("prod")){
                                return["no"]
                            }
                        '''
                ]
            ]
        ]
    ])
])

jenkins_pipeline_library_version = "master"
library "jenkins-pipeline-library@${jenkins_pipeline_library_version}"

def generated_label = "adviser-${UUID.randomUUID().toString()}"
def service_name = "adviser"
def kubeconfigMountPath = "/kubeconfig"
def podMemoryRequests = '3Gi'
def podCPURequests = '1'

def get_services(job) {
    if (job == 'all'){
      return ["adviser"]
    } else if (job == 'pods_only'){
      return ["adviser"]
    }else{
      return [job]
    }
}

def parallelStagesDynamicRolloutStatus = get_services("pods_only").collectEntries {
    ["${it}" : generateDynamicRolloutStage(it)]
}

def generateDynamicRolloutStage(service) {
    return {
        stage("${service}") {
                echo "check rollout status for ${service}"
                sh "kubectl rollout status --watch deployment/${service} --namespace $service_name-${params.deploy_env} --timeout=20m"
        }
    }
}

def get_current_replica_count(String namespace, String node) {
  result = sh returnStdout: true, script: "kubectl get deployments --namespace ${namespace} ${namespace}-${node} -o jsonpath='{ .spec.replicas }'"
  return result
}

def new_replica_count(String namespace, String node, desired_replica_count) {
  current_replica_count = get_current_replica_count("${namespace}", "${node}")

  if(current_replica_count.toInteger() > "${desired_replica_count}".toInteger()) { 
     return current_replica_count
  } else{
     return "${desired_replica_count}".toInteger() 
  }
}

def get_docker_image_tag(build_tag, existing_tag) {
    if("${build_tag}" != "") { 
      return "${build_tag}"
    } else if("${existing_tag}" != ""){ 
        return "${existing_tag}" 
    } else {
      return "error"
    }
}

def get_las_successful_build(String job_name) {
  lastSuccessfulBuild = Jenkins.instance.getItem("${job_name}").lastSuccessfulBuild.number
  return lastSuccessfulBuild
}

def get_k8s_job_status(job_name, namespace) {
    result = sh returnStdout: true, script: "kubectl get jobs ${job_name} --namespace ${namespace} -o jsonpath='{.status.succeeded}'"
    return result
}

pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      label generated_label
      defaultContainer 'docker-helm-kubectl'
      yaml dockerInPodwithKubeConfigMount(kubeconfigMap, kubeconfigMountPath, podMemoryRequests, podCPURequests)
    }
  }

  parameters {
      string(name: 'PIPELINE_BRANCH',
        defaultValue: "master",
        description: 'Specify brach to build'
      )

      string(name: 'SERVICE_IMAGE_TAG',
        defaultValue: "",
        description: 'Specify docker image tag or leave empty to build new one.'
      )

      choice(name: 'SKIP_DJANGO_MIGRATIONS',
        choices: ['no', 'yes'],
        description: 'Skip flyway migration job?'
      )
  }

  environment {
    PIPELINE_BRANCH = "${params.PIPELINE_BRANCH}"
    SERVICE_NAME = "$service_name"

    TEMPLATES_DIR = "k8s.service/helm/basic_templates"

    KUBECONFIG = "$kubeconfigMountPath/${params.kubeconfigMap}"
    KUBERNETES_NAMESPACE = "$SERVICE_NAME-${params.deploy_env}"

    JENKINS_SLAVE_ECR_REGION = "us-east-2"

    SERVICE_REGION = "us-east-2"
    SERVICE_ACCOUNT_ID = "989806208174"
    SERVICE_ECR_URI = "$SERVICE_ACCOUNT_ID" + ".dkr.ecr." + "$SERVICE_REGION" + ".amazonaws.com/microservice-" + "$SERVICE_NAME" + "-${params.deploy_env}"

    CONFIGURE_K8S_RBAC = "${params.ConfigureDevRBAC}"
  }

  stages{
     stage('checkout repos and set job attributes') {
       parallel {
          stage('set build name and description') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
            }
            steps {
              // container('jnlp') {
                  script {
                    currentBuild.displayName = "$SERVICE_NAME-${params.deploy_env}-"+currentBuild.displayName
                    currentBuild.description = "$SERVICE_NAME build branch: $PIPELINE_BRANCH"
                  }
                  script {
                     env.BUILD_SERVICE_IMAGE_TAG=""
                  }
              // }
            }
          }
          stage('checkout service repo') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" == "" && "${params.PIPELINE_BRANCH}" != "" }
            }
            steps {
              ansiColor('xterm') {
                  dir("$SERVICE_NAME") {
                    checkout([
                      $class: 'GitSCM',
                      branches: [[name: "$PIPELINE_BRANCH"]],
                      doGenerateSubmoduleConfigurations: false,
                      extensions: [
                         [$class: 'CloneOption',
                              depth: 1,
                              shallow: true
                         ]
                      ],
                      submoduleCfg: [],
                      userRemoteConfigs: [[credentialsId: 'jenkins-pipeline-ssh-key', url: 'ssh://git@git.listumbrella.com:8979/subdomain/adviser.git']]
                    ])
                
                    script {
                       env.SERVICE_REPO_PATH=sh(returnStdout: true, script: "pwd").trim()
                       env.SERVICE_GIT_COMMIT_HASH=sh(returnStdout: true, script: "git rev-parse HEAD").trim()
                       env.BUILD_SERVICE_IMAGE_TAG=""
                    }
                }
              }
            }
          }
          stage('checkout helm repo') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
            }
            steps {
              ansiColor('xterm') {
                  dir("helm") {
                    checkout([
                      $class: 'GitSCM',
                      branches: [[name: "master"]],
                      doGenerateSubmoduleConfigurations: false,
                      extensions: [
                         [$class: 'CloneOption',
                              depth: 1,
                              shallow: true
                         ]
                      ],
                      submoduleCfg: [],
                      userRemoteConfigs: [[credentialsId: 'jenkins-pipeline-ssh-key', url: 'ssh://git@git.listumbrella.com:8979/ops/exrates-ops-tools.git']]
                    ])
                  
                    script {
                       env.HELM_REPO_PATH=sh(returnStdout: true, script: "pwd").trim()
                    }
                  }
              }
            }
          }
      }
    }
    stage('build service') {
      when {
        expression { "${params.SERVICE_IMAGE_TAG}" == "" && "${params.PIPELINE_BRANCH}" != "" }
      }
      steps {
        ansiColor('xterm') {
            echo "build $SERVICE_NAME running..."
            dir("$SERVICE_NAME") {
              sh "docker build . -f ./$SERVICE_NAME-Dockerfile-build --tag $SERVICE_ECR_URI:${SERVICE_GIT_COMMIT_HASH}-${BUILD_NUMBER} --build-arg APP_PORT=8080"
              sh "docker tag $SERVICE_ECR_URI:${SERVICE_GIT_COMMIT_HASH}-${BUILD_NUMBER} $SERVICE_ECR_URI:latest"
            }
        }
      }
    }
    stage('push image') {
      when {
        expression { "${params.SERVICE_IMAGE_TAG}" == "" && "${params.PIPELINE_BRANCH}" != ""}
      }
      steps {
        ansiColor('xterm') {
            echo "login to ECR"
            sh "aws ecr get-login --region $SERVICE_REGION | sed -e 's/-e none//g' | bash"
            echo "pushing service image..."
            sh "docker push $SERVICE_ECR_URI:${SERVICE_GIT_COMMIT_HASH}-${BUILD_NUMBER}"
            sh "docker push $SERVICE_ECR_URI:latest"
            sh "docker rmi -f $SERVICE_ECR_URI:${SERVICE_GIT_COMMIT_HASH}-${BUILD_NUMBER}"
            sh "docker rmi -f $SERVICE_ECR_URI:latest"
        }
        script {
           env.BUILD_SERVICE_IMAGE_TAG="${SERVICE_GIT_COMMIT_HASH}-${BUILD_NUMBER}"
        }
      }
    }
    stage('kubectl config and test connection') {
      when {
        expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
      }
      steps {
        ansiColor('xterm') {
            echo "running kubectl connection test"
            echo "cat $KUBECONFIG > ~/.kube/config"
            sh "kubectl get pods --namespace $KUBERNETES_NAMESPACE"
        }
      }
    }


    stage('generate helm charts') {
      parallel {
        stage('generate django migration helm chart') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
            }
            steps {
                script {
                  env.SERVICE_DOCKER_IMAGE_TAG=get_docker_image_tag("${BUILD_SERVICE_IMAGE_TAG}", "${params.SERVICE_IMAGE_TAG}")
                }
                
                ansiColor('xterm') {
                  // dir("$SERVICE_NAME") {
                    echo "Running ansible dry run"
                    sh "cd ${SERVICE_REPO_PATH} && ansible-playbook -c local -i ',localhost' -e 'service_playbook_dir=${HELM_REPO_PATH}/$TEMPLATES_DIR' -e 'deployment_env=${params.deploy_env}' -e 'deploy_image_tag=${SERVICE_DOCKER_IMAGE_TAG}' -e 'deployment_app_version=${BUILD_NUMBER}' -e 'deployment_django_migrate_job_name=django-dbupdater-job-${BUILD_NUMBER}' ansible-template-${params.deploy_env}-env-migrate.yml --check"
                    echo "Running ansible to generate helm charts"
                    sh "cd ${SERVICE_REPO_PATH} && ansible-playbook -c local -i ',localhost' -e 'service_playbook_dir=${HELM_REPO_PATH}/$TEMPLATES_DIR' -e 'deployment_env=${params.deploy_env}' -e 'deploy_image_tag=${SERVICE_DOCKER_IMAGE_TAG}' -e 'deployment_app_version=${BUILD_NUMBER}' -e 'deployment_django_migrate_job_name=django-dbupdater-job-${BUILD_NUMBER}' ansible-template-${params.deploy_env}-env-migrate.yml"
                  // }
                }
            }
        }
        stage('generate service helm chart') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
            }
            steps {
                script {
                  env.SERVICE_DOCKER_IMAGE_TAG=get_docker_image_tag("${BUILD_SERVICE_IMAGE_TAG}", "${params.SERVICE_IMAGE_TAG}")
                }
                
                ansiColor('xterm') {
                  // dir("$SERVICE_NAME") {
                    echo "Running ansible dry run"
                    sh "cd ${SERVICE_REPO_PATH} && ansible-playbook -c local -i ',localhost' -e 'service_playbook_dir=${HELM_REPO_PATH}/$TEMPLATES_DIR' -e 'deployment_env=${params.deploy_env}' -e 'deploy_image_tag=${SERVICE_DOCKER_IMAGE_TAG}' -e 'deployment_app_version=${BUILD_NUMBER}' ansible-template-${params.deploy_env}-env.yml --check"
                    echo "Running ansible to generate helm charts"
                    sh "cd ${SERVICE_REPO_PATH} && ansible-playbook -c local -i ',localhost' -e 'service_playbook_dir=${HELM_REPO_PATH}/$TEMPLATES_DIR' -e 'deployment_env=${params.deploy_env}' -e 'deploy_image_tag=${SERVICE_DOCKER_IMAGE_TAG}' -e 'deployment_app_version=${BUILD_NUMBER}' ansible-template-${params.deploy_env}-env.yml"
                  // }
                }
            }
        }
      }
    }

    stage('helm init') {
        when {
          expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
        }
        steps {
            ansiColor('xterm') {
              // dir("helm") {
                echo "Running helm init"
                sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR && helm init --upgrade --client-only"
                echo "Updating $SERVICE_NAME helm dependencies"
                sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR && helm init --client-only && ./install.sh"

                echo "Updating django-migrate helm dependencies"
                sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR/django-migrate-chart && helm init --client-only && ./django_migrate_install.sh"
              // }
            }
        }
    }

    stage('helm dry-run') {
      parallel {
        stage('helm django-migrate dry-run') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
            }
            steps {
                ansiColor('xterm') {
                  // dir("helm") {
                    echo "Running helm dry-run django-migrate deployment"
                    sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR/django-migrate-chart && helm init --client-only && /usr/local/bin/helm upgrade --install --dry-run --debug $SERVICE_NAME-django-migrate --namespace $KUBERNETES_NAMESPACE  . "
                  // }
                }
            }
        }
        stage('helm service dry-run') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != ""}
            }
            steps {
                ansiColor('xterm') {
                  // dir("helm") {
                    echo "Running helm dry-run service deployment"
                    sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR && helm init --client-only && /usr/local/bin/helm upgrade --install --dry-run --debug $SERVICE_NAME --namespace $KUBERNETES_NAMESPACE  . "
                  // }
                }
            }
        }
      }
    }

    stage('helm deploy django-migrate') {
        when {
          expression { "${params.SKIP_DJANGO_MIGRATIONS}" == "no" }
        }
        steps {
            ansiColor('xterm') {
               echo "Running helm dry-run deployment"
               sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR/django-migrate-chart && helm init --client-only && /usr/local/bin/helm upgrade --install $SERVICE_NAME-django-migrate --namespace $KUBERNETES_NAMESPACE . "
            }
        }
    }
    stage('check django-dbupdater-job status') {
        when {
          expression { "${params.SKIP_DJANGO_MIGRATIONS}" == "no" }
        }
        steps {
            ansiColor('xterm') {
               echo "Checking django-dbupdater-job status..."
               sh "kubectl wait --for=condition=complete job/django-dbupdater-job-${BUILD_NUMBER} --namespace $KUBERNETES_NAMESPACE -o yaml --timeout=30m" //timeout - The length of time to wait before giving up. Zero means check once and don't wait, negative means wait for a week.
            }
            script {
               env.DJANGO_MIGRATIONS_JOB_STATUS=get_k8s_job_status("django-dbupdater-job-${BUILD_NUMBER}", "$KUBERNETES_NAMESPACE")
            }
            echo "DJANGO_MIGRATIONS_JOB_STATUS: ${DJANGO_MIGRATIONS_JOB_STATUS}"
        }
    }
    
    stage('helm deploy service') {
      parallel {
        stage('delete succeeded django-dbupdater-job') {
            when {
                expression { env.DJANGO_MIGRATIONS_JOB_STATUS == "1" && "${params.SKIP_DJANGO_MIGRATIONS}" == "no"  }
            }
            steps {
                ansiColor('xterm') {
                   echo "Deleting succeeded django-dbupdater-job..."
                   sh "kubectl delete job --namespace $KUBERNETES_NAMESPACE django-dbupdater-job-${BUILD_NUMBER}"
                }
            }
        }
        stage('deploy service') {
            when {
              expression { ("${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != "") && (env.DJANGO_MIGRATIONS_JOB_STATUS == "1" || "${params.SKIP_DJANGO_MIGRATIONS}" == "yes")}
            }
            steps {
                ansiColor('xterm') {
                  // dir("helm") {
                    echo "Running helm deployment"
                    sh "cd ${HELM_REPO_PATH}/$TEMPLATES_DIR && helm init --client-only && /usr/local/bin/helm upgrade --install $SERVICE_NAME --namespace $KUBERNETES_NAMESPACE . "
                  // }
                }
                script {
                  currentBuild.description = currentBuild.description + ", image tag: ${SERVICE_DOCKER_IMAGE_TAG}"
                }
            }
        }
      }
    }

    stage('configure RBAC') {
        when {
          expression { env.CONFIGURE_K8S_RBAC == "yes" && ("${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != "") }
        }
        steps {
            ansiColor('xterm') {
              // dir("helm") {
                echo "Add developer user to k8s using service account and create RBAC"
                sh "/${HELM_REPO_PATH}/$TEMPLATES_DIR/kubernetes_add_service_account_kubeconfig.sh sa-developer $KUBERNETES_NAMESPACE developer ${params.deploy_env}"
              // }
            }
        }
    }
    stage('rollout status') {
      parallel {
        stage('rollout status parallel stage') {
            when {
              expression { "${params.SERVICE_IMAGE_TAG}" != "" || "${params.PIPELINE_BRANCH}" != "" || "${params.ROLLOUT_IF_FAILED}" == "yes" }
            }
            steps {
                ansiColor('xterm') {
                  script {
                      parallel parallelStagesDynamicRolloutStatus
                  }
                }
            }
        }
      }
    }
  } //stages

}
