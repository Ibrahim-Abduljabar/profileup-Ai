
import streamlit as st 
import docx
st.set_page_config(page_title="ProfileUp AI", page_icon="📝", layout="centered")
st.title("📝 ProfileUp AI - صانع السير الذاتية")
st.write("أدخل معلوماتك ببساطة ودع الذكاء الاصطناعي يتولى الصياغة الاحترافية.")


name = st.text_input("الاسم الكامل")
job_title = st.text_input("المسمى الوظيفي المستهدف")
raw_experience = st.text_area("الخبرات المهنية والعملية")
raw_education = st.text_area("التعليم والشهادات")
raw_skills = st.text_input("المهارات (افصل بينها بفاصلة)")


if st.button("توليد السيرة الذاتية الاحترافية ✨"):
    if not name or not job_title:
        st.warning("الرجاء إدخال الاسم والمسمى الوظيفي على الأقل.")
    else:
        with st.spinner("جاري صياغة سيرتك الذاتية باحترافية..."):
            from groq import Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            prompt = f"قم بإنشاء سيرة ذاتية احترافية باللغة العربية: الاسم {name}، الوظيفة {job_title}، الخبرات {raw_experience}، التعليم {raw_education}، المهارات {raw_skills}."
            completion = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}])
            completion = client.chat.completions.create(model="groq/compound-mini", messages=[{"role": "user", "content": prompt}])
            st.markdown(cv_result)

            st.success("تم التوليد بنجاح!")


if 'cv_text' in st.session_state:
    st.subheader("📄 السيرة الذاتية الناتجة:")
    st.write(st.session_state['cv_text'])
    
  
    doc = docx.Document()
    doc.add_heading(f"السيرة الذاتية - {name}", 0)
    doc.add_paragraph(st.session_state['cv_text'])
    
    import io
    bio = io.BytesIO()
    doc.save(bio)
    
    st.download_button(
        label="تحميل الملف بصيغة Word (DOCX) 📥",
        data=bio.getvalue(),
        file_name=f"CV_{name}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
