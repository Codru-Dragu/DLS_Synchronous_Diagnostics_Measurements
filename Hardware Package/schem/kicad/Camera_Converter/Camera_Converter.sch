EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Conn_01x12_Male J0
U 1 1 614345F3
P 3400 2700
F 0 "J0" H 3508 3381 50  0000 C CNN
F 1 "HIROSE_12P_MALE" H 3508 3290 50  0000 C CNN
F 2 "" H 3400 2700 50  0001 C CNN
F 3 "~" H 3400 2700 50  0001 C CNN
	1    3400 2700
	1    0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J0
U 1 1 6143C74F
P 3550 5000
F 0 "J0" H 3607 5667 50  0000 C CNN
F 1 "RJ45" H 3607 5576 50  0000 C CNN
F 2 "" V 3550 5025 50  0001 C CNN
F 3 "~" V 3550 5025 50  0001 C CNN
	1    3550 5000
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x12_Female J1
U 1 1 61432D74
P 9450 3600
F 0 "J1" H 9478 3576 50  0000 L CNN
F 1 "HIROSE_12P_FEMALE" H 9478 3485 50  0000 L CNN
F 2 "" H 9450 3600 50  0001 C CNN
F 3 "~" H 9450 3600 50  0001 C CNN
	1    9450 3600
	1    0    0    -1  
$EndComp
Text Label 2850 5650 0    50   ~ 0
2,4,6,8-OrangeBlueGreenBrown,TRIGG
Text Label 2800 5850 0    50   ~ 0
1,3,5,7-OrangeBlueGreenBrownSTRIPED,GND
Wire Wire Line
	3950 4600 4400 4600
Wire Wire Line
	4400 4600 4400 4800
Wire Wire Line
	4400 5200 3950 5200
Wire Wire Line
	3950 4800 4400 4800
Connection ~ 4400 4800
Wire Wire Line
	4400 4800 4400 4900
Wire Wire Line
	3950 5000 4400 5000
Connection ~ 4400 5000
Wire Wire Line
	4400 5000 4400 5200
Wire Wire Line
	3950 4700 4100 4700
Wire Wire Line
	4100 4700 4100 4900
Wire Wire Line
	4100 5300 3950 5300
Wire Wire Line
	3950 4900 4100 4900
Connection ~ 4100 4900
Wire Wire Line
	4100 4900 4100 5100
Wire Wire Line
	3950 5100 4100 5100
Connection ~ 4100 5100
Wire Wire Line
	4100 5100 4100 5300
Wire Wire Line
	8350 4900 8350 3400
Wire Wire Line
	8350 3400 9250 3400
Wire Wire Line
	4100 5300 8850 5300
Wire Wire Line
	8850 5300 8850 3700
Wire Wire Line
	8850 3700 9250 3700
Connection ~ 4100 5300
Wire Wire Line
	3600 2200 6150 2200
Wire Wire Line
	6150 2200 6150 3100
Wire Wire Line
	6150 3100 9250 3100
Wire Wire Line
	9250 3200 5950 3200
Wire Wire Line
	5950 3200 5950 2300
Wire Wire Line
	5950 2300 3600 2300
Text Label 4550 2100 0    50   ~ 0
1-POWER_GND
Text Label 4550 2450 0    50   ~ 0
2-POWER_VOLTAGE
Wire Wire Line
	4400 4900 8350 4900
Connection ~ 4400 4900
Wire Wire Line
	4400 4900 4400 5000
Text Label 5800 4850 0    50   ~ 0
TRIGG
Text Label 5800 5450 0    50   ~ 0
TRIGG_GND
Text Label 9650 3100 0    50   ~ 0
1-POWER_GND
Text Label 9650 3300 0    50   ~ 0
2-POWER_VOLTAGE
Text Label 9650 3450 0    50   ~ 0
4-TRIGG
Text Label 9650 3900 0    50   ~ 0
7-TRIGG_GND
Text Notes 7900 6800 0    50   ~ 10
SYNCHRONOUS X-RAY DIAGNOSTICS TRIGGER SYSTEM SCHEMATIC\n
Text Notes 7850 7000 0    50   ~ 10
CODRUTZA DRAGU, UNIVERSITY OF OXFORD, SUMMER STUDENT 2021
Text Notes 7450 7500 0    50   ~ 10
CAMERA_CONVERTER_SCHEMATIC\n
Text Notes 8200 7650 0    50   ~ 10
17/09/2021\n
$EndSCHEMATC
