# Image Rectangle Selector Panel


### Author: [Ashok Fernandez](https://github.com/ashokfernandez/)
### Date  : 05 / 12 / 2013

## Description: 
Select an area on an image using a click and drag rectangle in wxPython.

This can be used to graphically measure areas on an image for simple image editing operations such as cropping.

## Usage example

Create an panel with an initial image

    fr = wx.Frame(None, title='test')
    panel = RectangleSelectImagePanel(fr, 'images/Lenna.png')

The initial image is optional. The image can be changed by using the setImage method

    panel.setImage('images/Lenna.png')


When the mouse is clicked and held over the image a dotted rectangle appears
![Image](screenshots/DottedRectangle.png?raw=true)

When the user lets go of the mouse the rectangle turns solid. 
![Image](screenshots/SolidRectangle.png?raw=true)

The origin, width and height of the rectangle are then able to be read. These values are always in pixels and are relative to the original image. For example if a 512x512 image is loaded and the panel is stretched to display the image at 1024x1024, selecting the entire image will still give a result of (0,0) for the origin and (512, 512) for the width and height respectivly. 

## Dependancies
This module depends on
 * [wxPython](http://www.wxpython.org/)
 * [PIL](http://www.pythonware.com/products/pil/)
 * [matplotlib](http://www.matplotlib.org)
