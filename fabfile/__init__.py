# 3rd party
from fabric.api import env, task, execute, local, hide

# local
import utils
import provision
import serve
import reset_db

from fabtools.vagrant import vagrant

@task
def dev():
    """define development server"""
    env.provider = "virtualbox"
    utils.set_hosts_from_config()
    
    # TODO do we want to start all the hosts?
    # or just the first one?
    if env.hosts:
        execute(vagrant, env.hosts[0])
    else:
        msg = "No hosts defined in the configuration file"
        raise FabricException(msg)

@task
def localhost():
    """configure fabric to run locally"""
    # install openssh-server and enable password-less ssh to localhost. this
    # should make it so all of the other provisioning scripts (particularly
    # fabtools) can work on the local copy
    # http://stackoverflow.com/a/16651742/564709
    with hide('everything'):
        local('sudo apt-get install -qy openssh-server')
        if not os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
            local('ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa -q')
            local('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')
            local('chmod og-wx ~/.ssh/authorized_keys')
    env.hosts = ['localhost']

    # in localhost mode, remote_root is the same as the local project root
    env.remote_root = utils.project_root()
    
