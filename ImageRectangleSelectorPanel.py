
# Used to determine the size of an image
from PIL import Image

# matplotlib.image requires PIL
import matplotlib
matplotlib.use('WXAgg')

# Matplotlib elements used to draw the bounding rectangle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# GUI stuff
import wx









class RectangleSelectImagePanel(wx.Panel):
    def __init__(self, parent, pathToImage=None):
    	''' Initialise a canvas panel'''
        wx.Panel.__init__(self, parent)

        # Intitialise the matplotlib figure, canvas and axes
        # REFERNCE: http://stackoverflow.com/questions/18154337/matplotlib-subplot-with-image-background
        self.figure = plt.figure() # Init the figure
        # image = matplotlib.image.imread('images/Lenna.png') # Load the image into matplotlib
        # imPIL = Image.open('images/Lenna.png') # Load the image using PIL to get it's dimensions
        # imageSize = imPIL.size
        # print imageSize

        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure,[0,0,1,1])      
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes) 

        # self.figure.figimage(image)
        # self.axes = self.figure.add_subplot(111) # self.figure.add_axes([0,1,0,1]) #
        
        

        self.canvas = FigureCanvas(self, -1, self.figure)

        # Turn off the axes labels
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        # Initialise the rectangle
        self.rect = Rectangle((0,0), 1, 1, facecolor='None', edgecolor='green')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.axes.add_patch(self.rect)
        
        # Sizer to contain the widget
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP)# | wx.GROW)
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
    	
    	image = matplotlib.image.imread(pathToImage) # Load the image into matplotlib
        imPIL = Image.open(pathToImage) # Load the image using PIL to get it's dimensions
        imageSize = imPIL.size
        self.axes.imshow(image,aspect='equal') 
        self.canvas.draw()
        print imageSize



if __name__ == "__main__":
    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = RectangleSelectImagePanel(fr)
    panel.setImage('images/Lenna.png')
    # wx.CallLater(2000, panel.setImage, 'images/lena-bw.jpg')

    fr.Show()
    app.MainLoop()

    
