import streamlit as st
import numpy as np
import pandas as pd
import datetime
import time

# 1. إعدادات الصفحة والتصميم الهادئ والمريح (Sage Green Theme)
st.set_page_config(page_title="ClearMind Pro", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    div[data-testid="stVerticalBlock"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #2c4a3e; font-family: 'Segoe UI', sans-serif; font-weight: 600; }
    .stButton>button { background-color: #6b8e23; color: white; border-radius: 20px; border: none; padding: 8px 20px; }
    .stButton>button:hover { background-color: #556b2f; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 ClearMind Pro")
st.subheader("Advanced Predictive Platform for Academic Well-being & Stress Management")
st.markdown("---")

# إدارة حالة البيانات للرسم البياني (Mood & Burnout Tracker)
if "history_df" not in st.session_state:
    dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(4, -1, -1)]
    st.session_state.history_df = pd.DataFrame({"التاريخ": dates, "مؤشر الإجهاد": [45, 55, 40, 60, 50]})

# 📓 إدارة حالة المذكرات الخاصة (Private Journal)
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# 🔒 إدخال المفتاح المحدث من الواجهة بدون مشاكل Secrets
import google.generativeai as genai

API_KEY = st.sidebar.text_input("🔑 أدخلي مفتاح الـ Gemini API لتفعيل الشات بوت:", type="password")

        else:
            if API_KEY:
                try:
                    system_instruction = "أنت مساعد ذكي متقدم لتطبيق ClearMind Pro. أجب دائماً بلغة عربية ودودة وداعمة لمساعدة الطلاب على إدارة التوتر الأكاديمي وتنظيم وقت الدراسة."

                    # تهيئة المكتبة والموديل مباشرة هنا
                    import google.generativeai as genai
                    genai.configure(api_key=API_KEY)
                    local_model = genai.GenerativeModel('gemini-3.8-flash')

                    response_ai = local_model.generate_content(
                        f"{system_instruction}\n\nالمستخدم يقول: {prompt}"
                    )

                    if response_ai.text:
                        response = response_ai.text
                    else:
                        response = "لم أتمكن من معالجة النص، يرجى المحاولة مرة أخرى."
                except Exception as e:
                    response = f"عذراً، حدثت مشكلة أثناء الاتصال بالخادم. تفاصيل الخطأ: {e}"
            else:
                response = "⚠️ يرجى إدخال مفتاح الـ API في القائمة الجانبية لتفعيل المحادثة."


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
            st.success("تم مسح الأفكار بنجاح!")

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
        st.error("⚠️ تنبيه مرتفع: مستويات الإجهاد والقلق تتطلب استراحة فورية.")
    elif normalized_risk > 40:
        st.warning("⚠️ تنبيه متوسط: يرجى زيادة ساعات الراحة وتقليل الضغط الدراسي.")
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

    chart_data = st.session_state.history_df.set_index("التاريخ")
    st.line_chart(chart_data)

    st.markdown("---")
    st.markdown("---")
    st.header("📓 Private Journal")
    entry_title = st.text_input("عنوان تدوينة اليوم:")
    entry_content = st.text_area("اكتبي تفاصيل ما يدور في ذهنكِ هنا...")
    
    if st.button("🔒 حفظ التدوينة بأمان"):
        if entry_content:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.journal_entries.append({"time": now_time, "title": entry_title, "content": entry_content})
            st.success("تم الحفظ بأمان تام!")
            
    if st.session_state.journal_entries:
        for entry in reversed(st.session_state.journal_entries):
            with st.expander(f"📅 {entry['time']} - {entry['title']}"): 
                st.write(entry['content'])

with col2:
    st.header("💬 Context-Aware AI Support")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً بكِ في ClearMind Pro. كيف تشعرين اليوم؟"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): 
            st.markdown(message["content"])

    if prompt := st.chat_input("اكتبي رسالتكِ هنا..."):
        with st.chat_message("user"): 
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        out_of_scope_keywords = ["برمجة", "كود", "سياسة", "اقتصاد", "رياضيات", "فيزياء", "تاريخ", "كورة", "لعبة"]
        if any(keyword in prompt.lower() for keyword in out_of_scope_keywords):
            response = "أنا هنا كمساعد ذكي مرن ومخصص لدعم الصحة النفسية والرفاهية الأكاديمية فقط. أنا غير متخصص في هذا المجال الخارجي، لكن يمكنني مساعدتكِ في إعداد خطة دراسية لتقليل التوتر الناتج عن هذه المواد إذا أردتِ!"
        else:
            if API_KEY:
                try:
                    # إعداد التعليمات البرمجية للمساعد الذكي وتوجيهه
                    system_instruction = "أنت مساعد ذكي متقدم لتطبيق ClearMind Pro. أجب دائماً بلغة عربية ودودة وداعمة لمساعدة الطلاب على إدارة التوتر الأكاديمي وتنظيم وقت الدراسة."
                    
                    # استدعاء الموديل وتمرير النص بشكل سليم وآمن
                                        # 1. إعادة التأكد من ضبط الإعدادات بالمفتاح النشط فوراً
                    genai.configure(api_key=API_KEY)
                    local_model = genai.GenerativeModel('gemini-3.8-flash')
                    
                    # 2. إرسال الطلب للموديل المحلي الجديد
                    response_ai = local_model.generate_content(
                        f"{system_instruction}\n\nالمستخدم يقول: {prompt}"
                    )

                    
                    # التأكد من جلب النص البرمجي بشكل صحيح ودعم الأخطاء المباشرة
                    if response_ai.text:
                        response = response_ai.text
                    else:
                        response = "لم أتمكن من معالجة النص، يرجى المحاولة مرة أخرى."
                        
                except Exception as e:
                    # إظهار الخطأ الحقيقي لمساعدتك في معالجة أي توقف بدلاً من الرسالة الثابتة المبهمة
                    response = f"عذراً، حدثت مشكلة أثناء الاتصال بالخادم. تفاصيل الخطأ: {e}"
            else:
                response = "⚠️ (في القائمة الجانبية أدخلي الذكاء الاصطناعي بدقة API Key ملاحظة: الشات بوت يعمل حالياً في الوضع التجريبي، يرجى تفعيل الـ) تشعر بك تماماً"

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
