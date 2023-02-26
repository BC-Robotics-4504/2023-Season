import wpilib

class FlightStickHMI:
    def __init__(self, stickLeft_ID, stickRight_ID):
        self.leftStick = wpilib.Joystick(stickLeft_ID)
        self.rightStick = wpilib.Joystick(stickRight_ID)
        
        self.fsR = 0
        self.fsRButtons = list(range(12))
        
        self.fsL = 0
        self.changed = True

    def is_changedInput(self):
        # Left Stick Commands
        fsL = self.leftStick.getY()

        # Right Stick Commands
        fsR = self.rightStick.getY()

        fsRButtons = list(range(12))
        for i in range (12):
            fsRButtons[i] = self.rightStick.getRawButton(i+1)

        if fsL != self.fsL or fsR != self.fsR or fsRButtons != self.fsRButtons:
            self.fsL = fsL
            self.fsR = fsR
            self.fsRBUttons = fsRButtons
            self.changed = True
            return True

        else:
            self.changed = False
            return False

    def getButton(self, buttonNum):     # TODO: If this code errors out, it's probably because of this change(see lines 9, 21-23, 28 too)
        return self.fsRButtons[buttonNum + 1]

    def getInput(self):
        return (self.fsL, self.fsR)

class HMIModule:
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.fsR = 0
        self.fsRb2 = False
        self.fsL = 0
        self.changed = False
        self.enabled = True

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


