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
U 1 1 60F48EAD
P 5750 3250
F 0 "A1" H 5750 2161 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" H 5750 2070 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 5750 3250 50  0001 C CIN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 5750 3250 50  0001 C CNN
	1    5750 3250
	-1   0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J0
U 1 1 60F4CE88
P 2300 3200
F 0 "J0" H 2357 3867 50  0000 C CNN
F 1 "RJ45" H 2357 3776 50  0000 C CNN
F 2 "" V 2300 3225 50  0001 C CNN
F 3 "~" V 2300 3225 50  0001 C CNN
	1    2300 3200
	1    0    0    1   
$EndComp
$Comp
L Connector:RJ45 J1
U 1 1 60F4EDF4
P 9750 1950
F 0 "J1" H 9420 1954 50  0000 R CNN
F 1 "RJ45" H 9420 2045 50  0000 R CNN
F 2 "" V 9750 1975 50  0001 C CNN
F 3 "~" V 9750 1975 50  0001 C CNN
	1    9750 1950
	-1   0    0    1   
$EndComp
$Comp
L Connector:RJ45 J2
U 1 1 60F50060
P 9750 3400
F 0 "J2" H 9420 3404 50  0000 R CNN
F 1 "RJ45" H 9420 3495 50  0000 R CNN
F 2 "" V 9750 3425 50  0001 C CNN
F 3 "~" V 9750 3425 50  0001 C CNN
	1    9750 3400
	-1   0    0    1   
$EndComp
$Comp
L Connector:RJ45 J3
U 1 1 60F508FD
P 9750 4800
F 0 "J3" H 9420 4804 50  0000 R CNN
F 1 "RJ45" H 9420 4895 50  0000 R CNN
F 2 "" V 9750 4825 50  0001 C CNN
F 3 "~" V 9750 4825 50  0001 C CNN
	1    9750 4800
	-1   0    0    1   
$EndComp
Wire Wire Line
	9350 1750 8950 1750
Wire Wire Line
	8950 1750 8950 1950
Wire Wire Line
	8950 1950 9350 1950
Wire Wire Line
	8950 2150 9350 2150
Connection ~ 8950 1950
Wire Wire Line
	8950 2150 8950 2350
Wire Wire Line
	8950 2350 9350 2350
Connection ~ 8950 2150
Wire Wire Line
	8950 1950 8950 2050
Wire Wire Line
	8950 2050 8000 2050
Connection ~ 8950 2050
Wire Wire Line
	8950 2050 8950 2150
Wire Wire Line
	9350 3200 8950 3200
Wire Wire Line
	8950 3200 8950 3400
Wire Wire Line
	8950 3800 9350 3800
Connection ~ 8950 3400
Wire Wire Line
	8950 3400 8950 3500
Wire Wire Line
	8950 3400 9350 3400
Wire Wire Line
	9350 3600 8950 3600
Connection ~ 8950 3600
Wire Wire Line
	8950 3600 8950 3800
Wire Wire Line
	9350 4600 8950 4600
Wire Wire Line
	8950 4600 8950 4800
Wire Wire Line
	8950 5200 9350 5200
Wire Wire Line
	9350 4800 8950 4800
Connection ~ 8950 4800
Wire Wire Line
	9350 5000 8950 5000
Wire Wire Line
	8950 4800 8950 4900
Connection ~ 8950 5000
Wire Wire Line
	8950 5000 8950 5200
Wire Wire Line
	8000 3500 8950 3500
Connection ~ 8950 3500
Wire Wire Line
	8950 3500 8950 3600
Wire Wire Line
	8000 4900 8950 4900
Connection ~ 8950 4900
Wire Wire Line
	8950 4900 8950 5000
Wire Wire Line
	9350 1650 9200 1650
Wire Wire Line
	9200 1650 9200 1850
Wire Wire Line
	5750 5750 5750 4250
Wire Wire Line
	9350 1850 9200 1850
Connection ~ 9200 1850
Wire Wire Line
	9200 1850 9200 2050
Wire Wire Line
	9350 2050 9200 2050
Connection ~ 9200 2050
Wire Wire Line
	9350 3100 9200 3100
Wire Wire Line
	9200 2050 9200 2250
Connection ~ 9200 3100
Wire Wire Line
	9200 3100 9200 3300
