import wpilib

class FlightStickHMI:
    def __init__(self, stickLeft_ID, stickRight_ID):
        self.leftStick = wpilib.Joystick(stickLeft_ID)
        self.rightStick = wpilib.Joystick(stickRight_ID)
        
        self.fsR = 0
        self.fsRButtons = list(range(12))
        
        self.fsL = 0
        self.fsLButtons = list(range(12))

        self.changed = True

    def is_changedInput(self):
        # Left Stick Commands
        fsL = self.leftStick.getY()

        # Right Stick Commands
        fsR = self.rightStick.getY()

        fsRButtons = list(range(12))
        for i in range(len(fsRButtons)):
            fsRButtons[i] = self.rightStick.getRawButton(i+1)

        fsLButtons = list(range(8))
        for i in range(len(fsLButtons)):
            fsLButtons[i] = self.leftStick.getRawButton(i+1)

        if fsL != self.fsL or fsR != self.fsR or fsRButtons != self.fsRButtons or fsLButtons != self.fsLButtons:
            self.fsL = fsL
            self.fsLButtons = fsLButtons
            self.fsR = fsR
            self.fsRButtons = fsRButtons
            self.changed = True
            return True

        else:
            self.changed = False
            return False

    def getRButton(self, buttonNum):
        return self.fsRButtons[buttonNum - 1]

    def getLButton(self, buttonNum):
            return self.fsLButtons[buttonNum - 1]

    def getInput(self):
        return (self.fsL, self.fsR)

class HMIModule:
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.fsR = 0
        self.fsRButtons = list(range(12))

        self.fsL = 0
        self.fsLButtons = list(range(8))

        self.changed = False
        self.enabled = True

    def getInput(self): # fsTuple = (fsL, fsR)
        self.changed = False
        return (self.fsL, self.fsR)

    def is_changed(self):
        return self.changed

    def is_buttonPressed(self, stick, buttonNum):
        if stick == 'L' or stick == 0:
            return self.fsLButtons[buttonNum - 1]
        elif stick == 'R' or stick == 1:
            return self.fsRButtons[buttonNum - 1]

    def execute(self):
        if self.hmi_interface.is_changedInput():
            (self.fsL, self.fsR) = self.hmi_interface.getInput()
            for i in range(len(self.fsRButtons)):
                self.fsRButtons[i] = self.hmi_interface.getRButton(i+1)
            for i in range(len(self.fsLButtons)):
                self.fsLButtons[i] = self.hmi_interface.getLButton(i+1)
            self.changed = True


