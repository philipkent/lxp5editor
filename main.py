import sys
import gui
import rtmidi
import logging
logger = None
logging.basicConfig(level=logging.DEBUG)


class LXP5App(gui.LXP5GUI):

    global_parameter_map = {

    }

    def __init__(self):
        # init logger
        self.logger = logging.getLogger()

        # init midi
        self.midi = rtmidi.MidiOut()

        # init gui
        super().__init__()

        self.algorithm = 1 # pitch_delay
        #self.algorithm = 2 # delay_reverb

    def __del__(self):
        self.midi.close_port()
        del self.midi

    # delay parameter mappings
    def mapDelay1Time(self, coarseInt, fineInt):
        # coarse time
        if self.algorithm == 1: #pitch/delay
            coarse = (coarseInt/127)*1.0404
        elif self.algorithm == 2: #delay/reverb
            coarse = (coarseInt / 127) * 0.6308

        # fine time
        fine = (fineInt / 127) * 0.0081
        return coarse + fine

    def mapDelay2Time(self, coarseInt, fineInt):
        # coarse time
        if self.algorithm == 1: #pitch/delay
            coarse = (coarseInt/126)*0.3225
        elif self.algorithm == 2: #delay/reverb
            coarse = (coarseInt / 127) * 0.1766

        # fine time
        fine = (fineInt / 127) * 0.0025
        return coarse + fine

    def mapDelay3Time(self, coarseInt, fineInt):
        # coarse time
        if self.algorithm == 1: #pitch/delay
            coarse = (coarseInt/126)*0.3225
        elif self.algorithm == 2: #delay/reverb
            return None

        # fine time
        fine = (fineInt / 127) * 0.0025
        return coarse + fine

    def mapFeedback1(self, amtInt):
        return amtInt/127

    def mapFeedback2(self, amtInt):
        return amtInt/126*0.99

    # pitch parameter mappings
    def mapPitchBase(self, intVal):
        if intVal == 0:
            return "Defeat"
        elif intVal == 1:
            return "-2 octv"
        elif intVal == 2:
            return "-1 octv"
        elif intVal == 3:
            return "Unison"
        else:
            return "?"

    def mapPitchAdjust(self, adjInt):
        return adjInt - 64

    # reverb parameter mappings
    def mapDecayTime(self, timeInt):
        return 0.5 + (timeInt/14)*(12 - 0.5)

    def mapTrebleDecay(self, freqInt):
        if freqInt == 0:
            return "320 Hz"
        elif freqInt == 15:
            return "Full"
        else:
            return "?"

    def mapBassMultiply(self, mulInt):
        return 0.3+(mulInt/31)*(2.5 - 0.3)

    def mapSize(self, sizeInt):
        if sizeInt < 26:
            return 8 + (sizeInt/25)*(26 - 8)
        else:
            return '?'

    def mapDiffusion(self, amtInt):
        return amtInt/100

    # equalization parameter mappings
    def mapHighCutFilter(self, freqInt):
        if freqInt == 0:
            return "320 Hz"
        elif freqInt == 15:
            return "Full"
        else:
            return "?"

    def mapLowCutFilter(self, freqInt):
        if freqInt == 0:
            return "Full"
        elif freqInt == 31:
            return "1350 Hz"
        else:
            return "?"

    # level parameter mappings
    def mapReverbBalance(self, balInt):
        return balInt/127*2-1

    def mapOutputBalance(self, balInt):
        return balInt/127*2-1

    def mapOutputLevel(self, amtInt):
        return amtInt/127

    def mapInputLevel(self, amtInt):
        return amtInt/127

    def mapLFORate(self, freqInt):
        return 0.066 + (freqInt/127)*(10 - 0.066)

    # Generators for LXP-5 Midi implementation
    def sendParamSysex(self, param, value, paramName):
        # bipolar param, take two's complement
        if value < 0:
            value = 2 ** 7 + value

        channel = self.spinbox_midiChannel.value()
        sysex = [0xF0, 6, 5, 0x20 + (channel-1), param, value, 0xF7]
        self.midi.send_message(sysex)
        hexstring = "".join('{:02X} '.format(x) for x in sysex)

        logmsg = "set '{0}' to {1:03} on channel {2:02}  {3}".format(paramName, value, channel, hexstring)
        self.logger.debug(logmsg)

def main():
    app = gui.QtGui.QApplication(sys.argv)
    app.setWindowIcon(gui.QtGui.QIcon('assets/lxp5.png'))
    form = LXP5App()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
