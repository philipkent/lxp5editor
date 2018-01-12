# Lexicon LXP-5 Editor

A cross-platform editor for the Lexicon LXP-5 effects processor written in Python.

## Getting Started

To start the editor, run `python main.py`.  Then select your midi interface and the midi channel of your LXP-5 in the
lower left of the editor.  Next, bask in the warmth of no longer having to program the LXP-5 with two knobs.


### Prerequisites

- Python 3
- rtmidi python package
- PyQt3 python package
- Qt 4 Designer (optional)

### Installing

Install Python 3, the [python-rtmidi](https://pypi.python.org/pypi/python-rtmidi) package and the
[PyQt3](https://sourceforge.net/projects/pyqt/files/PyQt3/) python package.

## Editing the GUI design
To make edits to the GUI design install Qt 4 designer, open `design.ui`, make your edits and save `design.ui`.
The updated design is then built with:

`pyuic4 design.ui -o design.py`

## Currently Supported Features
The current version supports editing all delay parameters, pitch parameters, reverb parameters, equalization parameters,
and level parameters on the LXP-5.  Parameters of the current patch are changed through parameter
adjust sysex commands sent to the LXP-5 over MIDI.  Extra abilities such as assigning midi clock destinations will be added in upcoming
versions.

