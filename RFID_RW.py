import RPi.GPIO as GPIO
import MFRC522
import signal
import re

class RFID_RW():
    
    def __init__(self):
        pass
    
    # converts text to list of int ascii codes 
    def convert_to_ascii(self, text):
        data = []
        for char in text:
            data.append(ord(char))  
        return data

    # Capture SIGINT for cleanup when the script is aborted 
    def end_read(self, signal, frame):
        global continue_reading
        print("Ctrl+C captured, ending read. ")
        continue_reading = False
        GPIO.cleanup()
    
    # Read from the RFID card ONE time 
    def read_RFID(self):
        
        # hook the SIGINT
        signal.signal(signal.SIGINT, self.end_read)

        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()

        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print ("Card detected")
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
        
            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 1, key, uid)
            print ("\n")

            # Check if authenticated
            if status == MIFAREReader.MI_OK:

                
                data1 = MIFAREReader.MFRC522_Read(1)
                
                
                MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 2, key, uid)
                data2 = MIFAREReader.MFRC522_Read(2)
                
                MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 20, key, uid)
                data3 = MIFAREReader.MFRC522_Read(20)
                
                MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 21, key, uid)
                data4 = MIFAREReader.MFRC522_Read(21)
                
                
                MIFAREReader.MFRC522_StopCrypto1()
                
                data = data1 + data2 + data3 + data4
                
                data = list(filter((0).__ne__, data))
                data = "".join(chr(i) for i in data)

                return data
            
            else:
                print("Authentication Error")
            
    # Write tag to the RFID Card
    def write_RFID(self, tag):
        
        # convert tag to 16 int byte lists
        data_sec1  = self.convert_to_ascii(tag[ 0:16])
        data_sec2  = self.convert_to_ascii(tag[16:32])
        data_sec20 = self.convert_to_ascii(tag[32:48])
        data_sec21 = self.convert_to_ascii(tag[48:64])
        
        continue_reading = True
        
        # hook the SIGINT
        signal.signal(signal.SIGINT, self.end_read)
        
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()
        
        while continue_reading:

            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                print ("Card detected")
        
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
        
                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 1, key, uid)
                print ("\n")

                # Check if authenticated
                if status == MIFAREReader.MI_OK:

                    MIFAREReader.MFRC522_Write(1, data_sec1)

                    MIFAREReader.MFRC522_Read(1)
                    print("\n")

                    MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 2, key, uid)
                    MIFAREReader.MFRC522_Write(2, data_sec2)
                    MIFAREReader.MFRC522_Read(2)
                    print("\n")
                    
                    MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 20, key, uid)
                    MIFAREReader.MFRC522_Write(20, data_sec20)
                    MIFAREReader.MFRC522_Read(20)
                    print("\n")
                    
                    MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 21, key, uid)
                    MIFAREReader.MFRC522_Write(21, data_sec21)
                    MIFAREReader.MFRC522_Read(21)
                    print("\n")

                    MIFAREReader.MFRC522_StopCrypto1()

                    continue_reading = False
                else:
                    print("Authentication Error")

#test = RFID_RW()
#test.read_RFID()
#print(test.read_RFID())
#test.write_RFID("AAAAAAAAAAAAAAAAAAAAAArAAAAAAAAAgAAAAAAAAAAAAAgAAAAAAAAAAAhAAAAAA")

                
