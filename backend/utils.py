import numpy as np
from PIL import Image, ImageOps  # <--- Nhớ thêm ImageOps ở đây

def load_labels(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().split(' ', 1)[-1] for line in f.readlines()]

def preprocess_image(image, target_size=(224, 224)):
    # 1. Đảm bảo ảnh là chuẩn màu RGB
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    image = ImageOps.fit(image, target_size, Image.Resampling.LANCZOS)
    
    # 3. Chuyển sang mảng số thực (float32)
    img_array = np.asarray(image).astype(np.float32)
    
    normalized_array = (img_array / 127.5) - 1
    
    return np.expand_dims(normalized_array, axis=0)