download:
	mkdir -p base_images
	wget -P base_images/ http://www.andrew.cmu.edu/user/ayushagr/basefs.tar.gz

install:
	# Put any compilation instructions here if required
	# Any third party installations shuld also occur here
	python3 -m venv venv
	source venv/bin/activate
	pip install flask requests

manager:
	# Put instruction to run your manager here
	source venv/bin/activate
	python3 app.py localhost 8080

clean:
	# Remove all config files stored by the manager in it's lifetime
	# and kill the manager process
	sudo rm -rf configs
	mkdir configs
	sudo kill -9 $(ps aux | grep unshare | awk '{print $2}')
	sudo kill -9 $(ps aux | grep python | awk '{print $2}')
	sudo kill -9 $(ps aux | grep tiny | awk '{print $2}')

cli_tests: clean manager
	./grading/cli_tests/test_1_upload.sh
	./grading/cli_tests/test_2_cfginfo.sh
	./grading/cli_tests/test_3_launch.sh
	./grading/cli_tests/test_4_list.sh
	./grading/cli_tests/test_5_destroyall.sh

api_tests: clean manager
	python3 grading/rest/grading.py 

	
	
