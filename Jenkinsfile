properties([
  buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '3', daysToKeepStr: '', numToKeepStr: '20')),
  disableConcurrentBuilds(),
  parameters([
    string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag used when publishing'),
    string(name: 'IMAGE_NAME', defaultValue: '', description: 'Docker image name used when publishing'),
    string(name: 'DOCKER_REGISTRY', defaultValue: '', description: 'The place where docker images are published.'),
    text(name: 'ADHOC_PROJECT_YAML', defaultValue: '', description: 'Override the project vars used to generate documentation')
  ])
])

podTemplate(
  containers: [
    containerTemplate(
      name: 'docker',
      image: 'docker:latest',
      ttyEnabled: true,
      command: 'cat',
      privileged: true
    ),
    containerTemplate(
        name: 'docs-site-builder',
        image: "${DOCKER_REGISTRY}/docs-site-builder:latest",
        command: 'cat',
        ttyEnabled: true,
        envVars: [
          envVar(key: 'HOME', value: '/root')
        ]
    )
  ],
  volumes: [
    hostPathVolume(
      hostPath: '/var/run/docker.sock',
      mountPath: '/var/run/docker.sock'
    )
  ]
) {
  node(POD_LABEL) {

    stage('Clone Repos') {
        container('docs-site-builder') {
          if (ADHOC_PROJECT_YAML == '') {
            checkout(scm)
            sh 'cp ./project_vars.yml /docs-site-builder/project_vars.yml'
            
          } else {
            sh 'echo "${ADHOC_PROJECT_YAML}" > /docs-site-builder/project_vars.yml'
          }
          sh '''
            cd /docs-site-builder
            python3 tasks/clone_repos.py -c project_vars.yml
          '''
        }
    }

    stage('Build site') {
      container('docs-site-builder') {
      sh '''
        cd /mkdocs-site
        python3 tasks/generate.py -c local_vars.yml
        cp -r site/ /home/jenkins/agent/site/
        cp docker/docs-service/Dockerfile /home/jenkins/agent/Dockerfile
      '''
      }
    }

    stage('Build Service') {
      container('docker') {
        withDockerRegistry(credentialsId: 'nexus-credentials', url: "https://${DOCKER_REGISTRY}") {
          sh '''
            cd /home/jenkins/agent
            docker build . -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
            docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
          '''
        }
      }
    }
  }
}
