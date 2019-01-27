MMDirectory = "C:\Program Files\Micro-Manager-1.4"

from flask import Flask, redirect, url_for, render_template
from PIL import Image
import atexit
import sys, traceback
sys.path.append(MMDirectory)
import MMCorePy

# Executes when the program exits
def exit_handler():
    # Saving unique id
    f = open("temp/id.txt", 'r+')
    check = int(f.readline())
    if unique_id > check:
        # Delete old id
        f.seek(0)
        f.truncate()
        f.write(str(unique_id))
    f.close()


atexit.register(exit_handler)

# Main program
app = Flask(__name__)

print("starting MicroManager")
mmc = MMCorePy.CMMCore()

mmc.loadDevice('Camera', 'TimepixCamera', 'TimepixCam')
mmc.initializeAllDevices()
mmc.setCameraDevice('Camera')

unique_id = 1  # used to save multiple images

try:
    f = open("temp/id.txt", 'r')
    unique_id = int(f.readline())
    f.close()
except:
    f = open("temp/id.txt", 'w')
    f.write("1")
    f.close()



@app.route('/')
def hello():
    return render_template('index.html', snap_image_url = url_for('snap_image'))

@app.route('/snap-image')
def snap_image():
    try:
        global unique_id
        mmc.snapImage()
        img = mmc.getImage()
        image_url = "static/img" + str(unique_id) + ".tiff"
        Image.fromarray(img).save(image_url)
        unique_id += 1
        success = True
    except : 
        traceback.print_exc()
        success = False
    return render_template('snap_image.html',
    success=success, image_url=image_url, snap_image_url=url_for('snap_image'), index_url=url_for('hello'))