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
L MCU_Module:Arduino_Nano_v3.x A1
U 1 1 60F19753
P 3150 2600
F 0 "A1" H 3150 1511 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" H 3150 1420 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 3150 2600 50  0001 C CIN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 3150 2600 50  0001 C CNN
	1    3150 2600
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3650 2300 4500 2300
Wire Wire Line
	4500 2300 4500 1100
$Comp
L Device:R R2
U 1 1 60F20565
P 6100 3800
F 0 "R2" H 6030 3754 50  0000 R CNN
F 1 "330 OHM" H 6030 3845 50  0000 R CNN
F 2 "" V 6030 3800 50  0001 C CNN
F 3 "~" H 6100 3800 50  0001 C CNN
	1    6100 3800
	-1   0    0    1   
$EndComp
$Comp
L Device:LED LED1
U 1 1 60F20B32
P 5400 4450
F 0 "LED1" V 5439 4332 50  0000 R CNN
F 1 "Green LED" V 5348 4332 50  0000 R CNN
F 2 "" H 5400 4450 50  0001 C CNN
F 3 "~" H 5400 4450 50  0001 C CNN
	1    5400 4450
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED LED2
U 1 1 60F21FAD
P 6100 4400
F 0 "LED2" V 6139 4282 50  0000 R CNN
F 1 "Red LED" V 6048 4282 50  0000 R CNN
F 2 "" H 6100 4400 50  0001 C CNN
F 3 "~" H 6100 4400 50  0001 C CNN
	1    6100 4400
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5400 3950 5400 4300
Wire Wire Line
	6100 3950 6100 4250
Wire Wire Line
	5400 2500 5400 3650
Wire Wire Line
	3650 2500 5400 2500
Wire Wire Line
	3150 3600 3150 5000
$Comp
L Switch:SW_Push SW1
U 1 1 60F28D19
P 3650 6300
F 0 "SW1" H 3650 6585 50  0000 C CNN
F 1 "Momentary Push Button" H 3650 6494 50  0000 C CNN
F 2 "" H 3650 6500 50  0001 C CNN
F 3 "~" H 3650 6500 50  0001 C CNN
	1    3650 6300
	1    0    0    -1  
$EndComp
Connection ~ 3150 5000
$Comp
L Device:R R3
U 1 1 60F2AC86
P 3950 5600
F 0 "R3" V 3743 5600 50  0000 C CNN
F 1 "10K OHM" V 3834 5600 50  0000 C CNN
F 2 "" V 3880 5600 50  0001 C CNN
F 3 "~" H 3950 5600 50  0001 C CNN
	1    3950 5600
	0    1    1    0   
$EndComp
Wire Wire Line
	3650 3200 4500 3200
Wire Wire Line
	4500 3200 4500 5600
Wire Wire Line
	4500 5600 4100 5600
Wire Wire Line
	3800 5600 3150 5600
Wire Wire Line
	3150 5600 3150 5000
Wire Wire Line
	4500 6300 4500 5600
Wire Wire Line
	3850 6300 4500 6300
Connection ~ 4500 5600
Wire Wire Line
	2150 6300 2150 1400
Wire Wire Line
	2150 1400 2950 1400
Wire Wire Line
	2950 1400 2950 1600
Wire Wire Line
	2150 6300 3450 6300
$Comp
L Device:R R1
U 1 1 60F1FABE
P 5400 3800
F 0 "R1" H 5330 3754 50  0000 R CNN
F 1 "330 OHM" H 5330 3845 50  0000 R CNN
F 2 "" V 5330 3800 50  0001 C CNN
F 3 "~" H 5400 3800 50  0001 C CNN
	1    5400 3800
	-1   0    0    1   
$EndComp
Wire Wire Line
	3150 5000 5400 5000
Wire Wire Line
	3650 2400 6100 2400
Wire Wire Line
	6100 2400 6100 3650
Wire Wire Line
	5400 4600 5400 5000
Wire Wire Line
	6100 5000 5400 5000
Wire Wire Line
	6100 4550 6100 5000
Connection ~ 5400 5000
Wire Wire Line
	3650 2600 7600 2600
Wire Wire Line
	4500 1100 7150 1100