Wire Wire Line
	9350 3500 9200 3500
Connection ~ 9200 3500
Wire Wire Line
	9200 3500 9200 3700
Wire Wire Line
	9350 3300 9200 3300
Connection ~ 9200 3300
Wire Wire Line
	9200 3300 9200 3500
Wire Wire Line
	9350 3700 9200 3700
Connection ~ 9200 3700
Wire Wire Line
	9200 3700 9200 4500
Wire Wire Line
	9350 2250 9200 2250
Connection ~ 9200 2250
Wire Wire Line
	9200 2250 9200 3100
Wire Wire Line
	9200 4500 9350 4500
Connection ~ 9200 4500
Wire Wire Line
	9200 4500 9200 4700
Wire Wire Line
	9350 4700 9200 4700
Connection ~ 9200 4700
Wire Wire Line
	9350 4900 9200 4900
Wire Wire Line
	9200 4700 9200 4900
Connection ~ 9200 4900
Wire Wire Line
	9350 5100 9200 5100
Wire Wire Line
	9200 4900 9200 5100
Connection ~ 9200 5100
Wire Wire Line
	9200 5100 9200 5750
Wire Wire Line
	8000 2050 8000 3050
Wire Wire Line
	6250 3050 6550 3050
Wire Wire Line
	6550 3050 6550 2650
Wire Wire Line
	6550 2650 6900 2650
Wire Wire Line
	7700 2650 7700 3050
Wire Wire Line
	7700 3050 8000 3050
Wire Wire Line
	6250 3150 6550 3150
Wire Wire Line
	6550 3150 6550 3450
Wire Wire Line
	6550 3450 7150 3450
Wire Wire Line
	8000 3450 8000 3500
Wire Wire Line
	6250 3250 6500 3250
Wire Wire Line
	6500 3250 6500 4000
Wire Wire Line
	8000 4000 8000 4900
$Comp
L Device:D_Zener D1
U 1 1 60F67AA0
P 6900 2900
F 0 "D1" V 6854 2980 50  0000 L CNN
F 1 "ZENER 5.1V" V 6945 2980 50  0000 L CNN
F 2 "" H 6900 2900 50  0001 C CNN
F 3 "~" H 6900 2900 50  0001 C CNN
	1    6900 2900
	0    1    1    0   
$EndComp
$Comp
L Device:D_Zener D2
U 1 1 60F68BE9
P 7150 3700
F 0 "D2" V 7104 3780 50  0000 L CNN
F 1 "ZENER 5.1V" V 7195 3780 50  0000 L CNN
F 2 "" H 7150 3700 50  0001 C CNN
F 3 "~" H 7150 3700 50  0001 C CNN
	1    7150 3700
	0    1    1    0   
$EndComp
$Comp
L Device:D_Zener D3
U 1 1 60F6CB05
P 7600 4350
F 0 "D3" V 7554 4430 50  0000 L CNN
F 1 "ZENER 5.1V" V 7645 4430 50  0000 L CNN
F 2 "" H 7600 4350 50  0001 C CNN
F 3 "~" H 7600 4350 50  0001 C CNN
	1    7600 4350
	0    1    1    0   
$EndComp
Wire Wire Line
	6900 2750 6900 2650
Connection ~ 6900 2650
Wire Wire Line
	6900 2650 7700 2650
Wire Wire Line
	6900 3050 6900 5750
Wire Wire Line
	5750 5750 6900 5750
Connection ~ 6900 5750
Wire Wire Line
	7150 3550 7150 3450
Connection ~ 7150 3450
Wire Wire Line
	7150 3450 8000 3450
Wire Wire Line
	7150 3850 7150 5750
Wire Wire Line
	6900 5750 7150 5750
Connection ~ 7150 5750
Wire Wire Line
	7150 5750 7600 5750
Wire Wire Line
	7600 4200 7600 4000
Wire Wire Line
	6500 4000 7600 4000
Connection ~ 7600 4000
Wire Wire Line
	7600 4000 8000 4000
Wire Wire Line
	7600 4500 7600 5750
Connection ~ 7600 5750
Wire Wire Line
	7600 5750 9200 5750
Wire Wire Line
	4300 3250 4300 5100
Wire Wire Line
	6300 5100 4300 5100
