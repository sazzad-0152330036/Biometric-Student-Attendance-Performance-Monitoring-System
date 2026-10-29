import time
# import ntplib
from datetime import datetime
# from pyfingerprint.pyfingerprint import PyFingerprint

# Fingerprint name mapping (index corresponds to Finger ID)
finger_names = {1: "Sazzad", 3: "Ayon"}  # Add names for other Finger IDs as needed

# Dictionary to track entry times (key: Finger ID, value: entry time)
entry_times = {}

# Function to get the current time from an NTP server
def get_current_time():
    # try:
        # ntp_client = ntplib.NTPClient()
        # response = ntp_client.request('pool.ntp.org', version=3)
        # current_time = time.localtime(response.tx_time)
        # return current_time
    # except Exception as e:
        print("Failed to get time from NTP server:", e)
        return time.localtime()  # Fallback to system time

# Function to format time as a 12-hour string with AM/PM
def format_time(t):
    return time.strftime("%I:%M:%S %p", t)

# Function to format the date
def format_date(t):
    return time.strftime("%Y-%m-%d", t)

# Function to handle fingerprint events
def handle_fingerprint(finger_id, action, entry_time=None):
    current_time = get_current_time()
    current_time_str = format_time(current_time)
    current_date_str = format_date(current_time)
    
    data_to_send = f"Finger ID: {finger_id}, Name: {finger_names.get(finger_id, 'Unknown')}, Date: {current_date_str}, Time: {current_time_str}, Action: {action}"
    
    if action == "exit" and entry_time:
        entry_time_str = format_time(entry_time)
        data_to_send += f", Entry Time: {entry_time_str}"
    
    print(data_to_send)  # Replace with sending data to a server or saving to a database

# Initialize the fingerprint sensor
# try:
    # fingerprint_sensor = PyFingerprint('/dev/ttyUSB0', 57600)
    
    # if not fingerprint_sensor.verifyPassword():
        raise ValueError("The fingerprint sensor password is incorrect.")

    print("Fingerprint sensor initialized successfully.")
    print(f"Templates stored: {fingerprint_sensor.getTemplateCount()}")
# except Exception as e:
    print("Failed to initialize fingerprint sensor:", e)
    exit(1)

# Main loop to process fingerprints
try:
    while True:
        print("Waiting for a fingerprint...")
        
        # Wait for a finger to be placed on the sensor
        # while not fingerprint_sensor.readImage():
        #     pass

        # fingerprint_sensor.convertImage(0x01)
        # result = fingerprint_sensor.searchTemplate()

        # if result[0] == -1:
        #     print("No match found.")
        # else:
        #     finger_id = result[0]
        #     print(f"Match found! Finger ID: {finger_id}")

            # Handle fingerprint event (entry or exit)
            # if finger_id not in entry_times:
            #     # New fingerprint, mark as entry
            #     entry_times[finger_id] = get_current_time()
            #     handle_fingerprint(finger_id, "entry")
            # else:
            #     # Existing fingerprint, mark as exit
            #     handle_fingerprint(finger_id, "exit", entry_times[finger_id])
            #     del entry_times[finger_id]  # Remove from the dictionary after exit

        time.sleep(1)  # Wait 1 second before the next scan
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print("An error occurred:", e)