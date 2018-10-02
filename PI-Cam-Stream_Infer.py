#!/usr/bin/python3
# Python script to start a PI camera and feed frames to
# the Movidius Neural Compute Stick that is loaded with a
# CNN graph file and report the inferred results
# show two displays on the PI one showing realtime with
# inf result, the other showing the preprocessed image to
# demonstrate what the NN sees

import mvnc.mvncapi as fx
from timeit import default_timer as timer

import threading
import time
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from queue import Queue
from threading import Thread

import scipy.misc
import picamera #import PiCamera
from picamera.array import PiRGBArray
import cv2


camera = picamera.PiCamera()
camera.resolution=(480,480)
camera.iso=200
camera.brightness=55
camera.framerate= 10
camera.meter_mode='spot'
camera.exposure_mode='nightpreview'
rawCapture=PiRGBArray(camera, size=(227,227))
time.sleep(2)
global counter
counter = 0

import numpy

#please don't change the image size since those sizes are required by each network

'''
NETWORK_IMAGE_WIDTH = 227       # the width of images the network requires
NETWORK_IMAGE_HEIGHT = 227      # the height of images the network requires
NETWORK_IMAGE_FORMAT = "BGR"    # the format of the images the network requires
NETWORK_DIRECTORY = "../../networks/Gender/" # directory of the network this directory needs to
                                # have 3 files: "graph", "stat.txt" and "categories.txtNETWORK_IMAGE_WIDTH = 224           # the width of images the network requires

NETWORK_IMAGE_WIDTH = 224          # the width of images the network requires
NETWORK_IMAGE_HEIGHT = 224          # the height of images the network requires
NETWORK_IMAGE_FORMAT = "BGR"        # the format of the images the network requires
NETWORK_DIRECTORY = "../../networks/GoogLeNet/"  # directory of the network this directory needs to
 
'''
EXAMPLES_BASE_DIR= '../../'                                   # have 3 files: "graph", "stat.txt" and "categories.txt"

NETWORK_IMAGE_WIDTH = 227           # the width of images the network requires
NETWORK_IMAGE_HEIGHT = 227          # the height of images the network requires
NETWORK_IMAGE_FORMAT = "BGR"        # the format of the images the network requires
NETWORK_DIRECTORY = "../../caffe/SqueezeNet/" # directory of the network this directory needs to
                                    # have 3 files: "graph", "stat.txt" and "categories.txt"
'''

NETWORK_IMAGE_WIDTH = 227          # the width of images the network requires
NETWORK_IMAGE_HEIGHT = 227          # the height of images the network requires
NETWORK_IMAGE_FORMAT = "BGR"        # the format of the images the network requires
NETWORK_DIRECTORY = "../../networks/AlexNet/"    # directory of the network this directory needs to
                                    # have 3 files: "graph", "stat.txt" and "categories.txt
'''

# Globals for the program

gIt = None
gRunning = False
gOt = None
gNetworkMean = None
gNetworkStd = None
gNetworkCategories = None
gUpdateq = Queue()
gGraph = None
gCallback = None

# end of globals for the program

# Start the input and output worker threads for the application
def start_thread():
    """ start threads and idle handler (update_ui) for callback dispatching
    """
    global gIt, gOt, gRunning
    gRunning = True
    gIt = Thread(target = input_thread)
    gIt.start()
    gOt = Thread(target = output_thread)
    gOt.start()


#Stop worker threads for the application.  Blocks until threads are terminated
def stop_thread():
    """ stop threads
    """
    
    global gIt, gOt, gRunning

    # Set gRunning flag to false so worker threads know to terminate
    gRunning = False;

    # Wait for worker threads to terminate.
    gIt.join()
    gOt.join()


# Worker thread function for input to MVNC.
# Gets a preprocessed camera sample and calls the MVNC API to do an inference on the image.
def input_thread():
    """ input thread function
    """
    global gRunning
    frame_number = 0
    while gRunning:
        preprocessed_image_buf = get_sample()
        if preprocessed_image_buf is not None:   # TODO: eliminate busy looping before samples are available
            #print("loading %s : %s" % (preprocessed_image_buf.shape, preprocessed_image_buf ))
            gGraph.LoadTensor(preprocessed_image_buf ,"frame %s" % frame_number)
            frame_number=frame_number + 1
        else:
            print('none')
        #time.sleep(0.05)
    print("Input thread terminating.")

	
