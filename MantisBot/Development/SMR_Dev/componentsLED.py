from wpilib import PWM

def getDuty(ton, k):
    D = ton*0.001/(k*5.005)
    return D


class LEDModule:
    def __init__(self, channel, multiplier=1):
        self.channel=channel
        self.pwm=PWM(channel)
        self.setMultipier(multiplier)
    
    def setMultiplier(multiplier):
        if multiplier == 1:
            m=PWM.PeriodMultiplier.kPeriodMultiplier_1X

        elif multiplier == 2:
            m=PWM.PeriodMultiplier.kPeriodMultiplier_2X

        elif multiplier == 4:
            m=PWM.PeriodMultiplier.kPeriodMultiplier_4X

        else: 
            m=PWM.PeriodMultiplier.kPeriodMultiplier_1X

        self.pwm.setPeriodMultiplier(m)

        return False

    def disable():
        self.pwm







