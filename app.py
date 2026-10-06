import os
import requests
import streamlit as st
from dotenv import load_dotenv


# =========================
# Configuration
# =========================

load_dotenv()

KAGGLE_API_URL = os.getenv("KAGGLE_API_URL")
API_KEY = os.getenv("API_KEY")


# =========================
# Page Configuration
# =========================

st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="centered")


# =========================
# Header
# =========================

st.title("🎥 YouTube Summarizer")

st.write("حط لينك فيديو YouTube وأنا هفهم محتواه وأطلعلك ملخص منظم.")


# =========================
# Input
# =========================

youtube_url = st.text_input(
    "YouTube Video URL", placeholder="https://www.youtube.com/watch?v=..."
)


# =========================
# Generate Summary
# =========================

if st.button("Generate Summary", type="primary", use_container_width=True):
    # -------------------------
    # Validate URL
    # -------------------------

    if not youtube_url.strip():
        st.warning("من فضلك حط لينك الفيديو الأول.")

        st.stop()

    # -------------------------
    # Validate API URL
    # -------------------------

    if not KAGGLE_API_URL:
        st.error("Kaggle API URL is not configured.")

        st.stop()

    # -------------------------
    # Validate API Key
    # -------------------------

    if not API_KEY:
        st.error("API Key is not configured.")

        st.stop()

    # -------------------------
    # Prepare Request
    # -------------------------

    payload = {"youtube_url": youtube_url.strip()}

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # -------------------------
    # Send Request
    # -------------------------

    try:
        with st.spinner("⏳ جاري تحميل الـ transcript وفهم محتوى الفيديو..."):
            response = requests.post(
                f"{KAGGLE_API_URL.rstrip('/')}/generate",
                json=payload,
                headers=headers,
                timeout=600,
            )

        # =========================
        # Success
        # =========================

        if response.status_code == 200:
            data = response.json()

            if data.get("success"):
                st.success("تم تلخيص الفيديو بنجاح ✅")

                # -------------------------
                # Summary
                # -------------------------

                summary = data.get("summary", "")

                if summary:
                    st.subheader("📝 ملخص الفيديو")

                    st.markdown(summary)

                else:
                    st.warning("الفيديو اتعالج بنجاح، لكن الـAPI مرجعتش Summary.")

            else:
                error_message = data.get("detail", "حصلت مشكلة أثناء التلخيص.")

                st.error(error_message)

        # =========================
        # Authentication Error
        # =========================

        elif response.status_code == 401:
            st.error("❌ API authentication failed. راجع الـAPI Key.")

        # =========================
        # Bad Request
        # =========================

        elif response.status_code == 400:
            try:
                error_data = response.json()

                st.error(error_data.get("detail", "الـYouTube URL غير صحيح."))

            except:
                st.error("الـYouTube URL غير صحيح.")

        # =========================
        # Server Error
        # =========================

        elif response.status_code >= 500:
            try:
                error_data = response.json()

                st.error(error_data.get("detail", "حصل خطأ في السيرفر."))

            except:
                st.error(f"Server Error: {response.status_code}")

        # =========================
        # Other Errors
        # =========================

        else:
            try:
                error_data = response.json()

                st.error(
                    error_data.get(
                        "detail", f"Unexpected error: {response.status_code}"
                    )
                )

            except:
                st.error(f"Unexpected error: {response.status_code}")

    # =========================
    # Timeout
    # =========================

    except requests.exceptions.Timeout:
        st.error("⏳ الفيديو أخد وقت أطول من المتوقع. جرب فيديو أقصر.")

    # =========================
    # Connection Error
    # =========================

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ مش قادر أوصل لـ Kaggle API. تأكد إن الـNotebook شغال وإن ngrok شغال."
        )

    # =========================
    # Unexpected Error
    # =========================

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
