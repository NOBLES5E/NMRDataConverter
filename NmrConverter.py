
__author__ = 'Xiangru Lian'
import re

# fileIn = input('Plz input to path to the file to convert:\n')
fileIn = input('plz input the file to convert')
fileOut = input('plz input the file to output')

mode = int(input('''
Plz input the data mode:
1. Frequency
2. T1
3. T2
'''))


#Read from in
with open(fileIn) as file:
    data = file.read()

rawList = re.findall(r'.+?\n', data)

paraList = []
paraDict = {}
dataList = []

reList = []
imList = []

scans = 0
count = 0
change = 'data'
for line in rawList:
    if re.search(r'[0-9E\.]+?\t', line):
        if change == 'para':
            count += 1
            paraDict['scans'] = scans
            dataList.append([reList, imList])
            paraList.append(paraDict)
            reList = []
            imList = []
            paraDict = {}
            scans = 0
        dataLine = line.split('\t')
        imList.append(float(dataLine[1]))
        reList.append(float(dataLine[2]))
        change = 'data'
        scans += 1

    if re.search(r'[a-z]+', line):
        paraLine = line.split('\t')
        try:
            paraDict[paraLine[0]] = float(paraLine[1])
        except Exception as e:
            print(e)
        change = 'para'
count += 1
paraDict['scans'] = scans
dataList.append([reList, imList])
paraList.append(paraDict)
reList = []
imList = []
paraDict = {}
scans = 0

