sudo umount containers/terri*/*/proc
sudo umount containers/terri*/*/webserver/cabbage/potato
sudo umount containers/terri*/*/webserver/cabbage
sudo umount containers/terri*/*/webserver/tomato/cabbage
sudo umount containers/terri*/*/webserver/tomato
sudo umount containers/terri*/*/webserver/potato

sudo umount containers/sensi*/*/proc
sudo umount containers/sensi*/*/webserver/potato

sudo rm -rf containers/terri*
sudo rm -rf containers/sensi*