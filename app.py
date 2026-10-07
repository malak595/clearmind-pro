import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# إعدادات الصفحة الأساسية للتطبيق
st.set_page_config(page_title="ClearMind Pro", page_icon="🧠", layout="wide")

# تحميل المتغيرات البيئية لضمان الأمان
load_dotenv()

# تحسين واجهة التطبيق باستخدام CSS مخصص
st.markdown("""
    <style>
    .main { background-color: #f5f7fb; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4A90E2; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# ----------------- إعدادات تعدد اللغات (Localization) -----------------
# 1. تحديد اللغات المتوفرة في القائمة الجانبية أولاً
st.sidebar.header("🌐 Language / اللغة / Langue")
lang_choice = st.sidebar.selectbox("Choose Language:", ["العربية", "English", "Français"])

# 2. قاموس النصوص لترجمة كامل الواجهة تلقائياً
translations = {
    "العربية": {
        "title": "🧠 ClearMind Pro - منصتك للصحة النفسية والرفاهية الأكاديمية",
        "subtitle": "نحن هنا لمساعدتك في إدارة التوتر الأكاديمي، تنظيم وقتك، وتحقيق التوازن الصحي.",
        "sidebar_control": "📁 لوحة التحكم والإعدادات",
        "api_label": "لتفعيل الشات بوت Gemini API أدخلي مفتاح الـ",
        "music_header": "🎵 خلفيات صوتية هادئة",
        "music_select": "اختر الخلفية الصوتية المفضلة لديك:",
        "music_options": ["أصوات المطر الهادئة", "صوت البحر الأمواج", "موسيقى تصفية الذهن Lo-Fi"],
        "exercise_header": "🧘 تمارين الاسترخاء والراحة",
        "exercise_select": "اختر تمرين الاسترخاء اليومي:",
        "exercise_options": ["تمرين التنفس المربع (Box Breathing)", "تمرين التخلص من تفريغ الأفكار (Mind Dump)"],
        "exercise_btn": "ابدأ التمرين الآن",
        "exercise_success": "رائع! خذ شهيقاً عميقاً وابدأ في تطبيق: ",
        "tabs": ["📊 مقياس الاحتراق الأكاديمي", "💬 المحادثة الذكية المدعومة"],
        "burnout_title": "📊 مقياس وحاسبة الاحتراق الأكاديمي والتوتر",
        "burnout_subtitle": "أجيبي عن الأسئلة التالية بدقة لتقييم مستوى التوتر الحالي لديكِ والحصول على نصائح مخصصة:",
        "sleep_label": "ساعات النوم اليومية:",
        "study_label": "ساعات الدراسة اليومية المتواصلة:",
        "leisure_label": "وقت الفراغ والراحة بالساعات:",
        "stress_label": "مستوى الضغط الدراسي المتوقع (من 1 إلى 10):",
        "calc_btn": "احسب مستوى الاحتراق الأكاديمي",
        "burnout_res": "نسبة التوتر والاحتراق الأكاديمي المتوقعة: ",
        "status_low": "وضعك ممتاز! أنت تديرين وقتك وضغوطك بشكل صحي جداً. استمري في هذا التوازن.",
        "status_med": "تحذير متوسط: هناك بعض المؤشرات على بداية الإرهاق. يُنصح بزيادة فترات الراحة وتنظيم ساعات النوم.",
        "status_high": "تنبيه مرتفع: أنت تعانين من إرهاق أكاديمي شديد! من الضروري التوقف قليلاً، ممارسة تمارين الاسترخاء، وإعادة ترتيب أولوياتك لحماية صحتك النفسية.",
        "chat_title": "💬 المساعد النفسي والأكاديمي الذكي",
        "chat_subtitle": "أنا هنا للاستماع إليك ومساعدتك في التغلب على صعوبات الدراسة وتنظيم وقتك. تحدث معي بحرية.",
        "chat_input_placeholder": "اكتبي رسالتكِ هنا...",
        "out_of_scope": "عذراً، أنا متخصص فقط في مجال الصحة النفسية، الرفاهية الأكاديمية، وتنظيم وقت الدراسة للطلاب لمساعدتهم على تقليل التوتر والضغط.",
        "api_warning": "⚠️ ملاحظة: الشات بوت يعمل حالياً في الوضع التجريبي. يرجى إدخال مفتاح الـ API Key في القائمة الجانبية لتفعيله فوراً.",
        "api_error": "لم أتمكن من معالجة النص حالياً، يرجى المحاولة مرة أخرى.",
        "server_error": "عذراً، حدثت مشكلة أثناء الاتصال بالخادم. تفاصيل الخطأ: ",
        "system_instruction": "أنت مساعد ذكي متقدم لتطبيق ClearMind Pro. أجب دائماً وبشكل كامل باللغة العربية الودودة والداعمة لمساعدة الطلاب على إدارة التوتر الأكاديمي وتنظيم وقت الدراسة والاهتمام بالصحة النفسية والرفاهية."
    },
    "English": {
        "title": "🧠 ClearMind Pro - Academic Well-being Platform",
        "subtitle": "We are here to help you manage academic stress, organize study time, and achieve a healthy balance.",
        "sidebar_control": "📁 Control Panel & Settings",
        "api_label": "Enter Gemini API Key to activate chatbot:",
        "music_header": "🎵 Calm Soundscapes",
        "music_select": "Choose your preferred background sound:",
        "music_options": ["Calm Rain Sounds", "Ocean Waves", "Lo-Fi Mind Clearing Music"],
        "exercise_header": "🧘 Relaxation Exercises",
        "exercise_select": "Choose a daily relaxation exercise:",
        "exercise_options": ["Box Breathing Exercise", "Mind Dump Exercise"],
        "exercise_btn": "Start Exercise Now",
        "exercise_success": "Great! Take a deep breath and start: ",
        "tabs": ["📊 Burnout Predictor", "💬 AI Support Chat"],
        "burnout_title": "📊 Academic Burnout & Stress Predictor",
        "burnout_subtitle": "Answer the following questions accurately to evaluate your current stress level and receive personalized tips:",
        "sleep_label": "Daily Sleep Hours:",
        "study_label": "Daily Continuous Study Hours:",
        "leisure_label": "Leisure & Free Time (Hours):",
        "stress_label": "Expected Study Stress Level (1 to 10):",
        "calc_btn": "Calculate Burnout Score",
        "burnout_res": "Expected Academic Burnout Score: ",
        "status_low": "Excellent status! You manage your time and stress very healthily. Keep up the balance.",
        "status_med": "Moderate warning: There are some indicators of early burnout. Increasing rest periods and regulating sleep is advised.",
        "status_high": "High alert: You are suffering from severe academic exhaustion! It is essential to pause, practice relaxation, and reset priorities.",
        "chat_title": "💬 AI Psychological & Academic Assistant",
        "chat_subtitle": "I am here to listen to you and help you overcome study difficulties and organize time. Talk to me freely.",
        "chat_input_placeholder": "Type your message here...",
        "out_of_scope": "Sorry, I specialize only in mental health, academic well-being, and study time management for students.",
        "api_warning": "⚠️ Note: The chatbot is currently in demo mode. Please enter an API Key in the sidebar to activate it.",
        "api_error": "Could not process text right now, please try again.",
        "server_error": "Sorry, a server connection error occurred. Details: ",
        "system_instruction": "You are an advanced AI assistant for ClearMind Pro. Always reply entirely in supportive, empathetic, and professional English to help students manage academic stress, organize study schedules, and maintain mental well-being."
    },
    "Français": {
        "title": "🧠 ClearMind Pro - Plateforme de Bien-être Académique",
        "subtitle": "Nous sommes là pour vous aider à gérer le stress académique, organiser votre temps et équilibrer votre vie.",
        "sidebar_control": "📁 Panneau de configuration",
        "api_label": "Entrez la clé API Gemini pour activer le chatbot :",
        "music_header": "🎵 Ambiances Sonores Calmes",
        "music_select": "Choisissez votre fond sonore préféré :",
        "music_options": ["Sons de Pluie Calme", "Vagues de l'Océan", "Musique Lo-Fi pour vider l'esprit"],
        "exercise_header": "🧘 Exercices de Relaxation",
        "exercise_select": "Choisissez un exercice de relaxation quotidien :",
        "exercise_options": ["Exercice de Respiration Carrée (Box Breathing)", "Exercice de Vidage d'Esprit (Mind Dump)"],
        "exercise_btn": "Commencer l'exercice",
        "exercise_success": "Super ! Prenez une grande inspiration et commencez : ",
        "tabs": ["📊 Indicateur de Burnout", "💬 Chat de Support IA"],
        "burnout_title": "📊 Simulateur de Burnout Académique & Stress",
        "burnout_subtitle": "Répondez précisément aux questions pour évaluer votre niveau de stress et obtenir des conseils personnalisés :",
        "sleep_label": "Heures de sommeil quotidiennes :",
        "study_label": "Heures d'étude continue par jour :",
        "leisure_label": "Temps libre et loisirs (Heures) :",
        "stress_label": "Niveau de stress académique attendu (1 à 10) :",
        "calc_btn": "Calculer le score de Burnout",
        "burnout_res": "Score de Burnout Académique estimé : ",
        "status_low": "Excellent état ! Vous gérez votre temps et votre stress de manière très saine. Continuez ainsi.",
        "status_med": "Avertissement modéré : Il y a des signes de début d'épuisement. Il est conseillé d'augmenter le repos et de régler le sommeil.",
        "status_high": "Alerte élevée : Vous souffrez d'un épuisement académique sévère ! Il est essentiel de faire une pause et de revoir vos priorités.",
        "chat_title": "💬 Assistant IA Psychologique & Académique",
        "chat_subtitle": "Je suis là pour vous écouter, vous aider à surmonter les difficultés d'études et organiser votre temps. Parlez-moi librement.",
        "chat_input_placeholder": "Écrivez votre message ici...",
        "out_of_scope": "Désolé, je me spécialise uniquement dans la santé mentale, le bien-être académique et la gestion du temps pour les étudiants.",
        "api_warning": "⚠️ Note : Le chatbot est en mode démo. Veuillez saisir une clé API dans la barre latérale pour l'activer.",
        "api_error": "Impossible de traiter le texte pour le moment, veuillez réessayer.",
        "server_error": "Désolé, une erreur de connexion au serveur est survenue. Détails : ",
        "system_instruction": "Vous êtes un assistant IA avancé pour ClearMind Pro. Répondez toujours entièrement en français, de manière bienveillante, encourageante et empathique pour aider les étudiants à gérér le stress, planifier les études et prendre soin de leur santé mentale."
    }
}

# جلب نصوص اللغة المختارة حالياً
text = translations[lang_choice]

# تطبيق العناوين المترجمة على الواجهة مباشرة
st.title(text["title"])
st.write(text["subtitle"])

# ----------------- محتويات القائمة الجانبية المترجمة -----------------
st.sidebar.markdown("---")
st.sidebar.subheader(text["sidebar_control"])

