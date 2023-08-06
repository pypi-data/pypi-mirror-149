alteon2f5
======

This is a simple script to convert Alteon configurations to F5 configuration

Install using pip:

``pip install alteon2f5``

Usage
=====
``$ ./alteon2f5.py
Usage: alteon2f5.py <filename> [partition]``

Output is to stdout and shows statistics about the number of objects and then F5-syntax configuration. 
This F5 configuration can be loaded onto an F5 device using ``tmsh load sys config merge file /var/tmp/<filename> verify``. 
Fix any issues and load with ``tmsh load sys config merge file /var/tmp/<filename>``

Contact me at DevCentral if you would like any configuration added or for bug fixes.
