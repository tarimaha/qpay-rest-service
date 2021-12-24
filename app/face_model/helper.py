import cv2
import os
import argparse
import os
import face_recognition
import sys
import pickle
from imutils import paths
import numpy as np

basedir = os.path.abspath(os.path.dirname(__file__))


DETECTION_METHOD = 'hog'
SAVED_ENCODINGS = os.path.join(basedir, "saved_encodings.pickle")
TOLERANCE = 0.4

if not os.path.exists(SAVED_ENCODINGS):
    with open(SAVED_ENCODINGS, 'w'): pass

def create_embeddings(name, dataset_path):
	if os.path.getsize(SAVED_ENCODINGS) != 0:
		# initialize the list of known encodings and known names
		f = open(SAVED_ENCODINGS, "rb") #fileObject
		b = pickle.load(f)
		# initialize knownEncodings and knownNames
		knownEncodings = b['encodings']
		knownNames = b['names']
		f.close()
	else:
		knownEncodings = []
		knownNames = []
	dirname = [f.path for f in os.scandir(dataset_path) if f.is_dir() and f.name == name][0]

	# grab the paths to the input images in our dataset for the specific user
	print(f"[INFO] quantifying faces for {dirname}...")
	imagePaths = list(paths.list_images(dirname))
	for (i, imagePath) in enumerate(imagePaths):
		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model=DETECTION_METHOD)
		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)
		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)
		# dump the facial encodings + names to disk
		print("[INFO] serializing encodings...")
		data = {"encodings": knownEncodings, "names": knownNames}
		f = open(SAVED_ENCODINGS, "wb")
		f.write(pickle.dumps(data))
		f.close()
		print('[INFO] Completed extracting embeddings')


def recognize_image(file_stream):
	data = pickle.loads(open(SAVED_ENCODINGS, "rb").read())
	# Load the uploaded image file
	img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
	unknown_encodings = face_recognition.face_encodings(img)
	names = []
	if unknown_encodings:
		# compute the facial embeddings for each face bounding box
		# encodings = face_recognition.face_encodings(rgb, boxes)
		for encoding in unknown_encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding, TOLERANCE)
			name = "Unknown"
			# Use the known face with the smallest distance to the new face
			face_distances = face_recognition.face_distance(data["encodings"], encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = data["names"][best_match_index]
				# best_match_distance = face_distances[best_match_index]
				# best_match_similarity_percentage = f'{((1/(1 + best_match_distance))*100):0.1f}%'
				# name = (name, best_match_similarity_percentage)
			names.append(name)
	else:
		names.append("No faces detected")
	return names
