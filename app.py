import streamlit as st
import numpy as np
import pandas as pd
import datetime
import time

# 1. إعدادات الصفحة والتصميم الهادئ والمريح (Sage Green Theme)
st.set_page_config(page_title="ClearMind Pro", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* تغيير خلفية التطبيق بالكامل */
    .stApp {
        background-color: #f4f7f6;
    }
    /* تحسين شكل البطاقات والإطارات */
    div[data-testid="stVerticalBlock"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    /* تخصيص العناوين */
    h1, h2, h3 {
        color: #2c4a3e; /* أخضر داكن مهدئ */
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    /* تخصيص الأزرار لتكون جذابة ودائرية */
    .stButton>button {
        background-color: #6b8e23; /* ألوان الباستيل الأخضر */
        color: white;
        border-radius: 20px;
        border: none;
        padding: 8px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #556b2f;
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 ClearMind Pro")
st.subheader("Advanced Predictive Platform for Academic Well-being & Stress Management")
st.markdown("---")

# إدارة حالة البيانات للرسم البياني (Mood & Burnout Tracker)
if "history_df" not in st.session_state:
    dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(4, -1, -1)]
    st.session_state.history_df = pd.DataFrame({
        "التاريخ": dates,
        "مؤشر الإجهاد": [45, 55, 40, 60, 50]
    })

# إدارة حالة المذكرات الخاصة (Private Journal)
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# شريط جانبي (Sidebar) للموسيقى والتمارين
with st.sidebar:
    st.header("🎵 Calm Soundscapes")
    track_choice = st.selectbox("اختر الخلفية الصوتية:", ["صوت المطر الهادئ", "موجات التأمل والدراسة", "موسيقى البيانو لتقليل القلق"])
    if track_choice == "صوت المطر الهادئ":
        st.audio("https://soundhelix.com")
    elif track_choice == "موجات التأمل والدراسة":
        st.audio("https://soundhelix.com")
    else:
        st.audio("https://soundhelix.com")
        
    st.markdown("---")
    st.header("🧘 Relaxation Exercises")
    exercise = st.radio("اختر تمرين الاسترخاء السريع:", ["تمرين التنفس المربع (Box Breathing)", "تفريغ الأفكار السلبي (Mind Dump)"])
    
    if exercise == "تمرين التنفس المربع (Box Breathing)":
        st.info("شهيق لـ 4 ثوانٍ ➡️ اكتم النفس لـ 4 ثوانٍ ➡️ زفير لـ 4 ثوانٍ ➡️ اكتم النفس لـ 4 ثوانٍ.")
        if st.button("ابدأ التوجيه البصري"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text("🌬️ شهيق عميق...")
            for i in range(25): time.sleep(0.04); progress_bar.progress(i)
            status_text.text("🛑 اكتم النفس واسترخِ...")
            for i in range(25, 50): time.sleep(0.04); progress_bar.progress(i)
            status_text.text("😮 زفير بطيء للتوتر...")
            for i in range(50, 75): time.sleep(0.04); progress_bar.progress(i)
            status_text.text("🛑 اكتم النفس...")
            for i in range(75, 101): time.sleep(0.04); progress_bar.progress(i)
            status_text.text("✅ أحسنتِ! كرري التمرين إذا شعرتِ بضغط إضافي.")
            
    elif exercise == "تفريغ الأفكار السلبي (Mind Dump)":
        distraction_text = st.text_area("ما الذي يشغل عقلكِ الآن؟", key="distract")
        if st.button("🗑️ نسف الأفكار وتصفية الذهن"):
            st.balloons()
            st.success("تم مسح الأفكار بنجاح! عقلكِ الآن أكثر صفاءً.")

# الواجهة الرئيسية: تقسيم المساحة بين التحليلات والشات بوت والمذكرات
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Academic Burnout Predictor")
    academic_pressure = st.slider("مستوى الضغط الأكاديمي الحالي (1-10)", 1, 10, 5)
    anxiety_level = st.slider("مستوى القلق العام (1-10)", 1, 10, 4)
    study_hours = st.slider("ساعات الدراسة اليومية", 1, 16, 6)
    sleep_hours = st.slider("ساعات النوم (Sleep Hours)", 3, 12, 7)
    free_time = st.slider("وقت الفراغ والراحة بالساعات", 0, 8, 2)
    meals_count = st.slider("عدد الوجبات المتناولة اليوم", 0, 5, 3)
    
    positive_factors = (sleep_hours * 0.3) + (free_time * 0.4) + (meals_count * 0.5)
    negative_factors = (academic_pressure * 0.8) + (anxiety_level * 0.9) + (study_hours * 0.3)
    raw_risk = (negative_factors - positive_factors) + 20
    normalized_risk = min(max(int((raw_risk / 25) * 100), 0), 100)
    
    st.metric(label="مؤشر خطر الاحتراق الأكاديمي الحالي", value=f"{normalized_risk}%")
    
    if normalized_risk > 70:
        st.error("⚠️ تنبيه مرتفع: مستويات الإجهاد والقلق تتطلب استراحة فورية وتنظيم الوجبات والنوم لحماية صحتكِ.")
    elif normalized_risk > 40:
        st.warning("⚠️ تنبيه متوسط: يرجى زيادة ساعات الراحة وتقليل الضغط الدراسي لتفادي الاحتراق الأكاديمي.")
    else:
        st.success("✅ وضعكِ الأكاديمي والنفسي متزن وممتاز حالياً!")
        
    if st.button("💾 حفظ قراءة اليوم في الإحصائيات"):
        today = datetime.date.today()
        if today in st.session_state.history_df["التاريخ"].values:
            st.session_state.history_df.loc[st.session_state.history_df["التاريخ"] == today, "مؤشر الإجهاد"] = normalized_risk
        else:
            new_row = pd.DataFrame({"التاريخ": [today], "مؤشر الإجهاد": [normalized_risk]})
            st.session_state.history_df = pd.concat([st.session_state.history_df, new_row], ignore_index=True)
        st.success("تم تحديث مخطط الإحصائيات بنجاح!")

    st.markdown("### 📈 مسار الإجهاد الأسبوعي (Burnout Tracking)")
    chart_data = st.session_state.history_df.set_index("التاريخ")
    st.line_chart(chart_data)

    st.markdown("---")
    st.header("📓 Private Journal")
    entry_title = st.text_input("عنوان تدوينة اليوم (مثال: شعور قبل الامتحان):")
    entry_content = st.text_area("اكتبي تفاصيل ما يدور في ذهنكِ هنا...")
    
    if st.button("🔒 حفظ التدوينة بأمان"):
        if entry_content:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.journal_entries.append({"time": now_time, "title": entry_title, "content": entry_content})
            st.success("تم حفظ تدوينتكِ الخاصة بنجاح وأمان تام!")
            
    if st.session_state.journal_entries:
        for idx, entry in enumerate(reversed(st.session_state.journal_entries)):
            with st.expander(f"📅 {entry['time']} - {entry['title']}"):
                st.write(entry['content'])

with col2:
    st.header("💬 Context-Aware AI Support")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً بكِ في ClearMind Pro. كيف تشعرين اليوم؟"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("اكتبي رسالتكِ هنا..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        out_of_scope_keywords = ["برمجة", "كود", "سياسة", "اقتصاد", "رياضيات", "فيزياء", "تاريخ", "كورة", "لعبة"]
        if any(keyword in prompt.lower() for keyword in out_of_scope_keywords):
            response = "أنا هنا كمساعد ذكي مرن ومخصص لدعم الصحة النفسية والرفاهية الأكاديمية فقط. أنا غير متخصص في هذا المجال الخارجي، لكن يمكنني مساعدتكِ في إعداد خطة دراسية لتقليل التوتر الناتج عن هذه المواد إذا أردتِ!"
        else:
            response = "أشعر بكِ تماماً. بناءً على معايير ClearMind Pro لإدارة التوتر الأكاديمي، أنصحكِ باستخدام مشغل الصوت في القائمة الجانبية للاستماع إلى ألحان المطر الهادئة، ثم تجربة تمين التنفس المربع لمدة دقيقتين فقط لإعادة شحن طاقتكِ الذهنية."
            
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
