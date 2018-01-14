from PyQt4 import QtGui
import sys
import design
import midi_implementation


class LXP5GUI(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # load combo box items & update labels
        self.__initGui()

        # connect event handlers
        self.__initMidiHandlers()
        self.__initDelayHandlers()
        self.__initPitchHandlers()
        self.__initReverbHandlers()
        self.__initEqualizationHandlers()
        self.__initLevelHandlers()
        self.__initPatchHandlers()

    def __initGui(self):
        # init comboboxes
        for port in self.midi.get_ports():
            self.comboBox_midiPort.addItem(port.split(":")[0])

        # main patch sources
        d1 = {key:value for key, value in midi_implementation.source_control_numbers.items() if key > 63}
        for num, label in d1.items():
            self.comboBox_patch1Source.addItem(label, num)
            self.comboBox_patch2Source.addItem(label, num)
            self.comboBox_patch3Source.addItem(label, num)
            self.comboBox_patch4Source.addItem(label, num)

        # remaining patch cc sources
        d2 = {key: value for key, value in midi_implementation.source_control_numbers.items() if key < 64}
        for num, label in d2.items():
            self.comboBox_patch1Source.addItem(label, num)
            self.comboBox_patch2Source.addItem(label, num)
            self.comboBox_patch3Source.addItem(label, num)
            self.comboBox_patch4Source.addItem(label, num)

        # patch destinations
        for num, label in midi_implementation.parameter_numbers.items():
            self.comboBox_patch1Destination.addItem(label, num)
            self.comboBox_patch2Destination.addItem(label, num)
            self.comboBox_patch3Destination.addItem(label, num)
            self.comboBox_patch4Destination.addItem(label, num)

        # init equalization parameter labels
        self.updateLabel_highCutFilter(self.slider_highCutFilter.value())
        self.updateLabel_lowCutFilter(self.slider_lowCutFilter.value())

        # init level parameter labels
        self.updateLabel_reverbBalance(self.slider_reverbBalance.value())
        self.updateLabel_outputBalance(self.slider_outputBalance.value())
        self.updateLabel_outputLevel(self.slider_outputLevel.value())
        self.updateLabel_inputLevel(self.slider_inputLevel.value())
        self.updateLabel_LFORate(self.slider_LFORate.value())


    def __initMidiHandlers(self):
        # connect midi configuration event handlers
        self.comboBox_midiPort.currentIndexChanged.connect(self.currentIndexChanged_midiPort)

    def __initDelayHandlers(self):
        # connect delay parameter event handlers
        self.btn_loop.clicked[bool].connect(self.clicked_loop)
        self.slider_delay1Coarse.valueChanged.connect(self.valueChanged_delay1Coarse)
        self.slider_delay1Fine.valueChanged.connect(self.valueChanged_delay1Fine)
        self.slider_feedback1.valueChanged.connect(self.valueChanged_feedback1)
        self.slider_delay2Coarse.valueChanged.connect(self.valueChanged_delay2Coarse)
        self.slider_delay2Fine.valueChanged.connect(self.valueChanged_delay2Fine)
        self.slider_feedback2.valueChanged.connect(self.valueChanged_feedback2)
        self.slider_delay3Coarse.valueChanged.connect(self.valueChanged_delay3Coarse)
        self.slider_delay3Fine.valueChanged.connect(self.valueChanged_delay3Fine)

    def __initPitchHandlers(self):
        # connect pitch parameter event handlers
        self.slider_pitchBase.valueChanged.connect(self.valueChanged_pitchBase)
        self.slider_pitchInterval.valueChanged.connect(self.valueChanged_pitchInterval)
        self.slider_pitchAdjust.valueChanged.connect(self.valueChanged_pitchAdjust)

    def __initReverbHandlers(self):
        # connect reverb parameter event handlers
        self.slider_decayTime.valueChanged.connect(self.valueChanged_decayTime)
        self.slider_trebleDecay.valueChanged.connect(self.valueChanged_trebleDecay)
        self.slider_bassMultiply.valueChanged.connect(self.valueChanged_bassMultiply)
        self.slider_size.valueChanged.connect(self.valueChanged_size)
        self.slider_diffusion.valueChanged.connect(self.valueChanged_diffusion)

    def __initEqualizationHandlers(self):
        # connect equalization parameter event handlers
        self.slider_highCutFilter.valueChanged.connect(self.valueChanged_highCutFilter)
        self.slider_lowCutFilter.valueChanged.connect(self.valueChanged_lowCutFilter)

    def __initLevelHandlers(self):
        # connect level parameter event handlers
        self.slider_reverbBalance.valueChanged.connect(self.valueChanged_reverbBalance)
        self.slider_outputBalance.valueChanged.connect(self.valueChanged_outputBalance)
        self.slider_outputLevel.valueChanged.connect(self.valueChanged_outputLevel)
        self.slider_inputLevel.valueChanged.connect(self.valueChanged_inputLevel)
        self.slider_LFORate.valueChanged.connect(self.valueChanged_LFORate)

    def __initPatchHandlers(self):
        # connect patch event handlers
        self.comboBox_patch1Source.currentIndexChanged.connect(self.currentIndexChanged_patch1Source)
        self.comboBox_patch2Source.currentIndexChanged.connect(self.currentIndexChanged_patch2Source)
        self.comboBox_patch3Source.currentIndexChanged.connect(self.currentIndexChanged_patch3Source)
        self.comboBox_patch4Source.currentIndexChanged.connect(self.currentIndexChanged_patch4Source)
        self.comboBox_patch1Destination.currentIndexChanged.connect(self.currentIndexChanged_patch1Destination)
        self.comboBox_patch2Destination.currentIndexChanged.connect(self.currentIndexChanged_patch2Destination)
        self.comboBox_patch3Destination.currentIndexChanged.connect(self.currentIndexChanged_patch3Destination)
        self.comboBox_patch4Destination.currentIndexChanged.connect(self.currentIndexChanged_patch4Destination)
        self.dial_patch1Threshold.valueChanged.connect(self.valueChanged_patch1Threshold)
        self.dial_patch2Threshold.valueChanged.connect(self.valueChanged_patch2Threshold)
        self.dial_patch3Threshold.valueChanged.connect(self.valueChanged_patch3Threshold)
        self.dial_patch4Threshold.valueChanged.connect(self.valueChanged_patch4Threshold)
        self.dial_patch1ScaleFactor.valueChanged.connect(self.valueChanged_patch1ScaleFactor)
        self.dial_patch2ScaleFactor.valueChanged.connect(self.valueChanged_patch2ScaleFactor)
        self.dial_patch3ScaleFactor.valueChanged.connect(self.valueChanged_patch3ScaleFactor)
        self.dial_patch4ScaleFactor.valueChanged.connect(self.valueChanged_patch4ScaleFactor)

    # delay parameter label updaters
    def updateLabel_delay1Time(self, coarseInt, fineInt):
        sec = self.mapDelay1Time(coarseInt, fineInt)
        ms = sec * 1000
        if sec < 1:
            unit = ' ms'
            time = round(ms, 1)
        else:
            time = round(sec, 4)
            unit = ' s'
        self.label_delay1Time.setText(str(time) + unit)

    def updateLabel_delay2Time(self, coarseInt, fineInt):
        time = self.mapDelay2Time(coarseInt, fineInt)
        self.label_delay2Time.setText(str(round(time*1000, 1)) + ' ms')

    def updateLabel_delay3Time(self, coarseInt, fineInt):
        time = self.mapDelay3Time(coarseInt, fineInt)
        self.label_delay3Time.setText(str(round(time*1000, 1)) + ' ms')

    def updateLabel_feedback1(self, amtInt):
        amt = self.mapFeedback1(amtInt)
        self.label_feedback1.setText(str(round(amt * 100, 1)) + '%')

    def updateLabel_feedback2(self, amtInt):
        amt = self.mapFeedback2(amtInt)
        self.label_feedback2.setText(str(round(amt * 100, 1)) + '%')

    # pitch parameter label updaters
    def updateLabel_pitchBase(self, baseInt):
        baseStr = self.mapPitchBase(baseInt)
        self.label_pitchBase.setText(baseStr)

    def updateLabel_pitchInterval(self, intervalInt):
        intervalStr = str(intervalInt)
        if intervalInt >= 0:
            intervalStr = "+"+intervalStr
        self.label_pitchInterval.setText(intervalStr+" st")

    def updateLabel_pitchAdjust(self, adjustInt):
        mapped = self.mapPitchAdjust(adjustInt)
        if mapped >= 0:
            adjustStr = "+"+str(mapped)
        else:
            adjustStr = str(mapped)
        self.label_pitchAdjust.setText(adjustStr)

    # reverb parameter label updaters
    def updateLabel_decayTime(self, timeInt):
        sec = self.mapDecayTime(timeInt)
        self.label_decayTime.setText(str(round(sec,1))+" sec")

    def updateLabel_trebleDecay(self, freqInt):
        freqStr = self.mapTrebleDecay(freqInt)
        self.label_trebleDecay.setText(freqStr)

    def updateLabel_bassMultiply(self, mulInt):
        val = self.mapBassMultiply(mulInt)
        self.label_bassMultiply.setText('x'+str(round(val, 2)))

    def updateLabel_size(self, sizeInt):
        size = self.mapSize(sizeInt)
        if size is not '?':
            self.label_size.setText(str(round(size, 1))+' m')
        else:
            self.label_size.setText('?')

    def updateLabel_diffusion(self, amtInt):
        amtPerc = self.mapDiffusion(amtInt)
        self.label_diffusion.setText(str(round(amtPerc*100, 1))+"%")

    # equalization parameter label updaters
    def updateLabel_highCutFilter(self, freqInt):
        freqStr = self.mapHighCutFilter(freqInt)
        self.label_highCutFilter.setText(freqStr)

    def updateLabel_lowCutFilter(self, freqInt):
        freqStr = self.mapLowCutFilter(freqInt)
        self.label_lowCutFilter.setText(freqStr)

    # level parameter label updaters
    def updateLabel_reverbBalance(self, balInt):
        bal = self.mapReverbBalance(balInt)
        bal = round(bal, 2)
        if bal > 0:
            balStr = "+"+str(bal)
        elif bal < 0:
            balStr = str(bal)
        else:
            balStr = str(bal)
        self.label_reverbBalance.setText(balStr)

    def updateLabel_outputBalance(self, balInt):
        bal = self.mapOutputBalance(balInt)
        bal = round(bal, 2)
        if bal > 0:
            balStr = "+" + str(bal)
        elif bal < 0:
            balStr = str(bal)
        else:
            balStr = str(bal)
        self.label_outputBalance.setText(balStr)

    def updateLabel_outputLevel(self, amtInt):
        amt = self.mapOutputLevel(amtInt)
        self.label_outputLevel.setText(str(round(amt*100, 1))+"%")

    def updateLabel_inputLevel(self, amtInt):
        amt = self.mapInputLevel(amtInt)
        self.label_inputLevel.setText(str(round(amt*100, 1))+"%")

    def updateLabel_LFORate(self, freqInt):
        freqHz = self.mapLFORate(freqInt)
        bpm = freqHz*60
        self.label_LFORateHz.setText(str(round(freqHz, 3))+" Hz")
        self.label_LFORateBPM.setText(str(round(bpm,2))+" bpm")

    # midi configuration event handlers
    def currentIndexChanged_midiPort(self):
        name = self.comboBox_midiPort.currentText()
        idx = self.comboBox_midiPort.currentIndex()
        self.midi.close_port()
        self.midi.open_port(idx)
        self.logger.debug("opened midi port {0} index:{1}".format(name, idx))

    # delay parameter event handlers
    def clicked_loop(self, pressed):
        if pressed:
            val = 127
        else:
            val = 0

        self.slider_feedback1.setValue(val)
        self.valueChanged_feedback1()

    def valueChanged_delay1Coarse(self):
        value = self.slider_delay1Coarse.value()
        self.sendParamSysex(0, value, "delay 1 coarse")
        self.updateLabel_delay1Time(value, self.slider_delay1Fine.value())

    def valueChanged_delay1Fine(self):
        value = self.slider_delay1Fine.value()
        self.sendParamSysex(1, value, "delay 1 fine")
        self.updateLabel_delay1Time(self.slider_delay1Coarse.value(), value)

    def valueChanged_feedback1(self):
        value = self.slider_feedback1.value()
        self.sendParamSysex(2, value, "feedback 1")
        self.updateLabel_feedback1(value)

    def valueChanged_delay2Coarse(self):
        value = self.slider_delay2Coarse.value()
        self.sendParamSysex(3, value, "delay 2 coarse")
        self.updateLabel_delay2Time(value, self.slider_delay2Fine.value())

    def valueChanged_delay2Fine(self):
        value = self.slider_delay2Fine.value()
        self.sendParamSysex(4, value, "delay 2 fine")
        self.updateLabel_delay2Time(self.slider_delay2Coarse.value(), value)

    def valueChanged_feedback2(self):
        value = self.slider_feedback2.value()
        self.sendParamSysex(5, value, "feedback 2")
        self.updateLabel_feedback2(value)

    def valueChanged_delay3Coarse(self):
        value = self.slider_delay3Coarse.value()
        self.sendParamSysex(6, value, "delay 3 coarse")
        self.updateLabel_delay3Time(value, self.slider_delay3Fine.value())

    def valueChanged_delay3Fine(self):
        value = self.slider_delay3Fine.value()
        self.sendParamSysex(7, value, "delay 3 fine")
        self.updateLabel_delay3Time(self.slider_delay3Coarse.value(), value)

    # pitch parameter handlers
    def valueChanged_pitchBase(self):
        value = self.slider_pitchBase.value()
        self.sendParamSysex(8, value, "pitch base")
        self.updateLabel_pitchBase(value)

    def valueChanged_pitchInterval(self):
        value = self.slider_pitchInterval.value()
        self.sendParamSysex(9, value, "pitch interval")
        self.updateLabel_pitchInterval(value)

    def valueChanged_pitchAdjust(self):
        value = self.slider_pitchAdjust.value()
        self.sendParamSysex(10, value, "pitch adjust")
        self.updateLabel_pitchAdjust(value)

    # reverb parameter handlers
    def valueChanged_decayTime(self):
        value = self.slider_decayTime.value()
        self.sendParamSysex(11, value, "decay time")
        self.updateLabel_decayTime(value)

    def valueChanged_trebleDecay(self):
        value = self.slider_trebleDecay.value()
        self.sendParamSysex(12, value, "treble decay")
        self.updateLabel_trebleDecay(value)

    def valueChanged_bassMultiply(self):
        value = self.slider_bassMultiply.value()
        self.sendParamSysex(13, value, "bass multiply")
        self.updateLabel_bassMultiply(value)

    def valueChanged_size(self):
        value = self.slider_size.value()
        self.sendParamSysex(14, value, "size")
        self.updateLabel_size(value)

    def valueChanged_diffusion(self):
        value = self.slider_diffusion.value()
        self.sendParamSysex(15, value, "diffusion")
        self.updateLabel_diffusion(value)

    # equalization parameter handlers
    def valueChanged_highCutFilter(self):
        value = self.slider_highCutFilter.value()
        self.sendParamSysex(16, value, "high cut filter")
        self.updateLabel_highCutFilter(value)

    def valueChanged_lowCutFilter(self):
        value = self.slider_lowCutFilter.value()
        self.sendParamSysex(17, value, "low cut filter")
        self.updateLabel_lowCutFilter(value)

    # balance parameter handlers
    def valueChanged_reverbBalance(self):
        value = self.slider_reverbBalance.value()
        self.sendParamSysex(18, value, "reverb balance")
        self.updateLabel_reverbBalance(value)

    def valueChanged_outputBalance(self):
        value = self.slider_outputBalance.value()
        self.sendParamSysex(19, value, "output balance")
        self.updateLabel_outputBalance(value)

    def valueChanged_outputLevel(self):
        value = self.slider_outputLevel.value()
        self.sendParamSysex(20, value, "output level")
        self.updateLabel_outputLevel(value)

    def valueChanged_inputLevel(self):
        value = self.slider_inputLevel.value()
        self.sendParamSysex(21, value, "input level")
        self.updateLabel_inputLevel(value)

    def valueChanged_LFORate(self):
        value = self.slider_LFORate.value()
        self.sendParamSysex(22, value, "lfo rate")
        self.updateLabel_LFORate(value)

    # patch1 event handlers
    def currentIndexChanged_patch1Source(self):
        controlnum = self.comboBox_patch1Source.itemData(self.comboBox_patch1Source.currentIndex())
        self.sendParamSysex(44, controlnum, "patch 1 source")

    def valueChanged_patch1Threshold(self):
        value = self.dial_patch1Threshold.value()
        self.sendParamSysex(45, value, "patch 1 threshold")

    def currentIndexChanged_patch1Destination(self):
        idx = self.comboBox_patch1Destination.currentIndex()
        self.sendParamSysex(46, idx, "patch 1 destination")

    def valueChanged_patch1ScaleFactor(self):
        value = self.dial_patch1ScaleFactor.value()
        self.sendParamSysex(47, value, "patch 1 scale factor")

    # patch2 event handlers
    def currentIndexChanged_patch2Source(self):
        idx = self.comboBox_patch2Source.currentIndex()
        self.sendParamSysex(49, idx, "patch 2 source")

    def valueChanged_patch2Threshold(self):
        value = self.dial_patch2Threshold.value()
        self.sendParamSysex(50, value, "patch 2 threshold")

    def currentIndexChanged_patch2Destination(self):
        idx = self.comboBox_patch2Destination.currentIndex()
        self.sendParamSysex(51, idx, "patch 2 destination")


    def valueChanged_patch2ScaleFactor(self):
        value = self.dial_patch2ScaleFactor.value()
        self.sendParamSysex(52, value, "patch 2 scale factor")

    # patch3 event handlers
    def currentIndexChanged_patch3Source(self):
        idx = self.comboBox_patch3Source.currentIndex()
        self.sendParamSysex(54, idx, "patch 3 source")

    def valueChanged_patch3Threshold(self):
        value = self.dial_patch3Threshold.value()
        self.sendParamSysex(55, value, "patch 3 threshold")

    def currentIndexChanged_patch3Destination(self):
        idx = self.comboBox_patch3Destination.currentIndex()
        self.sendParamSysex(56, idx, "patch 3 destination")

    # bipolar param
    def valueChanged_patch3ScaleFactor(self):
        value = self.dial_patch3ScaleFactor.value()
        self.sendParamSysex(57, value, "patch 3 scale factor")

    # patch4 event handlers
    def currentIndexChanged_patch4Source(self):
        idx = self.comboBox_patch4Source.currentIndex()
        self.sendParamSysex(59, idx, "patch 4 source")

    def valueChanged_patch4Threshold(self):
        value = self.dial_patch4Threshold.value()
        self.sendParamSysex(60, value, "patch 4 threshold")

    def currentIndexChanged_patch4Destination(self):
        idx = self.comboBox_patch4Destination.currentIndex()
        self.sendParamSysex(61, idx, "patch 4 destination")

    def valueChanged_patch4ScaleFactor(self):
        value = self.dial_patch4ScaleFactor.value()
        self.sendParamSysex(62, value, "patch 4 scale factor")