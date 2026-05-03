import streamlit as st
import requests
from langdetect import detect

# 1. إعدادات الصفحة
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 المساعد الذكي الخاص بالشركة (RAG)")
st.write("اسألني أي شيء عن مستندات الشركة!")

# 2. إعدادات الاتصال
# غيّر البورت لـ 8000 إذا كنت تشغل من Docker، أو 5000 إذا uvicorn مباشر
FASTAPI_HOST = "http://localhost:8000"

# ==============  Sidebar ==============
st.sidebar.header("⚙️ الإعدادات")

# اختيار المشروع
project_id = st.sidebar.number_input("📂 Project ID", min_value=1, value=1, step=1)

# عرض المصادر (Toggle)
show_sources = st.sidebar.toggle("📄 عرض المصادر", value=False,
                                  help="عرض المستندات المستخدمة في الإجابة (مفيد للتطوير والاختبار)")

st.sidebar.divider()

# مسح المحادثة
if st.sidebar.button("🗑️ مسح المحادثة", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# عدد الرسائل
if "messages" in st.session_state and len(st.session_state.messages) > 0:
    msg_count = len(st.session_state.messages)
    st.sidebar.caption(f"💬 عدد الرسائل: {msg_count}")

# ==============  Language Detection ==============
LANG_MAP = {
    "ar": {"name": "العربية", "flag": "🇸🇦", "instruction": "أجب باللغة العربية."},
    "en": {"name": "English", "flag": "🇺🇸", "instruction": "Reply in English."},
    "fr": {"name": "Français", "flag": "🇫🇷", "instruction": "Répondez en français."},
    "es": {"name": "Español", "flag": "🇪🇸", "instruction": "Responde en español."},
    "tr": {"name": "Türkçe", "flag": "🇹🇷", "instruction": "Türkçe cevap verin."},
}

def detect_language(text: str) -> dict:
    """كشف لغة النص تلقائياً"""
    try:
        lang_code = detect(text)
        if lang_code in LANG_MAP:
            return {"code": lang_code, **LANG_MAP[lang_code]}
        # إذا اكتشف لغة غريبة (مثل fa للفارسي بالخطأ بسبب العامية)، نعتبرها عربية كافتراضي
        return {"code": "ar", **LANG_MAP["ar"]}
    except Exception:
        return {"code": "en", **LANG_MAP["en"]}

# ==============  Chat State ==============
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # عرض المصادر للرسائل السابقة إذا الخيار مفعّل
        if show_sources and message["role"] == "assistant" and message.get("sources"):
            with st.expander("📄 المصادر المستخدمة"):
                st.code(message["sources"], language=None)

# ==============  Chat Input ==============
if prompt := st.chat_input("بماذا يمكنني مساعدتك اليوم؟"):
    # كشف اللغة
    lang = detect_language(prompt)

    # عرض سؤال المستخدم مع badge اللغة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"{prompt}  `{lang['flag']} {lang['name']}`")

    # إرسال السؤال إلى FastAPI
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير والبحث في المستندات... 🧠"):
            try:
                api_url = f"{FASTAPI_HOST}/api/v1/nlp/index/answer/{project_id}"

                # إضافة تعليمات اللغة للنص
                enhanced_text = f"{lang['instruction']}\n{prompt}"

                # تجهيز chat_history (نرسل آخر 6 رسائل فقط لتجنب تجاوز الحد الأقصى للتوكنز)
                # نستثني الرسالة الحالية لأنها سترسل في text
                recent_messages = st.session_state.messages[:-1][-6:]
                formatted_history = [{"role": m["role"], "content": m["content"]} for m in recent_messages]

                response = requests.post(
                    api_url,
                    json={
                        "text": enhanced_text, 
                        "limit": 5,
                        "chat_history": formatted_history
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "لم أتمكن من إيجاد إجابة.")
                    full_prompt = data.get("full_prompt", "")

                    st.markdown(answer)

                    # عرض المصادر إذا الخيار مفعّل
                    if show_sources and full_prompt:
                        with st.expander("📄 المصادر المستخدمة"):
                            st.code(full_prompt, language=None)

                    # حفظ في سجل المحادثة
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": full_prompt if full_prompt else None
                    })
                else:
                    error_detail = response.json().get("signal", response.status_code)
                    st.error(f"حدث خطأ في السيرفر: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("❌ لا يمكن الاتصال بالسيرفر. هل تأكدت أن FastAPI يعمل؟")
            except requests.exceptions.Timeout:
                st.error("⏱️ انتهت مهلة الانتظار. السيرفر يستغرق وقتاً طويلاً.")