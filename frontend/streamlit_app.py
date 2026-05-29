import streamlit as st
import requests
import os

# Streamlit App Configurations
st.set_page_config(
    page_title="TamilNadu Seva AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL Setup
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# Localized UI Content
LOCALIZED_TEXT = {
    "en": {
        "title": "🏛️ TamilNadu Seva AI",
        "tagline": "Your Trustworthy Multilingual Assistant for State & Central Welfare Schemes",
        "desc": "Ask queries about welfare schemes in Tamil Nadu in English, Tamil, or Hindi.",
        "lang_label": "Choose Language / மொழியைத் தேர்ந்தெடுக்கவும் / भाषा चुनें:",
        "input_label": "Enter your question here:",
        "input_placeholder": "e.g., Who is eligible for Pudhumai Penn scheme?",
        "ask_btn": "Ask Assistant",
        "sample_lbl": "Or click on a sample question below:",
        "samples": [
            "Am I eligible for Pudhumai Penn if I studied in a private school?",
            "What are the benefits of CMCHIS health insurance?",
            "How do I apply for the First Generation Graduation fee waiver?",
            "What schemes are available for collegiate scholarships?"
        ],
        "eligibility_hdr": "✅ Eligibility Criteria",
        "benefits_hdr": "🎁 Benefits & Entitlements",
        "apply_hdr": "ℹ️ How to Apply",
        "why_hdr": "🔍 Why This Answer?",
        "sources_hdr": "🔗 Official Sources",
        "confidence_hdr": "💡 Confidence Level",
        "error_msg": "Could not connect to TamilNadu Seva AI API. Please make sure the backend is running.",
        "disclaimer_title": "⚠️ Official Verification Disclaimer",
        "disclaimer_body": "This assistant summarizes official information for convenience. Final eligibility and benefits should be verified on the official government website."
    },
    "ta": {
        "title": "🏛️ தமிழ்நாடு சேவா AI",
        "tagline": "மாநில மற்றும் மத்திய அரசு நலத்திட்டங்களுக்கான உங்கள் நம்பகமான பன்மொழி உதவியாளர்",
        "desc": "தமிழ்நாட்டின் நலத்திட்டங்கள் பற்றிய கேள்விகளை ஆங்கிலம், தமிழ் அல்லது இந்தியில் கேட்கலாம்.",
        "lang_label": "மொழியைத் தேர்ந்தெடுக்கவும்:",
        "input_label": "உங்கள் கேள்வியை இங்கே உள்ளிடவும்:",
        "input_placeholder": "உதாரணம்: புதுமைப் பெண் திட்டத்திற்கு யார் தகுதியானவர்கள்?",
        "ask_btn": "கேள்வி கேள்",
        "sample_lbl": "அல்லது கீழே உள்ள மாதிரி கேள்வியைக் கிளிக் செய்யவும்:",
        "samples": [
            "நான் தனியார் பள்ளியில் படித்திருந்தால் புதுமைப் பெண் திட்டத்திற்குத் தகுதி உண்டா?",
            "முதலமைச்சரின் காப்பீட்டுத் திட்டத்தில் என்னென்ன நன்மைகள் உள்ளன?",
            "முதல் தலைமுறை பட்டதாரி கட்டணச் சலுகைக்கு எவ்வாறு விண்ணப்பிப்பது?",
            "கல்லூரி படிப்பிற்கான உதவித்தொகை திட்டங்கள் என்னென்ன உள்ளன?"
        ],
        "eligibility_hdr": "✅ தகுதி வரம்புகள்",
        "benefits_hdr": "🎁 திட்டத்தின் பயன்கள்",
        "apply_hdr": "ℹ️ விண்ணப்பிக்கும் முறை",
        "why_hdr": "🔍 இந்த பதிலின் அடிப்படை?",
        "sources_hdr": "🔗 அதிகாரப்பூர்வ ஆதாரங்கள்",
        "confidence_hdr": "💡 நம்பிக்கை நிலை",
        "error_msg": "தமிழ்நாடு சேவா AI API உடன் இணைக்க முடியவில்லை. பின்விளைவு சேவை இயங்குவதை உறுதிசெய்யவும்.",
        "disclaimer_title": "⚠️ அதிகாரப்பூர்வ சரிபார்ப்பு பொறுப்புத் துறப்பு",
        "disclaimer_body": "இந்த உதவியாளர் உங்கள் வசதிக்காக அதிகாரப்பூர்வ தகவல்களைச் சுருக்கமாக வழங்குகிறார். இறுதி தகுதி மற்றும் நன்மைகளை அதிகாரப்பூர்வ அரசு இணையதளத்தில் சரிபார்க்க வேண்டும்."
    },
    "hi": {
        "title": "🏛️ तमिलनाडु सेवा AI",
        "tagline": "राज्य और केंद्रीय कल्याण योजनाओं के लिए आपका विश्वसनीय बहुभाषी सहायक",
        "desc": "तमिलनाडु की कल्याणकारी योजनाओं के बारे में अंग्रेजी, तमिल या हिंदी में प्रश्न पूछें।",
        "lang_label": "भाषा चुनें:",
        "input_label": "अपना प्रश्न यहाँ दर्ज करें:",
        "input_placeholder": "जैसे: पुदुमई पेन योजना के लिए कौन पात्र है?",
        "ask_btn": "सहायक से पूछें",
        "sample_lbl": "या नीचे दिए गए किसी नमूना प्रश्न पर क्लिक करें:",
        "samples": [
            "यदि मैंने निजी स्कूल में पढ़ाई की है, तो क्या मैं पुदुमई पेन के लिए पात्र हूँ?",
            "सीएमसीएचआईएस (CMCHIS) स्वास्थ्य बीमा के क्या लाभ हैं?",
            "प्रथम पीढ़ी स्नातक शुल्क छूट के लिए कैसे आवेदन करें?",
            "कॉलेज छात्रवृत्ति के लिए कौन सी योजनाएं उपलब्ध हैं?"
        ],
        "eligibility_hdr": "✅ पात्रता मानदंड",
        "benefits_hdr": "🎁 लाभ और अधिकार",
        "apply_hdr": "ℹ️ आवेदन कैसे करें",
        "why_hdr": "🔍 यह उत्तर क्यों?",
        "sources_hdr": "🔗 आधिकारिक स्रोत",
        "confidence_hdr": "💡 आत्मविश्वास का स्तर",
        "error_msg": "तमिलनाडु सेवा AI API से कनेक्ट नहीं हो सका। कृपया सुनिश्चित करें कि बैकएंड चल रहा है।",
        "disclaimer_title": "⚠️ आधिकारिक सत्यापन अस्वीकरण",
        "disclaimer_body": "यह सहायक सुविधा के लिए आधिकारिक जानकारी का सारांश प्रस्तुत करता है। अंतिम पात्रता और लाभों की पुष्टि आधिकारिक सरकारी वेबसाइट पर की जानी चाहिए।"
    }
}

# Sidebar settings
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/81/TamilNadu_Logo.svg", width=120)
    st.markdown("---")
    # Language dropdown
    lang_code = st.selectbox(
        "Preferred Language / மொழி / भाषा",
        options=["en", "ta", "hi"],
        format_func=lambda x: "English" if x == "en" else "தமிழ் (Tamil)" if x == "ta" else "हिन्दी (Hindi)"
    )
    
    st.markdown("### Supported Schemes:")
    st.markdown("""
    *   **Pudhumai Penn Scheme**
    *   **CMCHIS Health Insurance**
    *   **First Gen Graduation Waiver**
    *   **Collegiate Scholarships**
    *   **Women Collegiate Welfare**
    """)
    
    st.markdown("---")
    st.caption("Google Cloud Gen AI Academy APAC — Meet the Builders Submission")

ui = LOCALIZED_TEXT[lang_code]

# Layout and Headers
st.title(ui["title"])
st.subheader(ui["tagline"])
st.write(ui["desc"])

# Initialize session state for text input if not present
if "user_question" not in st.session_state:
    st.session_state.user_question = ""

# Handle Sample Question Clicks
st.write(ui["sample_lbl"])
cols = st.columns(len(ui["samples"]))
for i, sample in enumerate(ui["samples"]):
    if cols[i].button(sample, key=f"sample_{i}"):
        st.session_state.user_question = sample

# Question Input Area
user_query = st.text_area(ui["input_label"], value=st.session_state.user_question, placeholder=ui["input_placeholder"], height=100)

# Submit button
if st.button(ui["ask_btn"], type="primary"):
    if user_query.strip() == "":
        st.warning("Please enter a question / தயவுசெய்து ஒரு கேள்வியை உள்ளிடவும் / कृपया एक प्रश्न दर्ज करें।")
    else:
        with st.spinner("Analyzing verified government sources..." if lang_code == "en" else "அதிகாரப்பூர்வ ஆதாரங்களை பகுப்பாய்வு செய்கிறது..." if lang_code == "ta" else "आधिकारिक स्रोतों का विश्लेषण किया जा रहा है..."):
            try:
                # Call FastAPI backend
                payload = {"question": user_query, "language": lang_code}
                response = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display Answer
                    st.markdown("### 🏛️ Answer / பதில் / उत्तर")
                    st.write(data.get("answer"))
                    
                    # Columns for structured attributes
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"#### {ui['eligibility_hdr']}")
                        elig = data.get("eligibility", [])
                        if elig:
                            for item in elig:
                                st.write(f"- {item}")
                        else:
                            st.write("N/A")
                            
                    with col2:
                        st.markdown(f"#### {ui['benefits_hdr']}")
                        bens = data.get("benefits", [])
                        if bens:
                            for item in bens:
                                st.write(f"- {item}")
                        else:
                            st.write("N/A")
                            
                    with col3:
                        st.markdown(f"#### {ui['apply_hdr']}")
                        steps = data.get("how_to_apply", [])
                        if steps:
                            for item in steps:
                                st.write(f"- {item}")
                        else:
                            st.write("N/A")
                            
                    st.markdown("---")
                    
                    # Rationale and Trust features
                    col_left, col_right = st.columns([2, 1])
                    with col_left:
                        st.info(f"**{ui['why_hdr']}**\n\n{data.get('why_this_answer')}")
                        
                    with col_right:
                        st.success(f"**{ui['confidence_hdr']}**: {data.get('confidence', '').upper()}")
                        
                    # Sources panel
                    st.markdown(f"### {ui['sources_hdr']}")
                    sources = data.get("sources", [])
                    if sources:
                        for src in sources:
                            st.markdown(f"- **{src.get('title')}**: [{src.get('url')}]({src.get('url')})")
                    else:
                        st.write("No direct source matched.")
                        
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException:
                st.error(ui["error_msg"])

st.markdown("---")
# Trust / Disclaimer Box
st.warning(f"**{ui['disclaimer_title']}**\n\n{ui['disclaimer_body']}")
