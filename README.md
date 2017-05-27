# Raspberry-pi-vital-monitor-via-OLED
This code works along with the raspberry pi guy's repoitory on OLED and helps you to monitor vital of your raspberry pi.
Code developed by woking on the raspberry pi guy's code by miniProjects. (Youtube- https://www.youtube.com/channel/UC8GkzgOijbVgAl5iraoD5TA)

Once you install the raspberry pi guy's repo (https://github.com/the-raspberry-pi-guy/OLED), clone this repo and copy OLEDMem_cpu.py in ~/OLED/python-examples directory.  

following this you can run the code independently by using following command-
sudo python /home/pi/OLED/python-examples/OLEDMem_cpu.py --sleep_time 1 &

You can also add it to /etc/rc.local to run this code every time raspberry pi boots up.
