import java.text.SimpleDateFormat

node {
    // Test pull requests
    if (env.BRANCH_NAME != 'master') {
        stage 'Git pull'
        checkout scm

        def demoBotRepo = git branch: env.CHANGE_BRANCH, url: 'https://github.com/giosg/demo-bot.git'
        env.DOCKER_IMAGE = "giosg/demo-bot:${demoBotRepo.GIT_BRANCH}"

        stage 'Build image'
        def customImage = docker.build(env.DOCKER_IMAGE)
        println "Built ${env.DOCKER_IMAGE}"

        stage 'Test'
        customImage.inside {
            withEnv(['SECRET_STRING=bEsTsEcReT']) {
                sh "python -m unittest discover"
            }
        }
    // Otherwise build image when a pull request is merged to master
    } else {
        stage 'Git pull master'
        checkout scm
        def dateFormat = new SimpleDateFormat("yyyy-MM-dd")
        def date = new Date()
        env.DOCKER_IMAGE = "giosg/demo-bot:${dateFormat.format(date)}-${env.BUILD_ID}"

        stage 'Build image'
        def customImage = docker.build(env.DOCKER_IMAGE)

        stage 'Upload image to docker hub'
        customImage.push()
        customImage.push('latest')
    }
}
