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
L Connector:LEMO2 J1
U 1 1 61432071
P 8250 3700
F 0 "J1" H 8430 3796 50  0000 L CNN
F 1 "LEMO To TetrAMM" H 8430 3705 50  0000 L CNN
F 2 "" H 8250 3750 50  0001 C CNN
F 3 " ~" H 8250 3750 50  0001 C CNN
	1    8250 3700
	1    0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J0
U 1 1 61432F44
P 3550 3650
F 0 "J0" H 3607 4317 50  0000 C CNN
F 1 "RJ45" H 3607 4226 50  0000 C CNN
F 2 "" V 3550 3675 50  0001 C CNN
F 3 "~" V 3550 3675 50  0001 C CNN
	1    3550 3650
	1    0    0    -1  
$EndComp
Text Label 2950 4350 0    50   ~ 0
1,3,5,7-OrangeBlueGreenBrownSTRIPED,GND
Text Label 2950 4200 0    50   ~ 0
2,4,6,8-OrangeBlueGreenBrown,TRIGG
Wire Wire Line
	3950 3850 4400 3850
Wire Wire Line
	4400 3850 4400 3700
Wire Wire Line
	4400 3650 3950 3650
Wire Wire Line
	4400 3650 4400 3450
Wire Wire Line
	4400 3450 3950 3450
Connection ~ 4400 3650
Wire Wire Line
	4400 3450 4400 3250
Wire Wire Line
	4400 3250 3950 3250
Connection ~ 4400 3450
Wire Wire Line
	4400 3700 7950 3700
Connection ~ 4400 3700
Wire Wire Line
	4400 3700 4400 3650
Wire Wire Line
	3950 3350 4150 3350
Wire Wire Line
	4150 3350 4150 3550
Wire Wire Line
	4150 3550 3950 3550
Wire Wire Line
	4150 3550 4150 3600
Wire Wire Line
	4150 3750 3950 3750
Connection ~ 4150 3550
Wire Wire Line
	4150 3750 4150 3950
Wire Wire Line
	4150 3950 3950 3950
Connection ~ 4150 3750
Wire Wire Line
	4150 3600 7950 3600
Connection ~ 4150 3600
Wire Wire Line
	4150 3600 4150 3750
Text Notes 7800 6750 0    50   ~ 10
SYNCHRONOUS X-RAY DIAGNOSTICS TIRGGER SYSTEM SCHEMATIC
Text Notes 7800 6950 0    50   ~ 10
CODRUTZA DRAGU, UNIVERSITY OF OXFORD, SUMMER STUDENT 2021
Text Notes 7450 7500 0    50   ~ 10
TETRAMM_CONVERTER_SCHEMATIC
Text Notes 8200 7650 0    50   ~ 10
17/09/2021
$EndSCHEMATC
