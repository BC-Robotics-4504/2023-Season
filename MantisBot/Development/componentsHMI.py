import wpilib

class FlightStickHMI:
    def __init__(self, stickLeft_ID, stickRight_ID):
        self.leftStick = wpilib.Joystick(stickLeft_ID)
        self.rightStick = wpilib.Joystick(stickRight_ID)
        
        self.fsR = 0
        self.fsRButtons = {i:{'value':False, 'changed':False} for i in range(1, self.rightStick.getButtonCount())}
        
        self.fsL = 0
        self.fsLButtons = {i:{'value':False, 'changed':False} for i in range(1, self.leftStick.getButtonCount())}

        self.changed = True

        self.DEADZONE = .1

    def updateLeftButtons(self):
        for button in self.fsLButtons.keys():
            rawVal = self.leftStick.getRawButtonPressed(button)
            self.fsLButtons[button]['value'] = rawVal
        return False
    
    def updateRightButtons(self):
        for button in self.fsRButtons.keys():
            rawVal = self.rightStick.getRawButton(button)
            self.fsRButtons[button]['value'] = rawVal
        return False
    
    def getLeftButtons(self, button_id):
        value = self.fsLButtons[button_id]['value']
        self.fsLButtons[button_id]['changed'] = False
        return value
    
    def getRightButtons(self, button_id):
        value = self.fsRButtons[button_id]['value']
        self.fsRButtons[button_id]['changed'] = False
        return value
    
    def updateLeftSick(self):
        # Left Stick Commands
        fsL = self.leftStick.getY()
        if abs(fsL) < self.DEADZONE:
            fsL = 0
        self.fsL = fsL
        return False

    def updateRightSick(self):
        # Right Stick Commands
        fsR = self.rightStick.getY()
        if abs(fsR) < self.DEADZONE:
            fsR = 0
        self.fsR = fsR
        return False

    def getInput(self):
        return (self.fsL, self.fsR)

class HMIModule:
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.fsR = 0
        self.fsRButtons = list(range(11))

        self.fsL = 0
        self.fsLButtons = list(range(11))

        self.changed = False
        self.enabled = True

    def getInput(self): # fsTuple = (fsL, fsR)
        self.changed = False
        return (self.fsL, self.fsR)
    
    def getLeftButton(self, button_id):
        if button_id in self.hmi_interface.fsLButtons.keys():
            value = self.hmi_interface.getLeftButtons(button_id)
            return value
        else:
            return False
    
    def getRightButton(self, button_id):
        if button_id in self.hmi_interface.fsRButtons.keys():
            value = self.hmi_interface.getRightButtons(button_id)
            return value
        else:
            return False

    def is_changed(self):
        return self.changed
    
    def execute(self):     
        self.hmi_interface.updateLeftButtons()
        self.hmi_interface.updateRightButtons()       

        self.hmi_interface.updateLeftSick()
        self.hmi_interface.updateRightSick()

        (self.fsL, self.fsR) = self.hmi_interface.getInput()
        