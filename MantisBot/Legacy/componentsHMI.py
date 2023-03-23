import wpilib

class FlightStickHMI:
    def __init__(self, stickLeft_ID, stickRight_ID):
        self.leftStick = wpilib.Joystick(stickLeft_ID)
        self.rightStick = wpilib.Joystick(stickRight_ID)
        
        self.fsR = 0
        self.fsRb2 = False
        
        self.fsL = 0
        self.changed = True

    def is_changedInput(self):
        # Left Stick Commands
        fsL = self.leftStick.getY()

        # Right Stick Commands
        fsR = self.rightStick.getY()
        fsRb2 = self.rightStick.getRawButtonPressed(2)

        if fsL != self.fsL or fsR != self.fsR or fsRb2 != self.fsRb2:
            self.fsL = fsL
            self.fsR = fsR
            self.fsRb2 = fsRb2
            self.changed = True
            return True

        else:
            self.changed = False
            return False

    def getButton(self):
        return self.fsRb2

    def getInput(self):
        return (self.fsL, self.fsR)

class HMIModule:
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.fsR = 0
        self.fsRb2 = False
        self.fsL = 0
        self.changed = False

    def getInput(self): # fsTuple = (fsL, fsR)
        self.changed = False
        return (self.fsL, self.fsR)

    def is_changed(self):
        return self.changed

    def is_buttonPressed(self):
        return self.fsRb2

    def execute(self):
        if self.hmi_interface.is_changedInput():
            (self.fsL, self.fsR) = self.hmi_interface.getInput()
            self.fsRb2 = self.hmi_interface.getButton()
            self.changed = True


