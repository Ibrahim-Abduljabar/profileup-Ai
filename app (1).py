

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
            
            cv_result = generate_cv_logic(name, job_title, raw_experience, raw_education, raw_skills)
            st.session_state['cv_text'] = cv_result
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
