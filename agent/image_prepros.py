import numpy as np
import cv2
import pickle

class ImageClassifier:
    def __init__(self, session, label_mapping_file):
        """
        Initialize the image classifier with an ONNX session and label mapping file.
        """
        self.session = session
        self.input_name = session.get_inputs()[0].name
        self.output_name = session.get_outputs()[0].name
        
        # Load the label mapping
        with open(label_mapping_file, "rb") as f:
            self.label_mapping = pickle.load(f)
            
        print(f"Input Name: {self.input_name}, Output Name: {self.output_name}")

    def preprocess_image(self, image_path):
        """
        Preprocess an input image for ONNX model inference.
        - Resizes the image to 224x224
        - Normalizes pixel values
        - Converts to a numpy array of shape (1, 3, 224, 224)
        """
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        image = cv2.resize(image, (224, 224))  # Resize to 224x224
        image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
        # Convert to shape (1, 3, 224, 224) as ONNX expects (batch_size, channels, height, width)
        image = np.transpose(image, (2, 0, 1))  # Convert to (C, H, W)
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        return image

    def classify_image(self, image_path):
        """
        Perform inference on an image using the ONNX model.
        """
        # Preprocess the input image
        input_data = self.preprocess_image(image_path)
        
        # Perform inference
        outputs = self.session.run([self.output_name], {self.input_name: input_data})
        
        # Get the predicted class
        predicted_class_index = np.argmax(outputs[0])  # Get index of the highest probability
        predicted_class = [k for k, v in self.label_mapping.items() if v == predicted_class_index][0]
        
        return predicted_class
