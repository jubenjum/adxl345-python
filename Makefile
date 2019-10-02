all:
	gcc -O -I/usr/include/i2c -li2c get_data_adxl345.c -o adxl345 
