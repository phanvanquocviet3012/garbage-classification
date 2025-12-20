import streamlit as st
import requests
from PIL import Image
import io
import base64
import time
import textwrap
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="AI Garbage Classification",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'machine_open' not in st.session_state:
    st.session_state.machine_open = False

# --- HÀM HỖ TRỢ (ĐỌC FILE, NHẠC, NỀN) ---
def get_base64_of_bin_file(bin_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, bin_file)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except FileNotFoundError:
            return None

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    if bin_str:
        st.markdown(f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        ''', unsafe_allow_html=True)

def play_music(mp3_file):
    bin_str = get_base64_of_bin_file(mp3_file)
    if bin_str:
        st.markdown(f"""
            <style>
                #audio-container-wrapper {{
                    position: fixed;
                    bottom: 30px;
                    left: 50%;
                    transform: translateX(-50%);
                    z-index: 9999;
                    background: rgba(255, 255, 255, 0.3);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.5);
                    padding: 10px 25px;
                    border-radius: 30px;
                    text-align: center;
                    color: #333;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    transition: opacity 0.3s;
                }}
                #audio-container-wrapper:hover {{
                    opacity: 1;
                }}
            </style>
            <div id="audio-container-wrapper">
                <div style="font-weight: bold; margin-bottom: 8px; font-size: 18px;">
                    🎵 Nhạc nè ấn đi: 👇
                </div>
                <audio id="bg_audio" controls autoplay loop style="height: 35px; width: 250px; border-radius: 20px;">
                    <source src="data:audio/mp3;base64,{bin_str}" type="audio/mp3">
                </audio>
            </div>
            <script>
                var audio = document.getElementById("bg_audio");
                audio.volume = 0.5;
                var playPromise = audio.play();
                if (playPromise !== undefined) {{
                    playPromise.then(_ => {{}}).catch(error => {{
                        console.log("Autoplay blocked");
                    }});
                }}
            </script>
            """, unsafe_allow_html=True)

set_background('background.png')
play_music('nhacnen.mp3')

# --- CSS TÙY CHỈNH ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600;900&display=swap');
    html, body, [class*="css"] { font-family: 'Fredoka', sans-serif; }

    .title-box {
        background-color: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        width: fit-content;
        margin: 0 auto 20px auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        text-align: center;
    }

    .glass-container {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 30px;
        border: 2px solid rgba(255,255,255,0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        margin-top: 20px;
    }
    
    .shimmer-title {
        font-size: 60px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 30px rgba(146, 254, 157, 0.6);
        margin-bottom: 10px;
    }
    
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 20px;
    }

    .section-header {
        background: linear-gradient(90deg, #005AA7, #FFFDE4); 
        padding: 10px 30px; 
        border-radius: 50px; 
        color: white;
        font-size: 22px;
        font-weight: bold;
        text-shadow: 1px 1px 2px black;
        margin-bottom: 15px;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    div.stButton > button {
        border-radius: 50px !important; 
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-box">
        <div class="shimmer-title">✨ AI GARBAGE CLASSIFICATION ✨</div>
        <h4 style='text-align: center; color: #333; margin: 0; font-weight: 600;'>
            🌍 Chung tay bảo vệ hành tinh xanh 🌍
        </h4>
    </div>
""", unsafe_allow_html=True)

# --- MÀN HÌNH CHỜ (Máy chưa mở) ---
if not st.session_state.machine_open:
    st.markdown("""
    <style>
    div.stButton > button {
        background: linear-gradient(45deg, #00b09b, #96c93d) !important;
        color: white !important;
        height: auto !important;
        padding: 20px 0px !important;
    }
    div.stButton > button p {
        font-size: 35px !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    machine_base64 = get_base64_of_bin_file("machine.png")
    if machine_base64:
        st.markdown(f"""
            <div class="center-content">
                <h2 style='color: #333; margin-bottom: 15px; font-weight: bold;
                           background: rgba(255,255,255,0.3); backdrop-filter: blur(10px); 
                           border: 1px solid rgba(255,255,255,0.5);
                           padding: 10px 25px; border-radius: 30px; display: inline-block;'>
                    ⬇️ Kích hoạt hệ thống tại đây ⬇️
                </h2>
                <img src="data:image/png;base64,{machine_base64}" 
                     style="width: 650px; max-width: 90%; filter: drop-shadow(0 10px 10px rgba(0,0,0,0.5));">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Chưa có file machine.png")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("KHỞI ĐỘNG MÁY PHÂN LOẠI", use_container_width=True):
            st.session_state.machine_open = True
            st.rerun()

# --- MÀN HÌNH CHÍNH (Máy đã mở) ---
else:
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background: #ff4757; 
        color: white;
        height: auto;
        padding: 8px 30px;
        font-size: 16px;
        font-weight: bold;
    }
    div.stButton > button:last-child {
        background: linear-gradient(to right, #11998e, #38ef7d);
        color: white !important;
        padding: 15px 30px !important;
        text-transform: uppercase;
    }
    div.stButton > button:last-child p {
        font-size: 30px !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_back, col_rest = st.columns([1, 6])
    with col_back:
        if st.button("⬅️ Đóng máy"):
            st.session_state.machine_open = False
            st.rerun()

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="section-header">📥 Upload ảnh rác</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True, caption="Ảnh đã chọn")

    with col2:
        st.markdown('<div class="section-header">⚙️ Kết quả phân tích</div>', unsafe_allow_html=True)
        st.write("") 
        
        if uploaded_file:
            if st.button("⚡ QUÉT NGAY ⚡", use_container_width=True):
                with st.spinner('Máy đang phân tích dữ liệu...'):
                    time.sleep(1.5) 
                    
                    try:
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        files = {'file': ('image.png', img_byte_arr, 'image/png')}
                        
                        response = requests.post("http://127.0.0.1:5000/predict", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            label_raw = data['label'] # Lấy nhãn gốc từ backend
                            conf = data['confidence']
                        else:
                            st.error(f"Lỗi Server: {response.status_code}")
                            st.stop()
                            
                    except Exception as e:
                        # Fallback giả lập để test nếu không kết nối được backend
                        label_raw = "Plastic" 
                        conf = 99.99
                        st.error(f"Lỗi kết nối: {e}")

                    # --- XỬ LÝ KẾT QUẢ CHO 10 LOẠI ---
                    # Chuẩn hóa về chữ thường để so sánh
                    l = label_raw.lower().strip()

                    # Dictionary cấu hình hiển thị cho từng loại
                    garbage_info = {
                        "battery": {
                            "vn": "PIN (BATTERY)", 
                            "color": "#FF4500", # Đỏ cam
                            "icon": "🔋", 
                            "advice": "Rác thải nguy hại. Hãy thu gom riêng!"
                        },
                        "biological": {
                            "vn": "RÁC HỮU CƠ (BIOLOGICAL)", 
                            "color": "#32CD32", # Xanh lá
                            "icon": "🥬", 
                            "advice": "Có thể ủ làm phân bón."
                        },
                        "cardboard": {
                            "vn": "BÌA CARTON (CARDBOARD)", 
                            "color": "#8B4513", # Nâu
                            "icon": "📦", 
                            "advice": "Xếp gọn và tái chế."
                        },
                        "clothes": {
                            "vn": "QUẦN ÁO (CLOTHES)", 
                            "color": "#9370DB", # Tím
                            "icon": "👕", 
                            "advice": "Quyên góp nếu còn dùng được."
                        },
                        "glass": {
                            "vn": "THỦY TINH (GLASS)", 
                            "color": "#00CED1", # Xanh ngọc
                            "icon": "🥂", 
                            "advice": "Cẩn thận vỡ khi bỏ thùng."
                        },
                        "metal": {
                            "vn": "KIM LOẠI (METAL)", 
                            "color": "#708090", # Xám
                            "icon": "🔩", 
                            "advice": "Giá trị tái chế cao."
                        },
                        "paper": {
                            "vn": "GIẤY (PAPER)", 
                            "color": "#1E90FF", # Xanh dương
                            "icon": "📄", 
                            "advice": "Giữ khô ráo để tái chế."
                        },
                        "plastic": {
                            "vn": "NHỰA (PLASTIC)", 
                            "color": "#FFD700", # Vàng
                            "icon": "🥤", 
                            "advice": "Làm sạch trước khi tái chế."
                        },
                        "shoes": {
                            "vn": "GIÀY DÉP (SHOES)", 
                            "color": "#FF69B4", # Hồng
                            "icon": "👟", 
                            "advice": "Quyên góp hoặc bỏ thùng rác thải."
                        },
                        "trash": {
                            "vn": "RÁC THẢI KHÁC (TRASH)", 
                            "color": "#696969", # Xám đậm
                            "icon": "🗑️", 
                            "advice": "Bỏ vào thùng rác chung."
                        }
                    }

                    # Tìm kiếm thông tin trong dictionary
                    # Mặc định nếu không tìm thấy
                    result = {
                        "vn": label_raw.upper(),
                        "color": "#333333",
                        "icon": "❓",
                        "advice": "Không xác định được loại rác."
                    }

                    # Quét qua các key để tìm
                    for key, info in garbage_info.items():
                        if key in l:
                            result = info
                            break

                    st.balloons()
                    
                    html_content = textwrap.dedent(f"""
                        <div style="background: white; border-radius: 20px; padding: 20px; border: 4px solid {result['color']}; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                            <div style="font-size: 60px;">{result['icon']}</div>
                            <h2 style="color: #444; margin:0; font-size: 20px;">AI KẾT LUẬN:</h2>
                            <h1 style="color: {result['color']}; font-size: 35px; margin: 10px 0; font-weight: 900;">{result['vn']}</h1>
                            <div style="background: #eee; height: 20px; border-radius: 10px; margin: 15px 0;">
                                <div style="width: {conf}%; background: {result['color']}; height: 100%; border-radius: 10px;"></div>
                            </div>
                            <p style="color: #333; font-size: 18px; margin-bottom: 5px;">
                                Độ tin cậy: <b style="color: {result['color']};">{conf}%</b>
                            </p>
                            <hr style="margin: 10px 0;">
                            <p style="color: #333; font-size: 18px;">💡 <i>{result['advice']}</i></p>
                        </div>
                    """)
                    
                    st.markdown(html_content, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="
                    background-color: rgba(255, 255, 255, 0.9);
                    border: 3px solid #ff4757;
                    border-radius: 20px;
                    padding: 30px;
                    text-align: center;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                    margin-top: 20px;
                ">
                    <h2 style="color: #ff4757; margin: 0; font-weight: 900; font-size: 30px;">⚠️ CHƯA CÓ ẢNH!</h2>
                    <p style="color: #333; font-size: 20px; font-weight: bold; margin-top: 15px;">
                        👈 Vui lòng chọn ảnh rác bên cột trái trước khi quét.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)