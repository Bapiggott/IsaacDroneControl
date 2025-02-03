from flask import Flask, request, jsonify, send_from_directory, render_template_string
import cv2
import numpy as np
import torch
import io
import os
import json
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
from collections import deque
import threading
import time


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DEPTH_OUTPUT_FOLDER = 'depth_outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEPTH_OUTPUT_FOLDER'] = DEPTH_OUTPUT_FOLDER

N = 5
latest_detections = deque(maxlen=N)
detections_lock = threading.Lock()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s').to(device)

#model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5x')
#depth_model_name = "depth-anything/Depth-Anything-V2-Small-hf"
depth_model_name = "depth-anything/Depth-Anything-V2-Small-hf"
depth_image_processor = AutoImageProcessor.from_pretrained(depth_model_name)
depth_model = AutoModelForDepthEstimation.from_pretrained(depth_model_name).to(device)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DEPTH_OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    HTML_TEMPLATE = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>YOLO and Depth Estimation Server</title>
        <script>
            function refreshImage() {
                var timestamp = new Date().getTime();
                document.getElementById('latest-image').src = '/image/latest?' + timestamp;
                document.getElementById('depth-image').src = '/depth_image/latest?' + timestamp;
            }
            setInterval(refreshImage, 5000);
        </script>
    </head>
    <body>
        <h1>YOLO and Depth Estimation Server</h1>
        <form action="/detect" method="post" enctype="multipart/form-data">
            <input type="file" name="image" required>
            <input type="submit" value="Upload Image">
        </form>
        <h2>Latest Processed Images:</h2>
        <div style="display: flex;">
            <div>
                <h3>Original Image</h3>
                <img id="latest-image" src="/image/latest" alt="Latest Image" style="max-width: 100%;">
            </div>
            <div>
                <h3>Depth Image</h3>
                <img id="depth-image" src="/depth_image/latest" alt="Depth Image" style="max-width: 100%;">
            </div>
        </div>
        <h3>Processing Times (ms):</h3>
        <p>YOLO Detection: {{ yolo_time }} ms</p>
        <p>Depth Estimation: {{ depth_time }} ms</p>
        <p>Total Time: {{ total_time }} ms</p>
    </body>
    </html>
    '''
    return render_template_string(HTML_TEMPLATE, yolo_time=0, depth_time=0, total_time=0)

@app.route('/detect', methods=['POST'])
def run_yolo():
    try:
        if 'image' not in request.files:
            return 'No file part', 400

        file = request.files['image']
        if file.filename == '':
            return 'No selected file', 400

            # Process the image
        img_bytes = file.read()
        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        print("*" * 8)
        # Move the image to GPU if available
        #img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(
        #    device)  # Convert to tensor and add batch dim

        start_time = time.time()
        print("1")
        results = model_yolo(img)#_tensor)  # Run inference
        yolo_time = (time.time() - start_time) * 1000
        print("2")
        # Convert detections to dictionary format
        detections = results.pandas().xyxy[0].to_dict(orient="records")
        print("3")
        # Save image and detections
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        image_filename = f"{timestamp}_{file.filename}"
        image_path = os.path.join("uploads", image_filename)
        with open(image_path, 'wb') as f:
            f.write(img_bytes)
        print("4")
        detection_data = {
            "timestamp": timestamp,
            "detections": detections
        }
        print("5")
        with detections_lock:
            latest_detections.append(detection_data)
        print("6")
        depth_time = run_depth_estimation(image_path, image_filename)
        print("7")
        total_time = (time.time() - start_time) * 1000
        return render_template_string(HTML_TEMPLATE, yolo_time=yolo_time, depth_time=depth_time, total_time=total_time)

    except Exception as e:
        return str(e), 400

def run_depth_estimation(image_path, original_filename):
    try:
        print('a')
        start_time = time.time()
        #print(f"image_path: {image_path}")
        from PIL import Image
        print('b')
        image = Image.open(image_path)
        print('')
        inputs = depth_image_processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = depth_model(**inputs)
            predicted_depth = outputs.predicted_depth

        print('c')
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        ).cpu()
        # Convert the depth map to a multi-dimensional numpy array
        print('d')
        depth_array = prediction.squeeze().numpy()

        # Continue with depth processing as before...
        # Convert to depth_with_coordinates array, save depth map, etc.

        # Create an array of [x, y, depth] for each pixel
        import numpy as np

        # Assuming depth_array is defined as your 2D depth map

        print('e')
        height, width = depth_array.shape

        # Vectorized way to create [x, y, depth] array
        x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
        depth_with_coordinates = np.stack([x_coords.ravel(), y_coords.ravel(), depth_array.ravel()], axis=1)

        # Save the array to a .txt file in human-readable form
        np.savetxt("depth_with_coordinates.txt", depth_with_coordinates, fmt='%.4f')

        # Optionally, save it to a .npy file for faster reloading
        np.save("depth_with_coordinates.npy", depth_with_coordinates)

        # Visualize the depth map and save it as an image (optional)
        print('f')
        formatted = (depth_array * 255 / np.max(depth_array)).astype("uint8")
        depth_image = Image.fromarray(formatted)
        depth_image.save("depth_estimation_output.png")

        # Optionally, print the shape of the array
        print("Depth array with coordinates shape:", depth_with_coordinates.shape)

        """depth_array = prediction.squeeze().cpu().numpy()
        depth_output_filename = f"depth_{original_filename}"
        depth_output_path = os.path.join(app.config['DEPTH_OUTPUT_FOLDER'], depth_output_filename)
        
        formatted = (depth_array * 255 / np.max(depth_array)).astype("uint8")
        depth_image = Image.fromarray(formatted)
        depth_image.save(depth_output_path)"""

        return (time.time() - start_time) * 1000

    except Exception as e:
        print(f"Depth estimation failed: {e}")
        return 0

@app.route('/detections/latest', methods=['GET'])
def get_latest_detection():
    with detections_lock:
        if latest_detections:
            latest_detection = latest_detections[-1]
            return jsonify(latest_detection)
        else:
            return jsonify([]), 404

@app.route('/image/latest')
def latest_image():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
        return send_from_directory(app.config['UPLOAD_FOLDER'], latest_file)
    return '', 404

"""@app.route('/depth_image/latest')
def latest_depth_image():
    files = os.listdir(app.config['DEPTH_OUTPUT_FOLDER'])
    if files:
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(app.config['DEPTH_OUTPUT_FOLDER'], x)))
        return send_from_directory(app.config['DEPTH_OUTPUT_FOLDER'], latest_file)
    return '', 404"""
@app.route('/depth_image/latest')
def latest_depth_image():
    files = os.listdir(app.config['DEPTH_OUTPUT_FOLDER'])
    if files:
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(app.config['DEPTH_OUTPUT_FOLDER'], x)))
        return send_from_directory(app.config['DEPTH_OUTPUT_FOLDER'], latest_file)
    return '', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

