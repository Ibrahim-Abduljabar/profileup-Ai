import streamlit as st
import docx
from groq import Groq

# إعدادات واجهة التطبيق
st.set_page_config(page_title="Profileup AI", page_icon="📄", layout="centered")
st.title("📄 Profileup AI - صانع السير الذاتية")
st.write("أدخل معلوماتك البسيطة لتوليد سيرة ذاتية احترافية بالذكاء الاصطناعي سريعاً.")

# مدخلات المستخدم
name = st.text_input("الاسم الكامل")
job_title = st.text_input("المسمى الوظيفي المستهدف")
raw_experience = st.text_area("الخبرات المهنية وسنوات العمل")
raw_education = st.text_area("التعليم (الجامعة والتخصص والشهادات)")
raw_skills = st.text_input("المهارات (افصل بينها بفاصلة)")

if st.button("✨ توليد السيرة الذاتية الاحترافية"):
    if not name or not job_title:
        st.warning("الرجاء إدخال الاسم والمسمى الوظيفي على الأقل.")
    else:
        with st.spinner("جاري صياغة سيرتك الذاتية بأعلى جودة..."):
            try:
                # الاتصال بسيرفر Groq ومفتاح الأمان
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                # صياغة الأمر الموجه للذكاء الاصطناعي
                prompt = f"""
                أنت خبير توظيف ومحترف في كتابة السير الذاتية المتوافقة مع أنظمة الـ ATS.
                قم بإنشاء سيرة ذاتية احترافية ومنظمة باللغة العربية بناءً على البيانات التالية:
                الاسم: {name}
                المسمى الوظيفي المستهدف: {job_title}
                الخبرات: {raw_experience}
                التعليم: {raw_education}
                المهارات: {raw_skills}
                """
                
                # إرسال الطلب لنموذج Llama 3 النشط والمستقر لعام 2026
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # استخراج النتيجة وعرضها للمستخدم
                cv_result = completion.choices[0].message.content
                st.markdown(cv_result)
                st.success("تم التوليد بنجاح!")
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بـ Groq: {e}")
