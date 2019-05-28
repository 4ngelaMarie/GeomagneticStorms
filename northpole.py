import time

import datetime



# Import the ADS1x15 module.

import Adafruit_ADS1x15



adc = Adafruit_ADS1x15.ADS1015()


GAIN = 1


#measurements saved to txt file on USB
magnet = open("northpole.txt", "a")


while True:
    
  # Read all the ADC channel values in a list.
    
  values = [0]*2
    
  for i in range(2):
        
    # Read channels 3 & 4.
        
    values[i] = adc.read_adc(i+2, gain=GAIN)
    
  
    
  
  now = datetime.datetime.now()
    
  print("%d" %now.month +'/'+ "%d" %now.day +'/'+ "%d" %now.year + ' '+"%d" %now.hour + ':'+"%d" %now.minute +':'+"%d" %now.second + ' '+' | {0:>6} | {1:>6} |'.format(*values))
    
    
  magnet.write("%d" %now.month +'/'+ "%d" %now.day +'/'+ "%d" %now.year + ' '+"%d" %now.hour + ':'+"%d" %now.minute +':'+"%d" %now.second + ' '+'| {0:>6} | {1:>6}|'.format(*values))
    
  magnet.write('\n')

    

  time.sleep(1) #1second delay


magnet.close()