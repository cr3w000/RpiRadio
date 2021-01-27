sudo apt install -y python3-dev
sudo apt install -y python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-pip
sudo apt install -y python3-setuptools
sudo apt install -y python3-rpi.gpio


git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git

cd Adafruit_Python_SSD1306

sudo python3 setup.py install