# Worker thread function to handle inference results from the MVNC stick
def output_thread():
  """ output thread function
  for getting inference results from Movidius NCS
  running graph specific post processing of inference result
  queuing the results for main thread callbacks
  """
  global gRunning

  try:
    while gRunning:
      try:
        inference_result, user_data = gGraph.GetResult()
        
        print (postprocess(inference_result))
        #print(user_data)
       # gUpdateq.put((postprocess(inference_result), user_data))

       
      except KeyError:
        # This error occurs when GetResult can't access the user param from the graph, we're just ignoring it for now
        print("KeyError")
        pass
  except Exception as e:
    print(e)
    pass
  print("Output thread terminating")
  

# Get a sample from the camera and preprocess it so that its ready for
# to be sent to the MVNC stick to run an inference on it.
def get_sample():
    """ get a preprocessed frame to be pushed to the graph
    """
    global counter
    counter = counter + 1 
   
    # capture frames from the camera;
   
    frame=picamera.array.PiRGBArray(camera)
    camera.capture(frame, 'bgr', use_video_port=True)
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    preprocessed_image_buffer=preprocess(image)
	# show the frame
    cv2.imshow("Frame0", image)
    key = cv2.waitKey(1) & 0xFF
    return preprocessed_image_buffer


# Read the graph file for the network from the filesystem.
def get_graph_from_disk():
    """
    :return: the bytes that were read from disk which are the binary graph file contents
    """

    with open(NETWORK_DIRECTORY + "graph", mode='rb') as file:
        graph_blob = file.read()
    return graph_blob


# preprocess the camera images to create images that are suitable for the
# network.  Specifically resize to appropriate height and width
# and make sure the image format is correct.  This is called by the input worker
# thread function prior to passing the image the MVNC API.
def preprocess(img):
    """ preprocess a video frame
    input - in the format specified by rawinputformat() method
    output - in the format required by the graph
    """
    dim=(227,227)
    resize_width = 224
    resize_height = 224

    img=cv2.resize(img,dim)
    #img=cv2.normalize(img,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)
    img = img.astype(numpy.float32)

    #Preprocess image changing the RGB pixel values to	             the values the network needs
    # to do this we subtract the mean and multiply the std for each channel (R, G and B)
    # these mean and std values come from the stat.txt file that must accompany the
    # graph file for the network.
   
    img[:,:,0] = (img[:,:,0] - gNetworkMean[0])
    img[:,:,1] = (img[:,:,1] - gNetworkMean[1])
    img[:,:,2] = (img[:,:,2] - gNetworkMean[2])
   

    # Finally we return the values as Float16 rather than Float32 as that is what the network expects.
    cv2.imshow("Frame", img)
    return img.astype('float16') #age_float_array.astype(numpy.float16)

 
# post process the results from MVNC API to create a human
# readable string.
def postprocess(output):
    """ postprocess an inference result
    input - in the format produced by the graph
    output - in a human readable format
    """
    text=''
    order = output.argsort()[::-1][:6]
   # print('\n------- predictions --------')
    for i in range(1):
       # print ('prediction ' + str(i) + ' (probability ' + str(output[order[i]]*100) + '%) is ' + gNetworkCategories[order[i]] + '  label index is: ' + str(order[i]) )
        text=text+str(gNetworkCategories[order[i]])

    return text

def fps():
    threading.Timer(2.0, fps).start()
    global counter
    print('FPS: %.2f fps' % (counter/2.0))
    counter = 0
   
# main entry point for the program
if __name__=="__main__":
   
    fps()

    # Load preprocessing data for network
    gNetworkMean=numpy.load(EXAMPLES_BASE_DIR+'data/ilsvrc12/ilsvrc_2012_mean.npy').mean(1).mean(1) #loading the mean file
    gNetworkStd=numpy.load(EXAMPLES_BASE_DIR+'data/ilsvrc12/ilsvrc_2012_mean.npy').std(1)
    
   
    # Load categories from categories.txt
    gNetworkCategories = []
    labels_file=EXAMPLES_BASE_DIR+'data/ilsvrc12/synset_words.txt'
    gNetworkCategories=numpy.loadtxt(labels_file,str,delimiter='\t')
    
    fx.SetGlobalOption(fx.GlobalOption.LOG_LEVEL, 2)

    # For this program we will always use the first MVNC device.
    ncs_names = fx.EnumerateDevices()
    if (len(ncs_names) < 1):
        print("Error - No NCS devices detected. Make sure your device is connected.")
        quit()
  # Initialize the MVNC device

    dev = fx.Device(ncs_names[0])
    dev.OpenDevice()
    gGraph = dev.AllocateGraph(get_graph_from_disk())

    # Initialize input and output threads to pass images to the
    # MVNC device and to read results from the inferences made on thos images.

    start_thread()

