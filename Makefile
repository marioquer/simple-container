download:
	mkdir -p base_images
	wget -P base_images/ http://www.andrew.cmu.edu/user/ayushagr/basefs.tar.gz

install:
	# Put any compilation instructions here if required
	# Any third party installations shuld also occur here
	sudo apt-get update
	sudo apt-get install -y python3-pip
	pip install --upgrade pip
	pip3 install flask requests

manager:
	# Put instruction to run your manager here
	python3 app.py localhost 8080 &
	sleep 2

clean:
	# Remove all config files stored by the manager in it's lifetime
	# and kill the manager process
	./destroy_tiny.sh > /dev/null 2>&1
	./destroy.sh > /dev/null 2>&1
	sudo rm -rf configs
	mkdir configs
	pkill python || true

cli_tests: clean manager
	./grading/cli_tests/test_1_upload.sh
	./grading/cli_tests/test_2_cfginfo.sh
	./grading/cli_tests/test_3_launch.sh
	./grading/cli_tests/test_4_list.sh
	./grading/cli_tests/test_5_destroyall.sh

api_tests: clean manager
	python3 grading/rest/grading.py