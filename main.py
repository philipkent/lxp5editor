import sys
import gui
import rtmidi


class LXP5App(gui.LXP5GUI):
    def __init__(self):
        # init midi
        self.midi = rtmidi.MidiOut()

        # init gui
        super().__init__()

    def __del__(self):
        self.midi.close_port()
        del self.midi

    # Generators for LXP-5 Midi implementation
    def sendParamSysex(self, param, value, paramName):
        channel = self.spinbox_midiChannel.value()
        sysex = [0xF0, 6, 5, 0x20 + (channel-1), param, value, 0xF7]
        self.midi.send_message(sysex)
        hexstring = "".join('{:02X} '.format(x) for x in sysex)

        logmsg = "set '{0}' to {1:03} on channel {2:02}  {3}".format(paramName, value, channel, hexstring)
        gui.logger.debug(logmsg)

def main():
    app = gui.QtGui.QApplication(sys.argv)
    app.setWindowIcon(gui.QtGui.QIcon('assets/lxp5.png'))
    form = LXP5App()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
