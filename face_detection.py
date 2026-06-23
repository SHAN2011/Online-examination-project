import numpy as np
import h5py
from PIL import Image
import base64
import io

# Exam monitoring status labels
EXAM_STATUS = {
    'face_present': 'Normal',
    'no_face': 'Cheating',
    'error': 'Error'
}

class FaceDetector:
    def __init__(self, model_path='model.h5'):
        self.weights = self._load_weights(model_path)
        self.input_size = (64, 64)
        
    def _load_weights(self, path):
        f = h5py.File(path, 'r')
        weights = {}
        
        # Load conv layers
        for layer_name in ['conv2d_1', 'conv2d_2', 'conv2d_3', 'conv2d_4']:
            w = f[layer_name][layer_name]['kernel:0'][:]
            b = f[layer_name][layer_name]['bias:0'][:]
            weights[f'{layer_name}_w'] = w
            weights[f'{layer_name}_b'] = b
            
        # Load dense layers
        for layer_name in ['dense_1', 'dense_2']:
            w = f[layer_name][layer_name]['kernel:0'][:]
            b = f[layer_name][layer_name]['bias:0'][:]
            weights[f'{layer_name}_w'] = w
            weights[f'{layer_name}_b'] = b
            
        f.close()
        return weights
    
    def _conv2d(self, x, w, b):
        kh, kw, ic, oc = w.shape
        ih, iw = x.shape[0], x.shape[1]
        oh, ow = ih - kh + 1, iw - kw + 1
        out = np.zeros((oh, ow, oc))
        for c in range(oc):
            for i in range(oh):
                for j in range(ow):
                    patch = x[i:i+kh, j:j+kw, :]
                    out[i, j, c] = np.sum(patch * w[:, :, :, c]) + b[c]
        return out
    
    def _max_pool2d(self, x, pool_size=2):
        h, w, c = x.shape
        oh, ow = h // pool_size, w // pool_size
        out = np.zeros((oh, ow, c))
        for i in range(oh):
            for j in range(ow):
                for k in range(c):
                    out[i, j, k] = np.max(x[i*pool_size:(i+1)*pool_size, j*pool_size:(j+1)*pool_size, k])
        return out
    
    def _relu(self, x):
        return np.maximum(0, x)
    
    def _dense(self, x, w, b):
        return np.dot(x, w) + b
    
    def _softmax(self, x):
        e = np.exp(x - np.max(x))
        return e / e.sum()
    
    def predict(self, image_array):
        """Run inference on a preprocessed image array (64x64x1, values 0-1)"""
        x = image_array
        
        # conv2d_1 -> relu -> max_pool
        x = self._conv2d(x, self.weights['conv2d_1_w'], self.weights['conv2d_1_b'])
        x = self._relu(x)
        x = self._max_pool2d(x)
        
        # conv2d_2 -> relu -> max_pool
        x = self._conv2d(x, self.weights['conv2d_2_w'], self.weights['conv2d_2_b'])
        x = self._relu(x)
        x = self._max_pool2d(x)
        
        # conv2d_3 -> relu -> max_pool
        x = self._conv2d(x, self.weights['conv2d_3_w'], self.weights['conv2d_3_b'])
        x = self._relu(x)
        x = self._max_pool2d(x)
        
        # conv2d_4 -> relu
        x = self._conv2d(x, self.weights['conv2d_4_w'], self.weights['conv2d_4_b'])
        x = self._relu(x)
        
        # flatten
        x = x.flatten()
        
        # dense_1 -> relu
        x = self._dense(x, self.weights['dense_1_w'], self.weights['dense_1_b'])
        x = self._relu(x)
        
        # dense_2 -> softmax
        x = self._dense(x, self.weights['dense_2_w'], self.weights['dense_2_b'])
        x = self._softmax(x)
        
        return x
    
    def preprocess_frame(self, base64_image):
        """Convert base64 image to model input format"""
        # Decode base64
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Resize to 64x64
        image = image.resize(self.input_size)
        
        # Convert to numpy array and normalize
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = img_array.reshape(64, 64, 1)
        
        return img_array
    
    def detect_face(self, base64_image):
        """
        Detect face from camera frame for exam monitoring.
        Returns dict with exam monitoring status only.
        """
        try:
            img_array = self.preprocess_frame(base64_image)
            predictions = self.predict(img_array)
            
            max_idx = np.argmax(predictions)
            max_confidence = float(predictions[max_idx])
            
            # Threshold for face detection
            # If confidence is high enough, we consider a face is detected
            face_detected = max_confidence > 0.4
            
            monitoring_status = EXAM_STATUS['face_present'] if face_detected else EXAM_STATUS['no_face']
            
            return {
                'face_detected': face_detected,
                'confidence': max_confidence,
                'monitoring_status': monitoring_status
            }
        except Exception as e:
            return {
                'face_detected': False,
                'monitoring_status': EXAM_STATUS['error'],
                'error': str(e)
            }

# Singleton instance
face_detector = None

def get_face_detector():
    global face_detector
    if face_detector is None:
        face_detector = FaceDetector()
    return face_detector

