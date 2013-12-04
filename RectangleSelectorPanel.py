# -------------------------------------------------------------------------------------------------------------------
#  wxPython Rectangle Selector Panel : Select an area on an image using a click and drag rectangle in wxPython 
# -------------------------------------------------------------------------------------------------------------------
# 
# Author: Ashok Fernandez - https://github.com/ashokfernandez/
# Date  : 05 / 12 / 2013
# 
# Description: 
# Select an area on an image using a click and drag rectangle in wxPython.
# This can be used to graphically measure areas on an image for simple image editing operations such as cropping.
# 
# Licence: 
# Copyright Ashok Fernandez 2013
# Released under the MIT license - http://opensource.org/licenses/MIT
# 
# Usage example: 
# See the bottom of this file. The demo can be run by running this file.
# -------------------------------------------------------------------------------------------------------------------

# Used to determine the size of an image
from PIL import Image   

# Use the wxPython backend of matplotlib
import matplotlib       
matplotlib.use('WXAgg')

# Matplotlib elements used to draw the bounding rectangle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# wxPython stuff for the demo
import wx


# --------------------------------------------------------------------------------------------------------------------
# CLASSES
# --------------------------------------------------------------------------------------------------------------------

class RectangleSelectImagePanel(wx.Panel):
    ''' Panel that contains an image that allows the users to select an area of the image with the mouse. The user clicks and
    holds the mouse to create a dotted rectangle, and when the mouse is released the rectangles origin, width and height can be
    read. The dimensions of these readings are always relative to the original image, so even if the image is scaled up larger
    to fit the panel the measurements will always refer to the original image.'''

    def __init__(self, parent, pathToImage=None):
    	''' Initialise the panel. Setting an initial image is optional.'''
        
        # Initialise the parent
        wx.Panel.__init__(self, parent)

        # Intitialise the matplotlib figure
        self.figure = plt.figure()

        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure,[0,0,1,1])      
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes) 

        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Initialise the rectangle
        self.rect = Rectangle((0,0), 1, 1, facecolor='None', edgecolor='green')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.axes.add_patch(self.rect)
        
        # Sizer to contain the canvas
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP)
        self.SetSizer(self.sizer)
        self.Fit()
        
        # Connect the mouse events to their relevant callbacks
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        # Lock to stop the motion event from behaving badly when the mouse isn't pressed
        self.pressed = False

        # If there is an initial image, display it on the figure
        if pathToImage is not None:
            self.setImage(pathToImage)


    def on_press(self, event):
    	''' Callback to handle the mouse being clicked and held over the canvas'''

    	# Check the mouse press was actually on the canvas
    	if event.xdata is not None and event.ydata is not None:

        	# Upon initial press of the mouse record the origin and record the mouse as pressed
        	self.pressed = True
        	self.rect.set_linestyle('dashed')
        	self.x0 = event.xdata
        	self.y0 = event.ydata


    def on_release(self, event):
    	'''Callback to handle the mouse being released over the canvas'''

    	# Check that the mouse was actually pressed on the canvas to begin with and this isn't a rouge mouse 
    	# release event that started somewhere else
    	if self.pressed:

            # Upon release draw the rectangle as a solid rectangle
            self.pressed = False
            self.rect.set_linestyle('solid')

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
	        	self.x1 = event.xdata
	        	self.y1 = event.ydata

            # Set the width and height and origin of the bounding rectangle
            self.boundingRectWidth =  self.x1 - self.x0
            self.boundingRectHeight =  self.y1 - self.y0
            self.bouningRectOrigin = (self.x0, self.y0)

            # Draw the bounding rectangle
            self.rect.set_width(self.boundingRectWidth)
            self.rect.set_height(self.boundingRectHeight)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()


    def on_motion(self, event):
    	'''Callback to handle the motion event created by the mouse moving over the canvas'''

    	# If the mouse has been pressed draw an updated rectangle when the mouse is moved so 
    	# the user can see what the current selection is
    	if self.pressed:

    		# Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
	        # height as the last values set by the motion event
        	if event.xdata is not None and event.ydata is not None:
	        	self.x1 = event.xdata
	        	self.y1 = event.ydata
    		
    		# Set the width and height and draw the rectangle
        	self.rect.set_width(self.x1 - self.x0)
        	self.rect.set_height(self.y1 - self.y0)
        	self.rect.set_xy((self.x0, self.y0))
        	self.canvas.draw()


    def setImage(self, pathToImage):
    	'''Sets the background image of the canvas'''
    	
        # Load the image into matplotlib and PIL
    	image = matplotlib.image.imread(pathToImage) 
        imPIL = Image.open(pathToImage) 

        # Save the image's dimensions from PIL
        self.imageSize = imPIL.size
        
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(image,aspect='equal') 
        self.canvas.draw()



# --------------------------------------------------------------------------------------------------------------------
# DEMO
# --------------------------------------------------------------------------------------------------------------------        

if __name__ == "__main__":

    # Create an demo application
    app = wx.App()

    # Create a frame and a RectangleSelectorPanel
    fr = wx.Frame(None, title='test')
    panel = RectangleSelectImagePanel(fr)
    
    # Set the image in the panel
    panel.setImage('images/Lenna.png')
    
    # Start the demo app
    fr.Show()
    app.MainLoop()

    
