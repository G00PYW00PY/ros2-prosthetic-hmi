import spidev
import time
import os

#spi comms
spi = spidev.SpiDev()
spi.open(0, 0)  # Opens bus 0, device 0 (CE0 / Pin 24)
spi.max_speed_hz = 1350000

#read data from mcp3008
def get_adc_value(channel):
    #start bit, config bit, dummy bit
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    #combine bits
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


print("--- 4-Channel Joystick HIL Test Initialized ---")
print("Reading Hip (X/Y), Knee, and Ankle Pitch. Press Ctrl+C to stop.")

try:
    while True:
        #live view in terminal
        os.system('clear')
        print(f"{'Channel':<15} | {'Raw Val':<10} | {'Voltage':<10} | {'Visual Gauge'}")
        print("-" * 70)

        #iterate 4 POTs wired to CH0, CH1, CH2, and CH3
        joint_names = ["HIP_FLEX", "HIP_LAT", "KNEE_FLEX", "ANKLE_PITCH"]

        for i in range(4):
            raw_val = get_adc_value(i)
            voltage = (raw_val * 3.3) / 1023.0  #3.3V logic

            #create a 20-character visual bar for each joint
            bar_length = int((raw_val / 1023.0) * 20)
            bar = "#" * bar_length

            print(f"{joint_names[i]:<15} | {raw_val:<10} | {voltage:.2f}V      | [{bar:<20}]")

        print("\n--- System Telemetry Active ---")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCalibration Logged. Closing SPI bus.")
    spi.close()
