import streamlit as st
import os
import json
from pathlib import Path
from PIL import Image
import random

# === CONFIG ===
IMAGE_DIR = "images"
LABEL_OUTPUT = "train.json"
CATEGORIES = ["MC", "referral letter", "tax invoice", "dr memo"]

# === Load all image files only once ===
if "image_list" not in st.session_state:
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(image_files)
    st.session_state.image_list = image_files
    st.session_state.index = 0
    st.session_state.annotations = []

# === Current image ===
if st.session_state.index < len(st.session_state.image_list):
    current_file = st.session_state.image_list[st.session_state.index]
    img_path = os.path.join(IMAGE_DIR, current_file)
    
    st.image(Image.open(img_path), caption=current_file, use_column_width=True)
    st.markdown(f"**[{st.session_state.index + 1}/{len(st.session_state.image_list)}]**")

    selected_label = st.radio("Select document category:", CATEGORIES, key=current_file)

    if st.button("✅ Submit Label"):
        st.session_state.annotations.append({
            "file_name": current_file,
            "ground_truth": f"class: {selected_label}"
        })
        st.session_state.index += 1
        st.rerun()
else:
    st.success("✅ Annotation complete.")
    if st.button("💾 Save to train.json"):
        with open(LABEL_OUTPUT, "w") as f:
            json.dump({"images": st.session_state.annotations}, f, indent=2)
        st.download_button("⬇️ Download train.json", data=json.dumps({"images": st.session_state.annotations}, indent=2), file_name="train.json", mime="application/json")
