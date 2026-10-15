
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def initialize_ads1115():
    """Initializes the I2C bus and the ADS1115 ADC."""
    # Create the I2C bus using board.SCL and board.SDA (Pins 5 and 3 on Raspberry Pi 4)
    i2c = busio.I2C(board.SCL, board.SDA)
    
    # Create the ADS1115 object at the default I2C address 0x48 (ADDR pin connected to GND)
    ads = ADS.ADS1115(i2c, address=0x48)
    
    return ads

def main():
    print("Initializing ADS1115 Side-Channel Data Ingestion...")
    ads = initialize_ads1115()
    
    # Configure an analog input channel on A0
    # PGA (Programmable Gain Amplifier) options:
    #   ads.gain = 2/3 (Range: -6.144V to +6.144V) -> Recommended for 3.3V/5V rails
    #   ads.gain = 1   (Range: -4.096V to +4.096V)
    #   ads.gain = 2   (Range: -2.048V to +2.048V)
    #   ads.gain = 4   (Range: -1.024V to +1.024V) -> Best for tiny shunt voltage drops
    ads.gain = 1 
    
    chan = AnalogIn(ads, ADS.P0)
    
    print(f"Streaming live voltage from Channel A0 (Gain: {ads.gain}). Press Ctrl+C to stop.\n")
    print(f"{'Timestamp':<22} | {'Voltage (V)':<12} | {'Raw Value':<10}")
    print("-" * 52)
    
    try:
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S.{}".format(int(time.time() % 1 * 1000)))
            voltage = chan.voltage
            raw_value = chan.value
            
            print(f"{timestamp} | {voltage:10.5f} V | {raw_value:10d}")
            
            # Control sampling frequency (adjust delay as needed for your streaming window)
            time.sleep(0.01) # ~100 Hz polling rate for prototyping
            
    except KeyboardInterrupt:
        print("\nStreaming stopped by user. Exiting safely.")

if __name__ == "__main__":
    main()