Wire Wire Line
	6300 3850 6250 3850
Wire Wire Line
	6300 3850 6300 5100
Wire Wire Line
	4000 2950 4000 5250
Wire Wire Line
	4000 5250 6400 5250
Wire Wire Line
	6400 5250 6400 3750
Wire Wire Line
	6400 3750 6250 3750
Wire Wire Line
	3750 5750 5750 5750
Connection ~ 5750 5750
Text Label 2000 4000 0    50   ~ 0
6,8-BrownGreen,EStop
Text Label 2000 4200 0    50   ~ 0
2,4-OrangeBlue,Output
Text Label 2000 4400 0    50   ~ 0
3,7-BrownGreenSTRIPED,GND
Text Label 2000 4600 0    50   ~ 0
1-OrangeStriped,Rx
Text Label 3350 2900 0    50   ~ 0
EMERGENCY_STOP_SIGNAL
Text Label 4350 3450 0    50   ~ 0
OUTPUT_SIGNAL
Text Label 8350 2000 0    50   ~ 0
Out1
Text Label 8350 3450 0    50   ~ 0
OUt2
Text Label 8450 4850 0    50   ~ 0
Out3
Text Label 2000 4800 0    50   ~ 0
5-BlueStriped,Tx
Wire Wire Line
	2700 3400 2950 3400
Wire Wire Line
	2950 3400 2950 2950
Wire Wire Line
	2700 3600 2950 3600
Wire Wire Line
	2950 3600 2950 3400
Connection ~ 2950 3400
Wire Wire Line
	3050 3200 3050 3250
Wire Wire Line
	2700 3100 2850 3100
Wire Wire Line
	2850 3100 2850 3500
Wire Wire Line
	2850 3850 3750 3850
Wire Wire Line
	3750 3850 3750 5750
Wire Wire Line
	2700 3500 2850 3500
Connection ~ 2850 3500
Wire Wire Line
	2850 3500 2850 3850
Connection ~ 3050 3200
Wire Wire Line
	3050 3000 3050 3200
Wire Wire Line
	2700 3000 3050 3000
Wire Wire Line
	2950 2950 4000 2950
Wire Wire Line
	3050 3250 4300 3250
Wire Wire Line
	2700 2900 2700 1350
Wire Wire Line
	6450 1350 6450 2750
Wire Wire Line
	6450 2750 6250 2750
Wire Wire Line
	2700 3300 2750 3300
Wire Wire Line
	2700 3200 3050 3200
Wire Wire Line
	2750 3300 2750 1400
Wire Wire Line
	6400 1400 6400 2650
Wire Wire Line
	6400 2650 6250 2650
Text Label 4500 1250 0    50   ~ 0
Connect-Tx-to-Rx
Text Label 4500 1650 0    50   ~ 0
Connect-Rx-to-Tx
Wire Wire Line
	2750 1400 6400 1400
Wire Wire Line
	2700 1350 6450 1350
Text Label 9350 2600 0    50   ~ 0
2,4,6,8-OrangeBlueGreenBrown,TRIGG
Text Label 9350 2750 0    50   ~ 0
1,3,5,7-OrangeBlueGreenBrownSTRIPED,GND
Text Label 9350 4050 0    50   ~ 0
2,4,6,8-OrangeBlueGreenBrown,TRIGG
Text Label 9350 4200 0    50   ~ 0
1,3,5,7-OrangeBlueGreenBrownSTRIPED,GND
Text Label 9300 5450 0    50   ~ 0
2,4,6,8-OrangeBlueGreenBrown,TRIGG
Text Label 9300 5600 0    50   ~ 0
1,3,5,7-OrangeBlueGreenBrownSTRIPED,GND
Text Notes 7850 6800 0    50   ~ 10
SYNCHRONOUS X-RAY DIAGNOSTICS TRIGGER SYSTEM SCHEMATIC\n
Text Notes 7800 6950 0    50   ~ 10
CODRUTZA DRAGU, UNIVERSITY OF OXFORD, SUMMER STUDENT 2021\n
Text Notes 7450 7500 0    50   ~ 10
MIDBOX_SCHEMATIC\n
Text Notes 8200 7650 0    50   ~ 10
17/09/2021\n
$EndSCHEMATC
