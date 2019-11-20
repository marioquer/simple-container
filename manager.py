import json
import uuid
import os
import signal
import shutil
import sys
import time

access_dict = {
    'READ': 'ro',
    'READWRITE': 'rw'
}

class Manager():
    def __init__(self):
        self.config_files = []
        self.running_containers = []
        self.running_containers_names = []
        self.running_containers_pid_map = {}
        self.running_containers_mnt_point_map = {}


    def add_config(self, argv):
        '''
        configs store in configs/
        '''
        # check valid arguments
        try:
            argv_dict = json.loads(argv.decode('utf8'))
        except ValueError:
            return '', 409
        if 'name' not in argv_dict or 'major' not in argv_dict or 'minor' not in argv_dict:
            return '', 409

        filename = argv_dict.get('name') + '-' + argv_dict.get('major') + '-' \
            + argv_dict.get('minor') + '.cfg'

        # exists
        if os.path.isfile('configs/' + filename):
            return '', 409

        # write config into a config file
        with open('configs/' + filename, 'w') as outfile:
            json.dump(argv_dict, outfile)

        # record the filename
        self.config_files.append(filename)

        return '', 200


    def list_config(self):
        '''
        show all configfiles
        '''
        return {
                    "files": self.config_files
            }, 200


    def launch(self, argv):
        '''
        container rootdirs store in containers/
        '''

        try:
            argv_dict = json.loads(argv.decode('utf8'))
        except ValueError:
            return '', 409

        # if configfiles does not exist - 404 not found
        filename = argv_dict.get('name') + '-' + argv_dict.get('major') + '-' \
            + argv_dict.get('minor') + '.cfg'
        if filename not in self.config_files:
            return '', 404

        # launch a new instance
        argv_dict['instance'] = argv_dict.get('name') + str(uuid.uuid4())
        config = self.read_config(filename)
        status = self.initialize_container(argv_dict['instance'], config)


        # add the newly launched container into running containers list
        self.running_containers.append(argv_dict)
        self.running_containers_names.append(argv_dict['instance'])

        print('launched {}'.format(argv_dict['instance']))

        return argv_dict, 200


    def list_container(self):
        '''
        list all containers
        '''
        return {
                    "instances": self.running_containers
            }, 200


    def destroy_container(self, name):
        '''
        destroy a running container
        '''
        # container name does not exist
        if name not in self.running_containers_names:
            return '', 404

        # destroy a running container
        self.clean_container_by_name(name)

        # update data structure of running containers (names)
        self.running_containers_names.remove(name)
        self.running_containers_pid_map.pop(name, None)
        self.running_containers_mnt_point_map.pop(name, None)
        self.running_containers = [container for container in self.running_containers \
            if not (container['instance'] == name)]

        print('destroyed {}'.format(name))

        return '', 200


    def destroy_all(self):
        '''
        destroy all running containers
        '''
        # destroy containers one by one
        for name in self.running_containers_names:
            self.clean_container_by_name(name)

        self.running_containers_names = []
        self.running_containers = []
        self.running_containers_pid_map = {}
        self.running_containers_mnt_point_map = {}
        return '', 200


    def clean_container_by_name(self, name):
        pid = self.running_containers_pid_map[name]
        # os.killpg(pid, signal.SIGINT)
        # kill all process in this process group
        os.system('sudo kill -9 -{}'.format(pid))
        sorted_list = self.running_containers_mnt_point_map[name]
        sorted_list.sort(key = lambda x: len(x.split('/')), reverse=True)

        for mnt_point in sorted_list:
            cmd = 'sudo umount containers/{}/*{}'.format(name, mnt_point)
            os.system(cmd)
        shutil.rmtree('containers/{}'.format(name))


    def read_config(self, filename):
        file = open('configs/' + filename, 'r')
        return json.loads(file.read())


    def initialize_container(self, container_name, config):
        # create dir
        os.makedirs('containers/{}'.format(container_name))
        os.system('tar -xzf base_images/{} --directory containers/{}'.format(config['base_image'], container_name))

        root_dir = config['base_image'].split('.')[0]
        mnt_point_list = ['/proc']

        # mount bind
        for mnt in config['mounts']:
            tar_name, mnt_point, access = mnt.split(' ')
            mnt_point_list.append(mnt_point)
            os.system('tar -xzf mountables/{} --directory containers/{}'.format(tar_name, container_name))
            mnt_point_dir = 'containers/{}/{}{}'.format(container_name, root_dir, mnt_point)
            os.makedirs(mnt_point_dir)
            os.system('sudo mount --bind -o {} $PWD/containers/{}/{} $PWD/{}'.format(access_dict[access], container_name, tar_name.split('.')[0], mnt_point_dir))

        # start process
        pid = os.fork()
        if pid == 0:
            # child process
            os.setpgrp()
            proc_dir = '$PWD/containers/{}/{}/proc'.format(container_name, root_dir)
            os.system("sudo mount -t proc proc {}".format(proc_dir))
            initialize_cmd = 'export {} && {}'.format(config['startup_env'], config['startup_script'])
            launch_cmd = 'sudo unshare -p -f --mount-proc={} chroot --userspec={} containers/{}/{} /bin/bash -c "{}"'.format(proc_dir, config['startup_owner'], container_name, root_dir, initialize_cmd)
            os.system(launch_cmd)
            # sys.exit(0)
        else:
            # parent process, add process pid to map
            self.running_containers_pid_map[container_name] = pid
            self.running_containers_mnt_point_map[container_name] = mnt_point_list
            time.sleep(5)



if __name__ == "__main__":
    manager = Manager()
    argv = {
        "name": "sensiblename",
        "major": "1",
        "minor": "01",
        "base_image": "basefs.tar.gz",
        "mounts": [
            "potato.tar /webserver/potato READ",
        ],
        "startup_script": "/webserver/tiny.sh",
        "startup_owner": "root",
        "startup_env": "PORT=10000;LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/var/lib"
    }
    launch_argv = {
        "name": "sensiblename",
        "major": "1",
        "minor": "01"
    }
    manager.add_config(bytes(json.dumps(argv), 'utf8'))
    response, status = manager.launch(bytes(json.dumps(launch_argv), 'utf8'))
    # manager.destroy_container(response['instance'])