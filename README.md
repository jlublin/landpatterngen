LandPatternGen
==============

LandPatternGen is a tool for creating land patterns for PCB design. Patterns are calculated according to IPC-7351 and currently exports to SVG and Eagle.

Requirements
============
Qt5
PyQt5
Sqlite3

Examples
========
Included example library can be used created using:
sqlite3 library.sqlite3 <example.sql

Installing Qt5
--------------
Download Qt5 from https://www.qt.io/download/ and install to directory of your choice.

Compiling PyQt5
---------------

!!!!! This following is initial work, not finished !!!!!

Download sip:
https://www.riverbankcomputing.com/software/sip/download

Download PyQt5:
https://www.riverbankcomputing.com/software/pyqt/download5

python3 configure.py --qmake /<qt-dir>/Qt/5.7/gcc_64/bin/qmake --sip-incdir <include-dir>/python3.4m/ --destdir /home/<user>/.local/lib/python3.4/site-packages/ --sipdir /home/<user>/.local/share/sip/


system:
sip-incdir: /usr/include

local:
sip-incdir: /home/<user>/.local/include




sip:
tar xf sip-4.18.1.tar.gz
cd sp
cd sip-4.18.1/
ls
python3 configure.py
make
make install



cd Downloads/sip-4.18.1/
python3 configure.py -b /home/joachim/Sys/bin/ -d /home/joachim/.local/lib/python3.4/site-packages/ -e /home/joachim/.local/include/python3.4m -v /home/joachim/.local/share/sip
make
make install
