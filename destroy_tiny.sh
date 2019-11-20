sudo umount containers/tiny*/*/proc
sudo umount containers/tiny*/*/webserver/potato
sudo umount containers/tiny*/*/webserver/tomato

sudo rm -rf containers/tiny*

sudo rm -rf configs
mkdir configs

sudo kill -9 $(ps aux | grep unshare | awk '{print $2}')
sudo kill -9 $(ps aux | grep python | awk '{print $2}')
sudo kill -9 $(ps aux | grep tiny | awk '{print $2}')