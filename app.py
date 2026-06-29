import streamlit as st
from groq import Groq
import time

st.set_page_config(
    page_title="ProfileUp AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.write("### ProfileUp AI - صانع السير الذاتية 📄✨")
st.caption("أدخل بياناتك المهنية والذكاء الاصطناعي سيقوم بصياغة سيرة ذاتية متوافقة مع أنظمة الـ ATS فوراً")
st.divider()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

if "cv_list" not in st.session_state:
    st.session_state.cv_list = [{"id": 0}]

st.write("#### 🛠️ مدخلات السير الذاتية")

for index, cv_item in enumerate(st.session_state.cv_list):
    st.write(f"##### 📋 السيرة الذاتية رقم ({index + 1})")
    
    name = st.text_input(f"الاسم الكامل:", key=f"name_{cv_item['id']}")
    job_title = st.text_input(f"المسمى الوظيفي المستهدف:", key=f"title_{cv_item['id']}")
    raw_experience = st.text_area(f"الخبرات المهنية وسنوات العمل:", height=100, key=f"exp_{cv_item['id']}")
    raw_education = st.text_area(f"التعليم والشهادات الأكاديمية:", height=100, key=f"edu_{cv_item['id']}")
    raw_skills = st.text_area(f"المهارات التقنية والشخصية:", height=100, key=f"skills_{cv_item['id']}")
    
    if not name or not job_title:
        st.warning(f"⚠️ الرجاء إدخال الاسم والمسمى الوظيفي المستهدف للسيرة الذاتية رقم {index + 1}...")
    else:
        if st.button(f"🚀 صياغة السيرة الذاتية رقم {index + 1}", key=f"btn_{cv_item['id']}"):
            with st.spinner("⏳ جاري صياغة السيرة الذاتية باحترافية..."):
                try:
                    prompt = f"""
                    صيغ السيرة الذاتية التالية بطريقة متوافقة مع أنظمة الـ ATS وبأسلوب محترف للغاية باللغة العربية:
                    
                    الاسم: {name}
                    المسمى الوظيفي: {job_title}
                    الخبرات: {raw_experience}
                    التعليم: {raw_education}
                    المهارات: {raw_skills}
                    
                    ---
                    المخرجات المطلوبة:
                    قم بتنظيم المدخلات السابقة في سيرة ذاتية ممتازة تحتوي على الأقسام التالية:
                    - الملخص المهني (Professional Summary).
                    - الخبرات العملية (Work Experience) مصاغة بأسلوب الإنجازات.
                    - التعليم والشهادات (Education).
                    - المهارات التقنية والشخصية (Skills).
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    cv_result = completion.choices[0].message.content
                    st.markdown(cv_result)
                    st.success("✅ تم الفراغ من الصياغة بنجاح!")
                except Exception as e:
                    st.error(f"⚠️ حدث خطأ في الاتصال بـ Groq: {e}")
                    
    st.write("---")

if st.button("➕ إضافة سيرة ذاتية أخرى"):
    new_id = len(st.session_state.cv_list)
    st.session_state.cv_list.append({"id": new_id})
    st.rerun()
