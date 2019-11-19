from flask import Flask, escape, request
import os
import sys
import manager

app = Flask(__name__)
manager = None

'''
Post a new config
'''
@app.route('/config', methods=['POST'])
def image_config():
    return manager.add_config(request.data)


'''
List config information
'''
@app.route('/cfginfo', methods=['GET'])
def list_config():
    return manager.list_config()


'''
Launch a new container
'''
@app.route('/launch', methods=['POST'])
def launch():
    return manager.launch(request.data)


'''
List container instance
'''
@app.route('/list', methods=['GET'])
def list_container():
    return manager.list_container()


'''
Destroy container instance
'''
@app.route('/destroy/<string:pk>', methods=['DELETE'])
def destroy_container(pk):
    return manager.destroy_container(pk)


'''
Destroy all container instances
'''
@app.route('/destroyall', methods=['DELETE'])
def destroy_all():
    return manager.destroy_all()


if __name__ == "__main__":
    manager = manager.Manager(sys.argv)
    app.run(host=sys.argv[1], port=sys.argv[2], threaded=False)