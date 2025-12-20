from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf  # Sử dụng TensorFlow đầy đủ
from PIL import Image
import io
import numpy as np
from utils import load_labels, preprocess_image

app = Flask(__name__)
CORS(app)

# 1. Khởi tạo TFLite Interpreter thông qua tf.lite
# Việc sử dụng tf.lite.Interpreter giúp tránh các lỗi về lớp custom trong file .h5
try:
    interpreter = tf.lite.Interpreter(model_path="models/model_unquant.tflite")
    interpreter.allocate_tensors()

    # Lấy thông tin chi tiết về đầu vào và đầu ra của mô hình
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Load danh sách nhãn từ file utils
    LABELS = load_labels('models/labels.txt')
    print("Backend: Model TFLite và Labels đã được tải thành công.")
except Exception as e:
    print(f"Lỗi nghiêm trọng khi khởi tạo Model: {e}")

@app.route("/predict", methods=["POST"])
def predict():
    # Kiểm tra xem có file trong request không
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file ảnh trong yêu cầu"}), 400
    
    try:
        file = request.files['file']
        # Đọc ảnh và chuyển sang định dạng RGB
        img = Image.open(io.BytesIO(file.read()))
        
        # 2. Tiền xử lý ảnh (sử dụng hàm từ utils.py)
        # Hàm này sẽ resize về 224x224 và chuẩn hóa về [-1, 1]
        input_data = preprocess_image(img)
        
        # 3. Chạy dự đoán với TFLite Interpreter
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        
        # 4. Thu thập kết quả đầu ra
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        # Lấy chỉ số có xác suất cao nhất
        index = np.argmax(output_data[0])
        confidence = float(output_data[0][index])
        
        # Trả về kết quả JSON cho Frontend (Streamlit)
        return jsonify({
            "label": LABELS[index],
            "confidence": round(confidence * 100, 2), # Chuyển sang đơn vị %
            "status": "success"
        })
        
    except Exception as e:
        print(f"Lỗi trong quá trình dự đoán: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Chạy Flask Server tại port 5000
    # host="0.0.0.0" cho phép các thiết bị khác trong mạng LAN truy cập nếu cần
    app.run(host="0.0.0.0", port=5000, debug=True)