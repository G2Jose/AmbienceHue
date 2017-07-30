# AmbienceHue

A python script that continuously changes Hue lightbulb colors based on what's displayed on the screen. This script uses the Quartz.CoreGraphics module, which is Mac specific. 

[Video](http://www.youtube.com/watch?feature=player_embedded&v=pHmz-tI5FK0)

<div style="text-align:center; align:center"<a href="http://www.youtube.com/watch?feature=player_embedded&v=pHmz-tI5FK0
" target="_blank"><img src="http://img.youtube.com/vi/pHmz-tI5FK0/0.jpg" 
alt="Demo video" width="480" height="360" border="10" /></a></div>

## How to use
### Requirements
- macOS with Xcode & command line tools installed. Tested with macOS 10.12 (Sierra).

- Quartz.CoreGraphics python module

	```bash
	pip install -U pyobjc-core
	pip install -U pyobjc
	```

- PHue python module

	```bash
	pip install phue
	```

- AmbienceHue code

	```bash
	git clone git@github.com:G2Jose/AmbienceHue.git
	```

### Customizing
- Change the value of `BRIDGE_IP` to the IP address of your Hue Bridge. You can find this by logging into your Router's admin page. 
- Change the `LEFT_LIGHT` and `RIGHT_LIGHT` parameters to match your setup. This might require some trial to figure out what numbers map to what lights. 
- The transition time is set to 0.1 ds (0.1 * 1/10th of a second) to avoid the appearance of the lights flickering. 
- By default, the script only watches a strip 1/20th the width of the screen on each side. This setting can be changed by modifying the `WIDTH` parameter.

### Launching
- Navigate to the directory containing the script

	```bash
	cd AmbienceHue
	```

- Launch the script using python (tested on 3.5.2)

	```bash
	python AmbienceHue.py
	```

In case of bugs or issues, get in touch through www.georgejose.com or file a github issue!