with open(fileOut, 'w') as file:

    if mode == 1:
        file.write('''%Program File%
C:\Spectro_pulse_programs\T2_tao_2.exp




%End%

%Program Comments%
Echo+anti ringing complet + cyclope
ST : scope Trigger
S1 : power gate
S2 : receiver blancking
AT : Acquisition







%End%

%Pulse Program%
0	0	0	Attente				0	0	0	0	0	0
0	0	0	Scope				0	0	0	0	0	0
0	0	0	Gate				0	1	1	0	0	0
1	0	0	Pi/2	Tl1	Rl1	Rq1	0	1	1	0	0	0
0	0	0	PostB				0	0	1	0	0	0
0	0	0	Tau				0	0	0	0	0	0
0	0	0	VarTau				0	0	0	0	0	0
0	0	0	Gate				0	1	1	1	0	0
1	0	0	Pi	Tl2			0	1	1	0	0	0
0	0	0	PostB				0	0	1	0	0	0
0	0	0	VarTau				0	0	0	0	0	0
0	0	0	Acqu				1	0	0	0	0	0
%End%

%Phase Lists%
Tl1	+X	+X	+X	+X
Tl2	+X	+Y	-X	-Y
Tl3	+X	+X	+X	+X
Rl1	+X	-X	+X	-X
Rl2	+X	+X	+X	+X
%End%

%nb of skipped transfers%
0
%End%

%loops%
1	0
1	0
%End%

%Delays%
Attente	200.000 ms	0
Scope	1.000 us	0
Gate	1.000 us	0
Pi/2	0.500 us	0
PostB	4.000 us	0
Tau	3.000 us	0
VarTau	0.100 us	0
Pi	1.000 us	0
Acqu	10.000 ms	0
%End%


''')
        file.write('%Parameters%' + '\n' +
        'Frequency\t' + '%.6f MHz' % float(paraList[0]['Frequency=']/1000000) + '\t1\n')
        file.write('''Field	10.00000 T	0
DW	''')
        file.write('%6.4f us' % float(paraList[0]['Sampling time=']*1000000))
        file.write('''	0
Sensitivity	0.5 V	0
Scans	''')
        file.write('%d' % int(paraList[0]['scans']))
        file.write('''	0
Transfer	1024	0
Record size	''' + str(paraList[0]['scans']) + '''	0
Power	0.0 dB	0
Aux. frequency	0.000000 MHz	0
Temperature	100.0000 K	0
%End%

%Variables : level1%
''')

        file.write('Frequency\t')
        for var in paraList:
            file.write('%.6f MHz\t' % float(var['Frequency=']/1000000))
        file.write('\n')
        for var in paraList:
            file.write('\tNone')
        file.write('\n%End%\n\n')
        file.write('''
%Variables : level2%
\tNone
\tNone
%End%

%Nb max of Measurements%
9
%End%

%Comments on experiment%
Sample :YBCO O-II
Temperature:  10 K
Frequency : 102.6 - 103.8 MHz 9 points
Power : 19 dB
Receiver : 0 dB
63Cu central line Cu1E Cu1F Cu2
H= 9 T  Tau = 3.0 us Var_Tau = 0.1 us
filter 1.0 us


%End%

''')

    elif mode == 2:
        file.write('''%Program File%
C:\Spectro_pulse_programs\T1_3pulsesComb.exp



%End%

%Program Comments%
Saturation comb for T1 (3 pulses)
Echo+anti ringing complet + cyclope
ST : scope Trigger
S1 : power gate
S2 : receiver blancking
AT : Acquisition















%End%

%Pulse Program%
0	0	0	Attente				0	0	0	0	0	0
0	0	0	Gate				0	1	1	0	0	0
0	0	0	Pi/2comb	+X			0	1	1	0	0	0
0	0	0	CombTime				0	0	0	0	0	0
0	0	0	Gate				0	1	1	0	0	0
0	0	0	Pi/2comb	+X			0	1	1	0	0	0
0	0	0	CombTime				0	0	0	0	0	0
0	0	0	Gate				0	1	1	0	0	0
0	0	0	Pi/2comb	+X			0	1	1	0	0	0
0	0	0	VarT1				0	0	0	0	0	0
0	0	0	Gate				0	1	1	1	0	0
1	0	0	Pi/2	Tl1	Rl1	Rq1	0	1	1	0	0	0
0	0	0	PostB				0	0	1	0	0	0
0	0	0	Tau				0	0	0	0	0	0
0	0	0	VarTau				0	0	0	0	0	0
0	0	0	Gate				0	1	1	0	0	0
1	0	0	Pi	Tl2			0	1	1	0	0	0
0	0	0	PostB				0	0	1	0	0	0
0	0	0	VarTau				0	0	0	0	0	0
0	0	0	Acqu				1	0	0	0	0	0
%End%

%Phase Lists%
Tl1	+X	+X	+X	+X
Tl2	+X	+Y	-X	-Y
Tl3	+X	+X	+X	+X
Rl1	+X	-X	+X	-X
Rl2	+X	+X	+X	+X
%End%

%nb of skipped transfers%
0
%End%

%loops%
1	0
1	0
%End%

%Delays%
Attente	100.000 ms	0
Gate	1.000 us	0
Pi/2comb	0.500 us	0
CombTime	500.000 us	0
VarT1	10.000 us	1
Pi/2	0.500 us	0
PostB	4.000 us	0
Tau	3.000 us	0
VarTau	0.100 us	0
Pi	1.000 us	0
Acqu	10.000 ms	0
%End%

%Parameters%
Frequency	''' + '%10.6f MHz' % float(paraList[0]['Frequency=']/1000000) + '''	0
Field	10.00000 T	0
DW	''' + '%6.4f us' % float(paraList[0]['Sampling time=']*1000000) + '''	0
Sensitivity	0.5 V	0
Scans	1024	0
Transfer	1024	0
Record size	''' + str(paraList[0]['scans']) + '''	0
Power	0.0 dB	0
Aux. frequency	0.000000 MHz	0
Temperature	100.0000 K	0
%End%

%Variables : level1%
''')

        file.write('VarT1\t')
        for var in paraList:
            file.write('%.3f us\t' % (var['Pul.tJ=']*1000000))
        file.write('\n')
        for var in paraList:
            file.write('\tNone')
        file.write('\n%End%\n\n')

        file.write('''
%Variables : level2%
	None
	None
%End%

%Nb max of Measurements%
9
%End%

%Comments on experiment%
Sample :YBCO O-II
Temperature:  10 K
Frequency : 102.6 - 103.8 MHz 9 points
Power : 19 dB
Receiver : 0 dB
63Cu central line Cu1E Cu1F Cu2
H= 9 T  Tau = 3.0 us Var_Tau = 0.1 us
filter 1.0 us


%End%
''')

    elif mode == 3:
        file.write('''%Program File%
C:\Spectro_pulse_programs\echo_arc_cycl.exp

%End%

%Program Comments%
Echo+anti ringing complet + cyclope
ST : scope Trigger
S1 : power gate
S2 : receiver blancking
AT : Acquisition

%End%

%Pulse Program%
0	0	0	Attente				0	0	0	0	0	0
0	0	0	Scope				0	0	0	0	0	0
0	0	0	Gate				0	1	1	1	0	0
0	0	0	Pi/2	Tl1	Rl1	Rq1	0	1	1	0	0	0
0	0	0	PostB				0	0	1	0	0	0
0	0	0	Tau				0	0	0	0	0	0
0	0	0	VarTau				0	0	0	0	0	0
0	0	0	Gate				0	1	1	0	0	0
0	0	0	Pi	Tl2			0	1	1	0	0	0
0	0	0	PostB				0	0	1	0	0	0
0	0	0	VarTau				0	0	0	0	0	0
0	0	0	Acqu				1	0	0	0	0	0
%End%

%Phase Lists%
Tl1	+X	+X	+X	+X
Tl2	+X	+Y	-X	-Y
Tl3	+X	+X	+X	+X
Rl1	+X	-X	+X	-X
Rl2	+X	+X	+X	+X
%End%

%nb of skipped transfers%
0
%End%

%loops%
1	0
1	0
%End%

%Delays%
Attente	500.000 ms	0
Scope	1.000 us	0
Gate	2.000 us	0
Pi/2	0.500 us	0
PostB	3.000 us	0
Tau	1.000 us	0
VarTau	0.100 us	1
Pi	1.000 us	0
Acqu	21.000 ms	0
%End%


%Parameters%
Frequency	''' + '%10.6f MHz' % float(paraList[0]['Frequency=']/1000000) + '''	0
Field	10.00000 T	0
DW	''' + '%6.4f us' % float(paraList[0]['Sampling time=']*1000000) + '''	0
Sensitivity	0.5 V	0
Scans	1024	0
Transfer	1024	0
Record size	''' + str(paraList[0]['scans']) + '''	0
Power	0.0 dB	0
Aux. frequency	0.000000 MHz	0
Temperature	100.0000 K	0
%End%

%Variables : level1%
''')

        file.write('VarTau\t')
        for var in paraList:
            file.write('%.3f us\t' % (var['Pul.t2='] * 1000000))
        file.write('\n')
        for var in paraList:
            file.write('\tNone')
        file.write('\n%End%\n\n')

        file.write('''
%Variables : level2%
	None
	None
%End%

%Nb max of Measurements%
9
%End%

%Comments on experiment%
Sample :YBCO O-II
Temperature:  10 K
Frequency : 102.6 - 103.8 MHz 9 points
Power : 19 dB
Receiver : 0 dB
63Cu central line Cu1E Cu1F Cu2
H= 9 T  Tau = 3.0 us Var_Tau = 0.1 us
filter 1.0 us


%End%
''')



    file.write('%Data%')
    for i in range(0, len(paraList)):
        file.write('''
measure ''' + str(i+1) + '''
scans ''' + str(paraList[i]['scans']) + '\n')
        for data in dataList[i][0]:
            toWrite = '%.3E' % data + '\t'
            toWrite = toWrite.replace('E+0', 'E+')
            toWrite = toWrite.replace('E-0', 'E-')
            file.write(toWrite)
        file.write('\n')
        for data in dataList[i][1]:
            toWrite = '%.3E' % data + '\t'
            toWrite = toWrite.replace('E+0', 'E+')
            toWrite = toWrite.replace('E-0', 'E-')
            file.write(toWrite)
