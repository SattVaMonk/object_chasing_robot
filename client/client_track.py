import numpy as np
import argparse
import imutils
import dlib
import cv2
import time
import piCar as pc

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", type = str, default="http://192.168.43.58",
	help="url of the stream we want to capture")
ap.add_argument("-l", "--label", required=True,
	help="class label we are interested in detecting + tracking")
ap.add_argument("-t", "--track", type = int, default=1,
	help="set to false if we don't need to control the PiCar")
ap.add_argument("-c", "--confidence", type=float, default=0.8,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

streamUrl = args["url"] + ":8080/?action=stream"
controlUrl = args["url"]+ ':8000/'

connect = False
print("[INFO] Connecting to PiCar...")
for i in range(10):
	connect = pc.connection_ok(controlUrl)
	if connect:
		print("[INFO] Connection established with the url: ", args["url"])
		break

if not connect:
	print("[INFO] Failed to build connection with the url: ", args["url"], " , please make sure your PiCar is connecting to the same network with this IP")
	exit()

# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

prototxt = "object_detection/data/MobileNetSSD_deploy.prototxt"
model = "object_detection/data/MobileNetSSD_deploy.caffemodel"
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# initialize the video stream, dlib correlation tracker, output video
# writer, and predicted class label
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(streamUrl)
print(vs.get(cv2.CAP_PROP_FRAME_WIDTH),vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
tracker = None
label = ""

if args["track"]:
	# Initializing the PiCar...
	pc.run_action('fwready')
	pc.run_action('bwready')
	pc.run_action('camready')
	pc.run_speed(30)
	pc.run_action('forward')

try:
	# loop over frames from the video file stream
	while True:
		# cur_time = time.perf_counter()
		# grab the next frame from the video file
		(grabbed, frame) = vs.read()
		# print("[Perf]time consuming for reading frame: ", time.perf_counter() - cur_time)
		# cur_time = time.perf_counter()

		# check to see if the stream ends
		if frame is None:
			break

		# resize the frame for faster processing and then convert the
		# frame from BGR to RGB ordering (dlib needs RGB ordering)
		frame = imutils.resize(frame, width=600)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# print("[Perf]time consuming for resizing frame: ", time.perf_counter() - cur_time)
		# cur_time = time.perf_counter()

		# if our correlation object tracker is None we first need to
		# apply an object detector to seed the tracker with something
		# to actually track
		if tracker is None:
			# grab the frame dimensions and convert the frame to a blob
			(h, w) = frame.shape[:2]
			blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)

			# pass the blob through the network and obtain the detections
			# and predictions
			net.setInput(blob)
			detections = net.forward()
			# print("[Perf]time consuming for object detection: ", time.perf_counter() - cur_time)
			# cur_time = time.perf_counter()

			# ensure at least one detection is made
			if len(detections) > 0:
				# find the index of the detection with the largest
				# probability -- out of convenience we are only going
				# to track the first object we find with the largest
				# probability; future examples will demonstrate how to
				# detect and extract *specific* objects
				i = np.argmax(detections[0, 0, :, 2])

				# grab the probability associated with the object along
				# with its class label
				conf = detections[0, 0, i, 2]
				label = CLASSES[int(detections[0, 0, i, 1])]

				# filter out weak detections by requiring a minimum
				# confidence
				if conf > args["confidence"] and label == args["label"]:
					if args["track"]:
						#boost the PiCar to chase the duck
						pc.run_speed(60)
					# compute the (x, y)-coordinates of the bounding box
					# for the object
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")

					# construct a dlib rectangle object from the bounding
					# box coordinates and then start the dlib correlation
					# tracker
					tracker = dlib.correlation_tracker()
					rect = dlib.rectangle(startX, startY, endX, endY)
					tracker.start_track(rgb, rect)

					# draw the bounding box and text for the object
					# cv2.rectangle(frame, (startX, startY), (endX, endY),
					# 	(0, 255, 0), 2)
					# cv2.putText(frame, label, (startX, startY - 15),
					# 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
					# print("[Perf]time consuming for tracking: ", time.perf_counter() - cur_time)
					# cur_time = time.perf_counter()

		# otherwise, we've already performed detection so let's track
		# the object
		else:
			# update the tracker and grab the position of the tracked
			# object
			tracker.update(rgb)
			pos = tracker.get_position()
			# print("[Perf]time consuming for tracking: ", time.perf_counter() - cur_time)
			# cur_time = time.perf_counter()

			# unpack the position object
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())

			center = [(startX+endX)/2 , (startY+endY)/2]

			# if the target is missing then clear the tracker and 
			# restart detection
			if(center[0] < 50 or center[0] > w - 50 or center[1] < 50 or center[1] > h - 50):
				tracker = None
				#slow down when lose target
				if args["track"]:
					pc.run_speed(20)
			else:
				# draw the bounding box from the correlation object tracker
				# cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
				# cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
				if args["track"]:
					# turning the wheel towards the object to complete chasing
					if(center[0]< w/2 - 10):
						print('[Action] Left')
						pc.run_action('fwturn:75')
						time.sleep(.100)
						pc.run_action('fwturn:90')
					elif(center[0]> w/2 + 10):
						print('[Action] Left')
						pc.run_action('fwturn:105')
						time.sleep(.100)
						pc.run_action('fwturn:90')
			# print("[Perf]time consuming for car controling: ", time.perf_counter() - cur_time)
			# cur_time = time.perf_counter()
		# show the output frame
		cv2.imshow("Frame", frame)
		cv2.waitKey(1)
		# print("[Perf]time consuming for show image: ", time.perf_counter() - cur_time)

except KeyboardInterrupt:
    pass

# do a bit of cleanup
cv2.destroyAllWindows()
if args["track"]:
	pc.run_action('stop')
vs.release()