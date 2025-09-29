import time
import serial
import sys
from datetime import datetime

def main():
    print(sys.argv)
    serial_name = sys.argv[1]
    date_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    print("date and time:",date_time)	
    output_name = "flow_meter_capture_" +date_time+ ".csv"
    if len(sys.argv) > 2:
        #Might need to parse additional arguments like --noheaders=true
        #Currently only handles output file name override
        output_name = sys.argv[2]
    
    try:
        with open(".\\" + output_name, "w") as f:
            print("Writing to file: " + output_name)

            #Writing headers to the file
            f.write("PSIA,Temp(Celsius),TotalFlow(LPM),GasFlow(LPM),GasMeasured\r")
            
            ser = serial.Serial(
                port=serial_name,
                baudrate=19200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                xonxoff=False,
                timeout=3
            )
            
            ser.isOpen()
            if (ser.is_open):
                print('Port opened: ' + ser.name)
                print('Pulling data')
                try:
                    while (True):
                        data = ser.readline(40)
                        if (data == b''):
                            print("Not getting any data, please ensure that flow meter is ON and connected")
                        else:
                            str_data = data.decode("utf-8")
                            line = ' '.join(str_data.strip().split()).replace(' ', ',')
                            print(line)
                            f.write(line+"\r")
                except KeyboardInterrupt:
                    print("program terminated by user")
                else:
                    print("Unknonwn exception during data read")
                finally:
                    ser.close()
                    if (not ser.is_open):
                        print('Port closed')
                    f.close()
            else:
                print('Could not open port')
    except serial.SerialException as e:
        print("Failed to establish connection on port " + serial_name + ", please verify that port name is correct")

if __name__== "__main__":
    main()
