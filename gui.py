from PyQt4 import QtGui
import sys
import design
import logging
logging.basicConfig(level=logging.DEBUG)
logger = None


class LXP5GUI(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # init logger
        handler = QPlainTextEditLogger(self.logConsole)
        global logger
        logger = logging.getLogger()
        logger.addHandler(handler)

        # connect event handlers
        self.__initHandlers()

    def __initHandlers(self):

        # midi configuration
        self.comboBox_midiPort.currentIndexChanged.connect(self.valueChanged_midiPort)
        for port in self.midi.get_ports():
            self.comboBox_midiPort.addItem(port.split(":")[0])

        # delay parameters
        self.btn_loop.clicked[bool].connect(self.clicked_loop)
        self.slider_delay1Coarse.valueChanged.connect(self.valueChanged_delay1Coarse)
        self.slider_delay1Fine.valueChanged.connect(self.valueChanged_delay1Fine)
        self.slider_feedback1.valueChanged.connect(self.valueChanged_feedback1)
        self.slider_delay2Coarse.valueChanged.connect(self.valueChanged_delay2Coarse)
        self.slider_delay2Fine.valueChanged.connect(self.valueChanged_delay2Fine)
        self.slider_feedback2.valueChanged.connect(self.valueChanged_feedback2)
        self.slider_delay3Coarse.valueChanged.connect(self.valueChanged_delay3Coarse)
        self.slider_delay3Fine.valueChanged.connect(self.valueChanged_delay3Fine)

        # pitch parameters
        self.slider_pitchBase.valueChanged.connect(self.valueChanged_pitchBase)
        self.slider_pitchInterval.valueChanged.connect(self.valueChanged_pitchInterval)
        self.slider_pitchAdjust.valueChanged.connect(self.valueChanged_pitchAdjust)

        # reverb parameters
        self.slider_decayTime.valueChanged.connect(self.valueChanged_decayTime)
        self.slider_trebleDecay.valueChanged.connect(self.valueChanged_trebleDecay)
        self.slider_bassMultiply.valueChanged.connect(self.valueChanged_bassMultiply)
        self.slider_size.valueChanged.connect(self.valueChanged_size)
        self.slider_diffusion.valueChanged.connect(self.valueChanged_diffusion)

        # equalization parameters
        self.slider_highCutFilter.valueChanged.connect(self.valueChanged_highCutFilter)
        self.slider_lowCutFilter.valueChanged.connect(self.valueChanged_lowCutFilter)

        # level parameters
        self.slider_reverbBalance.valueChanged.connect(self.valueChanged_reverbBalance)
        self.slider_outputBalance.valueChanged.connect(self.valueChanged_outputBalance)
        self.slider_outputLevel.valueChanged.connect(self.valueChanged_outputLevel)
        self.slider_inputLevel.valueChanged.connect(self.valueChanged_inputLevel)
        self.slider_LFORate.valueChanged.connect(self.valueChanged_LFORate)

    # delay parameter handlers
    def clicked_loop(self, pressed):
        if pressed:
            val = 127
        else:
            val = 0

        self.slider_feedback1.setValue(val)
        self.valueChanged_feedback1()

    def valueChanged_midiPort(self):
        name = self.comboBox_midiPort.currentText()
        idx = self.comboBox_midiPort.currentIndex()
        self.midi.close_port()
        self.midi.open_port(idx)
        logger.debug("opened midi port {0} index:{1}".format(name, idx))

    def valueChanged_delay1Coarse(self):
        value = self.slider_delay1Coarse.value()
        self.label_delay1Coarse.setText(str(value))
        self.sendParamSysex(0, value, "delay 1 coarse")

    def valueChanged_delay1Fine(self):
        value = self.slider_delay2Fine.value()
        self.label_delay1Fine.setText(str(value))
        self.sendParamSysex(1, value, "delay 1 fine")

    def valueChanged_feedback1(self):
        value = self.slider_feedback1.value()
        self.label_feedback1.setText(str(value))
        self.sendParamSysex(2, value, "feedback 1")

    def valueChanged_delay2Coarse(self):
        value = self.slider_delay2Coarse.value()
        self.label_delay2Coarse.setText(str(value))
        self.sendParamSysex(3, value, "delay 2 coarse")

    def valueChanged_delay2Fine(self):
        value = self.slider_delay2Fine.value()
        self.label_delay2Fine.setText(str(value))
        self.sendParamSysex(4, value, "delay 2 fine")

    def valueChanged_feedback2(self):
        value = self.slider_feedback2.value()
        self.label_feedback2.setText(str(value))
        self.sendParamSysex(5, value, "feedback 2")

    def valueChanged_delay3Coarse(self):
        value = self.slider_delay3Coarse.value()
        self.label_delay3Coarse.setText(str(value))
        self.sendParamSysex(6, value, "delay 3 coarse")

    def valueChanged_delay3Fine(self):
        value = self.slider_delay3Fine.value()
        self.label_delay3Fine.setText(str(value))
        self.sendParamSysex(7, value, "delay 3 fine")

    # pitch parameter handlers
    def valueChanged_pitchBase(self):
        value = self.slider_pitchBase.value()
        self.label_pitchBase.setText(str(value))
        self.sendParamSysex(8, value, "pitch base")

    def valueChanged_pitchInterval(self):
        value = self.slider_pitchInterval.value()
        self.label_pitchInterval.setText(str(value))
        self.sendParamSysex(9, value, "pitch interval")

    def valueChanged_pitchAdjust(self):
        value = self.slider_pitchAdjust.value()
        self.label_pitchAdjust.setText(str(value))
        self.sendParamSysex(10, value, "pitch adjust")

    # reverb parameter handlers
    def valueChanged_decayTime(self):
        value = self.slider_decayTime.value()
        self.label_decayTime.setText(str(value))
        self.sendParamSysex(11, value, "decay time")

    def valueChanged_trebleDecay(self):
        value = self.slider_trebleDecay.value()
        self.label_trebleDecay.setText(str(value))
        self.sendParamSysex(12, value, "treble decay")

    def valueChanged_bassMultiply(self):
        value = self.slider_bassMultiply.value()
        self.label_bassMultiply.setText(str(value))
        self.sendParamSysex(13, value, "bass multiply")

    def valueChanged_size(self):
        value = self.slider_size.value()
        self.label_size.setText(str(value))
        self.sendParamSysex(14, value, "size")

    def valueChanged_diffusion(self):
        value = self.slider_diffusion.value()
        self.label_diffusion.setText(str(value))
        self.sendParamSysex(15, value, "diffusion")

    # balance parameter handlers
    def valueChanged_highCutFilter(self):
        value = self.slider_highCutFilter.value()
        self.label_highCutFilter.setText(str(value))
        self.sendParamSysex(16, value, "high cut filter")

    def valueChanged_lowCutFilter(self):
        value = self.slider_lowCutFilter.value()
        self.label_lowCutFilter.setText(str(value))
        self.sendParamSysex(17, value, "low cut filter")

    # reverb parameter handlers
    def valueChanged_reverbBalance(self):
        value = self.slider_reverbBalance.value()
        self.label_reverbBalance.setText(str(value))
        self.sendParamSysex(18, value, "reverb balance")

    def valueChanged_outputBalance(self):
        value = self.slider_outputBalance.value()
        self.label_outputBalance.setText(str(value))
        self.sendParamSysex(19, value, "output balance")

    def valueChanged_outputLevel(self):
        value = self.slider_outputLevel.value()
        self.label_outputLevel.setText(str(value))
        self.sendParamSysex(20, value, "output level")

    def valueChanged_inputLevel(self):
        value = self.slider_inputLevel.value()
        self.label_inputLevel.setText(str(value))
        self.sendParamSysex(22, value, "input level")

    def valueChanged_LFORate(self):
        value = self.slider_LFORate.value()
        self.label_LFORate.setText(str(value))
        self.sendParamSysex(22, value, "lfo rate")


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super(self.__class__, self).__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)