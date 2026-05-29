import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
import io
from datetime import datetime
from math import ceil

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="CSC Photo Maker Pro",
    page_icon="📸",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #f1f5f9, #ffffff);
}

.title {
    font-size: 42px;
    font-weight: bold;
    color: #0f172a;
}

.subtitle {
    font-size: 18px;
    color: #475569;
}

.box {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<p class="title">📸 CSC Photo Maker Pro</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Professional Passport Photo Creator</p>',
    unsafe_allow_html=True
)

st.write("")

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:

    st.header("⚙️ Photo Controls")

    uploaded_file = st.file_uploader(
        "Upload Photo",
        type=["jpg", "jpeg", "png"]
    )

    st.divider()

    photo_size = st.selectbox(
        "📏 Select Photo Size",
        [
            "Passport",
            "Aadhaar",
            "PAN Card",
            "Visa"
        ]
    )

    quantity = st.slider(
        "📄 Quantity",
        1,
        20,
        4
    )

    realtime_update = st.checkbox(
        "Live Crop Update",
        value=True
    )

# ==========================================
# HELPER FUNCTION: Generate Grid of Photos
# ==========================================
def create_photo_grid(photo, quantity, size_width, size_height):
    """Create a grid of multiple photo copies for printing."""
    cols = ceil(quantity ** 0.5)
    rows = ceil(quantity / cols)
    
    grid_width = cols * (size_width + 10) + 10
    grid_height = rows * (size_height + 10) + 10
    
    grid_img = Image.new('RGB', (grid_width, grid_height), (255, 255, 255))
    
    for i in range(quantity):
        row = i // cols
        col = i % cols
        x = col * (size_width + 10) + 10
        y = row * (size_height + 10) + 10
        grid_img.paste(photo, (x, y))
    
    return grid_img

# ==========================================
# MAIN
# ==========================================
if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file)
        
        # Validate image
        image.verify()
        image = Image.open(uploaded_file)
        
    except Exception as e:
        st.error(f"❌ Error loading image: {str(e)}")
        st.info("Please upload a valid JPG or PNG file.")
        st.stop()

    col1, col2 = st.columns(2)

    # ==========================================
    # LEFT SIDE
    # ==========================================
    with col1:

        st.markdown('<div class="box">', unsafe_allow_html=True)

        st.subheader("✂️ Crop Photo")

        cropped_img = st_cropper(
            image,
            realtime_update=realtime_update,
            box_color='#2563eb',
            aspect_ratio=(3, 4)
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # RIGHT SIDE
    # ==========================================
    with col2:

        st.markdown('<div class="box">', unsafe_allow_html=True)

        st.subheader("🖼 Final Preview")

        # Resize According to Type
        if photo_size == "Passport":
            size_w, size_h = 300, 400
            
        elif photo_size == "Aadhaar":
            size_w, size_h = 350, 350
            
        elif photo_size == "PAN Card":
            size_w, size_h = 250, 350
            
        else:  # Visa
            size_w, size_h = 400, 400

        final_img = cropped_img.resize((size_w, size_h))

        st.image(
            final_img,
            width=250
        )

        st.write("")

        st.success("✅ Photo Ready")

        st.write(f"📄 Copies: {quantity}")
        st.write(f"📐 Selected Size: {photo_size}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # ==========================================
    # DOWNLOAD SECTION
    # ==========================================
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.subheader("⬇️ Download Photo")

    # Generate grid of photos
    photo_grid = create_photo_grid(final_img, quantity, size_w, size_h)

    # Generate dynamic filename with timestamp and size
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{photo_size.lower().replace(' ', '_')}_{quantity}_copies_{timestamp}.png"

    # Prepare image bytes
    img_bytes = io.BytesIO()
    photo_grid.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    st.download_button(
        label=f"📥 Download {quantity} Copies",
        data=img_bytes.getvalue(),
        file_name=filename,
        mime="image/png",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

else:

    st.info("👈 Upload a photo from sidebar to begin.")