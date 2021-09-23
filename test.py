import cv2 as cv
import numpy as np
import time


SOURCE_WINDOW_NAME = 'Fortnite  '
source_hwd = win32gui.FindWindow(None, SOURCE_WINDOW_NAME)


classes = open('model.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

net = cv.dnn.readNetFromDarknet('yolov5.cfg', 'yolov5_640.pt')
# net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

while True:
  window_rect = win32gui.GetWindowPlacement(source_hwd)[4]
  image = cv2.cvtColor(np.array(ImageGrab.grab(window_rect)), cv2.COLOR_BGR2RGB)
  blob = cv.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
  r = blob[0, 0, :, :]

  cv.imshow('blob', r)

  net.setInput(blob)
  t0 = time.time()
  outputs = net.forward(ln)
  t = time.time()
  print('time=', t-t0)

  for out in outputs:
      print(out.shape)

  boxes = []
  confidences = []
  classIDs = []
  h, w = img.shape[:2]

  for output in outputs:
      for detection in output:
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > 0.8:
            box = detection[:4] * np.array([w, h, w, h])
            (centerX, centerY, width, height) = box.astype("int")
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
            box = [x, y, int(width), int(height)]
            boxes.append(box)
            confidences.append(float(confidence))
            classIDs.append(classID)

  indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
  if len(indices) > 0:
      for i in indices.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        color = [int(c) for c in colors[classIDs[i]]]
        cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
        cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

  cv.imshow('window', img)
  cv.waitKey(0)
  cv.destroyAllWindows()
