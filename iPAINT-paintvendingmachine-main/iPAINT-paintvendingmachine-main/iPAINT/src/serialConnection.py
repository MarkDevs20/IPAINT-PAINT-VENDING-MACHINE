import serial
import serial.tools.list_ports
import threading
import time

class SerialConnection:
    def __init__(self, baudRate=115200, callback=None):
        self.callback = callback
        self.running = False
        self.serialPort = None
        self.port = None
        port = self.findArduino()
        if port:
            self.port = port
            self.serialPort = serial.Serial(port, baudRate, timeout=0.1)
            self.running = True
            self.thread = threading.Thread(target=self.listenSerial, daemon=True)
            self.thread.start()
        else:
            print("No Arduino detected.")

    def findArduino(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p.description or "CH340" in p.description:
                return p.device  # Example: "COM5"
        return None
    
    def listenSerial(self):
        while self.running:
            if self.serialPort and self.serialPort.in_waiting:
                data = self.serialPort.readline().decode().strip()
                if data and self.callback:
                    self.callback(data)
            time.sleep(0.05)

    def sendCommand(self, command):
        if self.serialPort:
            self.serialPort.write(f"{command}\n".encode())
            
    def stop(self):
        if self.serialPort:
            self.running = False
            self.thread.join()
            self.serialPort.close()
