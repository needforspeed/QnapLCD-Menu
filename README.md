# QnapLCD-Menu

A simplistic package and examples using the front panel display and buttons
on QNAP NAS devices under other operating systems. Tested with TVS-671,
but should work on other models that use the "A125" display with two buttons.

# What's Included

In most cases you would setup *preinit.py*, *lcd-menu.py*, and *shutdown.py* to get a workable menu on the Qnap LCD.

* *preinit.py* a short pre-initialization script to print a message on the LCD panel and terminate.

* *postinit.py* a short post-initialization script to print a message on the LCD panel and terminate. Not used in most cases.

* *lcd-menu.py* a Python script that will display a menu similar to the default QNAP menu, written for TrueNAS SCALE but may work with other TrueNAS and FreeNAS systems. This should take the place of the *postinit.py* script if you want the menu system active.

* *shutdown* a short shutdown script to print a message on the LCD panel and terminate.

* *qnaplcd* Python package (class) for using the front-panel (A125) display. Uses *pyserial* and threading to send button events to calling program.

# Installation

To install, clone this repository onto your NAS somewhere that is accessible to the admin (root) user. It needs to be run *as root* to communicate with the display and the TrueNAS CLI.

To communicate with the display, *pyserial* is required. If you are able to install it with `pip`, that's wonderful, do that!

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
./clear-and-turn-off-backlight.py
```


# Using

Add `lcd-menu.py` in TrueNAS SCALE under *System Settings*, *Advanced*, *Init/Shutdown Scripts* as a pre or post init script.

