import json


class Manager():
    def __init__(self, argv):
        self.config_files = []
        self.running_containers = []
        self.running_containers_names = []

    def add_config(self, argv):
        '''
        configs store in configs/
        '''
        try:
            argv_dict = json.loads(argv)
        except ValueError:
            return '', 409
      
        # write config into a config file
        filename = argv_dict.get('name') + '-' + argv_dict.get('major') + '-' \
            + argv_dict.get('minor') + '.cfg'

        with open(filename, 'w') as outfile:
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
            argv_dict = json.loads(argv)
        except ValueError:
            return '', 409

        # if configfiles does not exist - 404 not found
        filename = argv_dict.get('name') + '-' + argv_dict.get('major') + '-' \
            + argv_dict.get('minor') + '.cfg'
        if filename not in self.config_files:
            return '', 404

        # TODO: launch a new instance
        argv_dict['instance'] = 'instance_name'

        # add the newly launched container into running containers list
        self.running_containers.append(argv_dict)
        self.running_containers_names.append(argv_dict['instance'])

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

        # TODO: destroy a running container

        # update data structure of running containers (names)
        self.running_containers_names.remove(name)
        self.running_containers = [container for container in self.running_containers \
            if not (container['instance'] == name)]

        return '', 200

    def destroy_all(self):
        '''
        destroy all running containers
        '''
        # destroy containers one by one
        for container in self.running_containers:
            # TODO: destroy this container
            pass
        
        self.running_containers_names = []
        self.running_containers = []

        return '', 200