$Comp
L Device:D_Zener D2
U 1 1 60F34F1C
P 7150 1500
F 0 "D2" V 7104 1580 50  0000 L CNN
F 1 "ZENER 5.1V" V 7195 1580 50  0000 L CNN
F 2 "" H 7150 1500 50  0001 C CNN
F 3 "~" H 7150 1500 50  0001 C CNN
	1    7150 1500
	0    1    1    0   
$EndComp
$Comp
L Device:D_Zener D1
U 1 1 60F35909
P 7600 3100
F 0 "D1" V 7554 3180 50  0000 L CNN
F 1 "ZENER 5.1V" V 7645 3180 50  0000 L CNN
F 2 "" H 7600 3100 50  0001 C CNN
F 3 "~" H 7600 3100 50  0001 C CNN
	1    7600 3100
	0    1    1    0   
$EndComp
Wire Wire Line
	7150 1100 7150 1350
Connection ~ 7150 1100
Wire Wire Line
	7150 1100 8300 1100
Wire Wire Line
	7150 1650 7150 5000
Wire Wire Line
	7150 5000 6100 5000
Connection ~ 6100 5000
Wire Wire Line
	7600 3250 7600 5000
Wire Wire Line
	7600 5000 7150 5000
Connection ~ 7150 5000
Wire Wire Line
	7600 2950 7600 2600
Connection ~ 7600 2600
Connection ~ 7600 5000
Wire Wire Line
	7600 2600 8850 2600
$Comp
L Connector:RJ45 J1
U 1 1 60F384BA
P 9800 1750
F 0 "J1" H 9470 1754 50  0000 R CNN
F 1 "RJ45" H 9470 1845 50  0000 R CNN
F 2 "" V 9800 1775 50  0001 C CNN
F 3 "~" V 9800 1775 50  0001 C CNN
	1    9800 1750
	-1   0    0    1   
$EndComp
Text Label 8000 2500 0    50   ~ 0
OUTPUT_SIGNAL
Text Label 7700 1050 0    50   ~ 0
EMERGENCy_STOP_SIGNAL
Wire Wire Line
	9400 1950 9200 1950
Wire Wire Line
	9200 1950 9200 2150
Connection ~ 9200 2150
Wire Wire Line
	9200 2150 9400 2150
Text Label 9500 2400 0    50   ~ 0
6,8-BrownGreen,EStop
Wire Wire Line
	8850 1550 8850 2600
Wire Wire Line
	8850 1550 9200 1550
Wire Wire Line
	9200 1550 9200 1750
Wire Wire Line
	9200 1750 9400 1750
Connection ~ 9200 1550
Wire Wire Line
	9200 1550 9400 1550
Text Label 9500 2550 0    50   ~ 0
2,4-OrangeBlue,Output
Wire Wire Line
	8300 2150 8300 1100
Wire Wire Line
	8300 2150 9200 2150
Text Label 9500 2700 0    50   ~ 0
3,7-BrownGreenSTRIPED,GND
Wire Wire Line
	9400 1650 9050 1650
Wire Wire Line
	9050 1650 9050 2050
Wire Wire Line
	9400 2050 9050 2050
Connection ~ 9050 2050
Wire Wire Line
	7600 5000 9050 5000
Wire Wire Line
	9050 2050 9050 5000
Text Label 9500 2850 0    50   ~ 0
1-OrangeSTRIPED,Rx
Wire Wire Line
	8550 2000 8550 1450
Wire Wire Line
	8550 1450 9400 1450
Wire Wire Line
	3650 2000 8550 2000
Wire Wire Line
	8650 2100 8650 1850
Wire Wire Line
	8650 1850 9400 1850
Wire Wire Line
	3650 2100 8650 2100
Text Label 9500 3000 0    50   ~ 0
5,-BlueSTRIPED,Tx
Text Notes 7900 6900 0    50   ~ 10
SYNCHRONOUS X-RAY DIAGNOSTICS TRIGGER SYSTEM SCHEMATIC
Text Notes 7500 7500 0    50   ~ 10
USERSIDE_BOX_SCHEMATIC\n
Text Notes 8200 7650 0    50   ~ 10
17/09/2021
Text Notes 7850 7050 0    50   ~ 10
CODRUTZA DRAGU, UNIVERSITY OF OXFORD, SUMMER STUDENT 2021\n
$EndSCHEMATC
