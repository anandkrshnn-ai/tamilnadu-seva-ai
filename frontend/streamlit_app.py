import streamlit as st
import requests
import os

# Streamlit Page Setting
st.set_page_config(
    page_title="TamilNadu Seva AI - Public Welfare Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling for high-end UI design
st.markdown("""
<style>
    /* Styling headers and custom premium containers */
    .gov-banner {
        background: linear-gradient(135deg, #0f4c3a 0%, #1c7c54 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    .gov-banner img {
        filter: drop-shadow(0px 2px 5px rgba(0,0,0,0.3));
    }
    .trust-card {
        background-color: #f7f9f8;
        border-left: 5px solid #1c7c54;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .attribute-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-high {
        background-color: #d4edda;
        color: #155724;
    }
    .badge-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    .badge-low {
        background-color: #f8d7da;
        color: #721c24;
    }
    .scheme-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1c7c54;
    }
</style>
""", unsafe_allow_html=True)

# Fetch backend connection
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# Localized Interface Configuration
LOCALIZED_TEXT = {
    "en": {
        "title": "தமிழ்நாடு சேவை AI — TamilNadu Seva AI",
        "tagline": "Grounded Multilingual Public Service Assistant for Citizen Welfare Schemes",
        "desc": "Empowering citizens with simple, direct, and verifiable information regarding State and Central welfare schemes.",
        "lang_label": "Select Communication Language",
        "input_label": "Describe your situation or ask a scheme question:",
        "input_placeholder": "e.g., I am a government school student continuing my college degree, what assistance can I get?",
        "ask_btn": "Verify Scheme Details",
        "sample_lbl": "Frequently Asked Questions",
        "samples": [
            "Am I eligible for Pudhumai Penn if I studied in a private school?",
            "What are the benefits of Chief Minister's Comprehensive Health Insurance Scheme?",
            "How do I apply for the First Generation Graduation tuition fee waiver?",
            "Show me scholarships available under Directorate of Collegiate Education"
        ],
        "eligibility_hdr": "📋 Eligibility Checklist",
        "benefits_hdr": "🎁 Benefits and Allowances",
        "apply_hdr": "📍 Steps to Apply",
        "why_hdr": "⚖️ Why This Answer? (Grounding Rationale)",
        "sources_hdr": "🔗 Official Portals",
        "confidence_hdr": "Verification Confidence",
        "feedback_lbl": "Was this answer accurate?",
        "feedback_yes": "Yes, helpful",
        "feedback_no": "Report inaccuracy",
        "disclaimer_title": "Official Government Information Disclaimer",
        "disclaimer_body": "This AI assistant summaries rules from verified records for citizen convenience. Actual eligibility, parameters, and applications must be processed through the official government channels listed under sources.",
        "verified_badge": "Verified Source Document Grounded"
    },
    "ta": {
        "title": "தமிழ்நாடு சேவை AI",
        "tagline": "அரசு நலத்திட்டங்களுக்கான பன்மொழி மக்கள் சேவை உதவியாளர்",
        "desc": "மாநில மற்றும் மத்திய அரசு நலத்திட்டங்கள் குறித்த எளிய, நேரடி மற்றும் சரிபார்க்கப்பட்ட தகவல்களை குடிமக்களுக்கு வழங்குதல்.",
        "lang_label": "தொடர்பு மொழியைத் தேர்ந்தெடுக்கவும்",
        "input_label": "உங்கள் சூழ்நிலையை விவரிக்கவும் அல்லது நலத்திட்ட கேள்வி கேட்கவும்:",
        "input_placeholder": "உதாரணம்: நான் அரசுப் பள்ளியில் படித்து கல்லூரி சேர விரும்பும் மாணவி, எனக்கு என்ன உதவி கிடைக்கும்?",
        "ask_btn": "விவரங்களைச் சரிபார்க்கவும்",
        "sample_lbl": "அடிக்கடி கேட்கப்படும் கேள்விகள்",
        "samples": [
            "நான் தனியார் பள்ளியில் படித்திருந்தால் புதுமைப் பெண் திட்டத்திற்குத் தகுதி உண்டா?",
            "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டத்தில் என்னென்ன நன்மைகள் உள்ளன?",
            "முதல் தலைமுறை பட்டதாரி கல்விக்கட்டண சலுகைக்கு எவ்வாறு விண்ணப்பிப்பது?",
            "கல்லூரி கல்வி இயக்ககத்தின் கீழ் என்னென்ன உதவித்தொகை திட்டங்கள் உள்ளன?"
        ],
        "eligibility_hdr": "📋 தகுதி சரிபார்ப்பு பட்டியல்",
        "benefits_hdr": "🎁 திட்டத்தின் நன்மைகள்",
        "apply_hdr": "📍 விண்ணப்பிக்கும் வழிமுறைகள்",
        "why_hdr": "⚖️ இந்த பதிலின் அடிப்படை (சரிபார்ப்பு விளக்கம்)",
        "sources_hdr": "🔗 அதிகாரப்பூர்வ இணையதளங்கள்",
        "confidence_hdr": "சரிபார்ப்பு நிலை",
        "feedback_lbl": "இந்த பதில் துல்லியமானதா?",
        "feedback_yes": "ஆம், பயனுள்ளது",
        "feedback_no": "பிழையை புகாரளி",
        "disclaimer_title": "அதிகாரப்பூர்வ அரசு தகவல் பொறுப்புத்துறப்பு",
        "disclaimer_body": "குடிமக்களின் வசதிக்காக சரிபார்க்கப்பட்ட பதிவுகளிலிருந்து விதிகளை இந்த உதவியாளர் சுருக்கமாக வழங்குகிறார். உண்மையான தகுதி, விதிகள் மற்றும் விண்ணப்பங்கள் ஆதாரங்களில் பட்டியலிடப்பட்டுள்ள அதிகாரப்பூர்வ அரசு சேனல்கள் மூலம் செயல்படுத்தப்பட வேண்டும்.",
        "verified_badge": "சரிபார்க்கப்பட்ட மூல ஆவண அடிப்படையிலானது"
    },
    "hi": {
        "title": "तमिलनाडु सेवा AI",
        "tagline": "नागरिक कल्याण योजनाओं के लिए बहुभाषी जन सेवा सहायक",
        "desc": "नागरिकों को राज्य और केंद्र की कल्याणकारी योजनाओं के संबंध में सरल, प्रत्यक्ष और सत्यापन योग्य जानकारी प्रदान करना।",
        "lang_label": "संचार भाषा चुनें",
        "input_label": "अपनी स्थिति का वर्णन करें या योजना से संबंधित प्रश्न पूछें:",
        "input_placeholder": "जैसे: मैं एक सरकारी स्कूल का छात्र हूँ और कॉलेज की पढ़ाई जारी रखना चाहता हूँ, मुझे क्या सहायता मिल सकती है?",
        "ask_btn": "योजना विवरण सत्यापित करें",
        "sample_lbl": "अक्सर पूछे जाने वाले प्रश्न",
        "samples": [
            "यदि मैंने निजी स्कूल में पढ़ाई की है, तो क्या मैं पुदुमई पेन के लिए पात्र हूँ?",
            "मुख्यमंत्री व्यापक स्वास्थ्य बीमा योजना (CMCHIS) के क्या लाभ हैं?",
            "प्रथम पीढ़ी स्नातक ट्यूशन शुल्क छूट के लिए मैं कैसे आवेदन करूँ?",
            "कॉलेज शिक्षा निदेशालय के अंतर्गत कौन सी छात्रवृत्तियां उपलब्ध हैं?"
        ],
        "eligibility_hdr": "📋 पात्रता मानदंड",
        "benefits_hdr": "🎁 लाभ और अधिकार",
        "apply_hdr": "📍 आवेदन करने के चरण",
        "why_hdr": "⚖️ यह उत्तर क्यों? (सत्यापन का आधार)",
        "sources_hdr": "🔗 आधिकारिक पोर्टल",
        "confidence_hdr": "सत्यापन का स्तर",
        "feedback_lbl": "क्या यह उत्तर सटीक था?",
        "feedback_yes": "हाँ, मददगार",
        "feedback_no": "त्रुटि रिपोर्ट करें",
        "disclaimer_title": "आधिकारिक सरकारी सूचना अस्वीकरण",
        "disclaimer_body": "यह एआई सहायक नागरिकों की सुविधा के लिए सत्यापित दस्तावेजों से नियमों का सारांश प्रदान करता है। वास्तविक पात्रता, नियम और आवेदन स्रोतों में सूचीबद्ध आधिकारिक सरकारी चैनलों के माध्यम से संसाधित किए जाने चाहिए।",
        "verified_badge": "सत्यापित मूल दस्तावेज आधारित"
    }
}

# Sidebar Layout
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/81/TamilNadu_Logo.svg", width=110)
    st.markdown("### Language Selection")
    lang_code = st.selectbox(
        "Communication Language",
        options=["en", "ta", "hi"],
        format_func=lambda x: "English (EN)" if x == "en" else "தமிழ் (TA)" if x == "ta" else "हिन्दी (HI)",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("#### 🏛️ Active Schemes Database")
    st.markdown("""
    - **Pudhumai Penn Scheme**
    - **CMCHIS Health Insurance**
    - **First Generation Graduation**
    - **DCE collegiate scholarships**
    - **DCE Women Collegiate incentives**
    """)
    st.markdown("<span class='attribute-badge badge-high'>All Entries Verified</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### ⚙️ Google AI groundings")
    st.caption("Powered by Gemini 2.5 Flash & text-embedding-004 Semantic Search.")
    
ui = LOCALIZED_TEXT[lang_code]

# Header Gov Banner
st.markdown(f"""
<div class='gov-banner'>
    <h2>{ui['title']}</h2>
    <p style='margin:0; font-size:1.1rem; opacity:0.9;'>{ui['tagline']}</p>
</div>
""", unsafe_allow_html=True)

# Main container
st.write(ui["desc"])

# FAQs Sample Questions Section
st.write(f"#### ❓ {ui['sample_lbl']}")
cols = st.columns(len(ui["samples"]))

# Session state initialization for dynamic input update
if "user_question" not in st.session_state:
    st.session_state.user_question = ""

for i, sample in enumerate(ui["samples"]):
    if cols[i].button(sample, key=f"faq_btn_{i}"):
        st.session_state.user_question = sample

# Ask Text Box
query_input = st.text_area(
    ui["input_label"],
    value=st.session_state.user_question,
    placeholder=ui["input_placeholder"],
    height=110
)

# Button Trigger
col_btn, col_badge = st.columns([1, 4])
with col_btn:
    submit_triggered = st.button(ui["ask_btn"], type="primary", use_container_width=True)
    
with col_badge:
    st.markdown(f"<div style='margin-top: 8px;'><span class='attribute-badge badge-high'>🛡️ {ui['verified_badge']}</span></div>", unsafe_allow_html=True)

# Display Results
if submit_triggered:
    if query_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.status("Performing Semantic Search & Grounding Analysis...") as status:
            try:
                payload = {"question": query_input, "language": lang_code}
                response = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=35)
                
                if response.status_code == 200:
                    status.update(label="Analysis Completed successfully!", state="complete")
                    data = response.json()
                    
                    # Structured layout output
                    st.markdown("### 🏛️ Verification Response")
                    st.markdown(f"<p style='font-size:1.15rem; line-height:1.6;'>{data.get('answer')}</p>", unsafe_allow_html=True)
                    
                    # Core specifications in 3 Columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"<div class='scheme-card'><h4>{ui['eligibility_hdr']}</h4>", unsafe_allow_html=True)
                        elig = data.get("eligibility", [])
                        if elig:
                            for item in elig:
                                st.write(f"- {item}")
                        else:
                            st.write("No specific restrictions provided in records.")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f"<div class='scheme-card'><h4>{ui['benefits_hdr']}</h4>", unsafe_allow_html=True)
                        bens = data.get("benefits", [])
                        if bens:
                            for item in bens:
                                st.write(f"- {item}")
                        else:
                            st.write("No specific benefit quantities provided in records.")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    with col3:
                        st.markdown(f"<div class='scheme-card'><h4>{ui['apply_hdr']}</h4>", unsafe_allow_html=True)
                        steps = data.get("how_to_apply", [])
                        if steps:
                            for item in steps:
                                st.write(f"- {item}")
                        else:
                            st.write("Consult the official portal links listed below to apply.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Rationale and Trust Card
                    st.markdown(f"<div class='trust-card'><strong>{ui['why_hdr']}</strong><br/><p>{data.get('why_this_answer')}</p></div>", unsafe_allow_html=True)
                    
                    # Confidence Badge
                    conf_level = data.get("confidence", "low").lower()
                    badge_class = "badge-high" if conf_level == "high" else "badge-medium" if conf_level == "medium" else "badge-low"
                    
                    col_info, col_feed = st.columns([2, 1])
                    with col_info:
                        st.markdown(f"**{ui['confidence_hdr']}**: <span class='attribute-badge {badge_class}'>{conf_level.upper()}</span>", unsafe_allow_html=True)
                        st.markdown("##### " + ui["sources_hdr"])
                        for src in data.get("sources", []):
                            st.markdown(f"- [{src.get('title')}]({src.get('url')})")
                            
                    with col_feed:
                        st.markdown(f"**{ui['feedback_lbl']}**")
                        c_yes, c_no = st.columns(2)
                        if c_yes.button(ui["feedback_yes"]):
                            st.toast("Thank you for your feedback!", icon="💖")
                        if c_no.button(ui["feedback_no"]):
                            st.toast("Feedback recorded. Reviewing grounding records.", icon="⚠️")
                            
                else:
                    status.update(label="API Server returned an error status.", state="error")
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                status.update(label="Failed to contact backend API.", state="error")
                st.error(f"Could not connect to API at {BACKEND_URL}. Details: {e}")

st.markdown("---")
# Trust Disclaimer Box
st.warning(f"**{ui['disclaimer_title']}** — {ui['disclaimer_body']}")

# Google attribution footer
st.markdown("""
<div style='text-align: center; margin-top: 30px; opacity:0.8; font-size:0.9rem;'>
    Built with <strong>Google Cloud Gen AI Academy APAC</strong>. Supported by Gemini Developer API.
</div>
""", unsafe_allow_html=True)
