from optparse import OptionParser
import time
import serial

print '-------------'
print 'file2serial v0.1 created by Sharan'
print 'Use "python -m serial.tools.list_ports" to get possible ports'
print '"Python file2serial.py -h" for help, command line args are possible'
print '-------------\n\n'

# This allows the user to input parameters from commandline
parser = OptionParser()
parser.add_option("-c", "--com", dest="com", help="select COM port", metavar="COM")
parser.add_option("-b", "--baud", dest="baud", help="select baud rate", metavar="BAUD")
parser.add_option("-d", "--delay", dest="delay", help="select interline delay(ms)", metavar="DELAY")
parser.add_option("-s", "--start", action="store_true", dest="start", default=False, help="begin immediately")
parser.add_option("-f", "--file", dest="filename", help="select file to push to serial COM", metavar="FILE")

(options, args) = parser.parse_args()

# Ask the user for the missing information
if options.com == None:
    options.com = raw_input('Please enter a COM Port: ')
if options.baud == None:
    options.baud = raw_input('Please enter a Baud rate: ')
if options.delay == None:
    options.delay = raw_input('Please enter an interline delay(ms): ')
if options.filename == None:
    options.filename = raw_input('Please enter a serial input file: ')

# Display the settings
print ''
print 'Com Port: ', options.com
print 'Baud Rate: ', options.baud
print 'Interline Delay: ', options.delay
print 'File: ', options.filename
print 'Start Immediately: ', options.start
print ''

# Prompt user to continue
while not options.start:
    user_input = raw_input('Begin? [Y/n]: ')
    if user_input.lower() in ['y', 'yes', 'ye', '']:
        options.start = True
    elif user_input.lower() in ['n', 'no']:
        raise SystemExit
    else:
        print 'Invalid Option!'

print ''

# Establish a serial connection
ser = serial.Serial(options.com, options.baud)
ser.write("1".encode())

# Wait a bit
time.sleep(2)

# Open the file to send through serial
f = open(options.filename)
line = f.readline().replace('\r', '')

# Initialize Params
last_time = 0

# MORE RESEARCH INTO EOL CHARACTERS NEEDED IF ISSUES ARISE
# Send the strings through serial without blocking serial read
try:
    while line:
        if ser.inWaiting():
            print ser.readline(),

        if time.time()*1000 > last_time + int(options.delay):
            print line,
            ser.write(line)
            ser.flush()
            line = f.readline().replace('\r', '')
            last_time = time.time()*1000

    # Continue reading serial until user CTRL-C
    while True:
        print ser.readline(),
except KeyboardInterrupt:
    ser.close()
    f.close()
    print '\n\nfile2serial has terminated gracefully.'
    raise SystemExit

# Clean up the program
ser.close()
f.close()
print '\n\nfile2serial has terminated gracefully.'
