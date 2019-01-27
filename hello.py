MMDirectory = "C:\Program Files\Micro-Manager-1.4"

from flask import Flask, redirect, url_for, render_template
from PIL import Image
import sys, traceback
sys.path.append(MMDirectory)
import MMCorePy

app = Flask(__name__)

print("starting MicroManager")
mmc = MMCorePy.CMMCore()

mmc.loadDevice('Camera', 'TimepixCamera', 'TimepixCam')
mmc.initializeAllDevices()
mmc.setCameraDevice('Camera')

@app.route('/')
def hello():
    return render_template('index.html', snap_image_url = url_for('snap_image'))

@app.route('/snap-image')
def snap_image():
    try:
        mmc.snapImage()
        img = mmc.getImage()
        Image.fromarray(img).save('temp/image.tiff')
        success = True
    except : 
        traceback.print_exc()
        success = False
    return render_template('snap_image.html',
    success=success, snap_image_url=url_for('snap_image'), index_url=url_for('hello'))