***************
CTid-programmer
***************

A graphical-user interface for programming CTid®-enabled sensors.

This program depends on PySide2.  On many platforms, you can install
it with the command:

    pip3 install PySide2

On some platforms (e.g., Raspian Buster), this may not work and
instead the following command should be used:

    sudo apt install python3-pyside2.{qtcore,qtgui,qtwidgets}

The programmer uses an enhanced version avrdude which can be found here:

    https://bitbucket.org/egauge/avrdude/src/upstream/

Apart from all the normal avrdude features, this version enables
programming of ATtiny microcontrollers with a standard FTDI serial
cable.
