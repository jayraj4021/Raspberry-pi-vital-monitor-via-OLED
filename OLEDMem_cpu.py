# miniProjects (https://www.youtube.com/channel/UC8GkzgOijbVgAl5iraoD5TA) created this program by working on OLEDtext.py and OLEDip.py code by The Raspberry Pi Guy!

# Imports the necessary libraries... Gaugette 'talks' to the display ;-)
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys
import os
import socket
import fcntl
import struct

if len(sys.argv) != 3:
	print "USAGE:sudo python OLEDMem_cpu.py --sleep_time <time in seconds>"
	exit()
elif (sys.argv[1] != '--sleep_time'):
	print "USAGE:sudo python OLEDMem_cpu.py --sleep_time <time in seconds>"
        exit()

sleep_time = int(sys.argv[2])

# This function allows us to grab any of our IP addresses
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Define which GPIO pins the reset (RST) and DC signals on the OLED display are connected to on the
# Raspberry Pi. The defined pin numbers must use the WiringPi pin numbering scheme.
RESET_PIN = 15 # WiringPi pin 15 is GPIO14.
DC_PIN = 16 # WiringPi pin 16 is GPIO15.

spi_bus = 0
spi_device = 0
gpio = gaugette.gpio.GPIO()
spi = gaugette.spi.SPI(spi_bus, spi_device)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=64, cols=128) # Change rows & cols values depending on your display dimensions.
led.begin()
led.clear_display()
led.display()
#led.invert_display()
time.sleep(0.5)
led.normal_display()
time.sleep(0.5)

# led.draw_text2(x-axis, y-axis, whatyouwanttoprint, size) < Understand?
# So led.drawtext2() prints simple text to the OLED display like so:

#---------------------------infinite loop-------------------------
while (1):
	#getting RAM usage data	
	os.system("rm -rf mem_data")
	os.system("free | grep Mem | awk -F ' ' '{print $3/$2}' > mem_data")
	mem_file = open("mem_data","r")
	for line in mem_file:
		line = line.rstrip()
		ram_usage_str = line
	mem_file.close()
	ram_usage_float = float(ram_usage_str) * 100.00
	ram_usage = str(ram_usage_float) + ' %'
	os.system("rm -rf mem_data")
	
	#getting cpu usage data
	os.system("rm -rf cpu_data")
	os.system("mpstat | grep all | awk -F ' ' '{print $3}' > cpu_data")
	cpu_file = open("cpu_data","r")
	for line in cpu_file:
	        line = line.rstrip()
	        cpu_usage = line + ' %'
	cpu_file.close()
	os.system("rm -rf cpu_data")
	
	#getting cpu temperature
	os.system("rm -rf temp_data")
	os.system("/opt/vc/bin/vcgencmd measure_temp > temp_data")
	temp_file = open("temp_data","r")
	for line in temp_file:
	        line = line.rstrip()
	        temperature = line.split('=')[1]
	temp_file.close()
	os.system("rm -rf temp_data")
	
	#getting ip address using code from OLEDip.py
	# This sets TEXT equal to whatever your IP address is, or isn't
	try:
		ip_addr = get_ip_address('wlan0') # WiFi address of WiFi adapter. NOT ETHERNET
	except IOError:
		try:
	        	ip_addr = get_ip_address('eth0') # WiFi address of Ethernet cable. NOT ADAPTER
		except IOError:
	        	ip_addr = ('NO INTERNET!')
	
	
	#Putting out things on OLED 	
	led.clear_display()
	text0 = '-Raspberry pi vitals-'
	led.draw_text2(0,0,text0,1)
	text00 = '---------------------'
	led.draw_text2(0,8,text00,1)
	text1 = 'RAM USAGE='
	led.draw_text2(0,16,text1,1)
	led.draw_text2(64,16,ram_usage,1)
	text2 = 'CPU='
	led.draw_text2(0,24,text2,1)
	led.draw_text2(28,24,cpu_usage,1)
	text3 = 'Temperature='
	led.draw_text2(0,32,text3,1)
	led.draw_text2(75,32,temperature,1)
	text4 = 'Your IP Address is:'
	led.draw_text2(0,40,text4,1)
	led.draw_text2(0,48,ip_addr,1)
	text5 = '----------------------'
	led.draw_text2(0,56,text5,1)
	led.display()

	time.sleep(sleep_time)
