from fabric.api import cd, env, local, prefix, run

env.hosts = ['cloud']


def deploy():
    local('git push')
    with cd('~/code/twiffle'):
        run('git pull')
        with prefix('source ~/.virtualenvs/twiffle/bin/activate'):
            with cd('~/code/twiffle'):
                run('pip install -r requirements.txt')
                run('supervisorctl restart twiffle')
