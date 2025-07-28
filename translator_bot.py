import streamlit as st
import pyttsx3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# -- Gemini API Key (provided by user) --
GOOGLE_API_KEY = "AIzaSyA02m9uCQYMlftxAsejMTOas8wQCc2DYHY"

# -- Load Gemini 1.5 Flash Model (Free Tier) --
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # ✅ This model works with MakerSuite key
    google_api_key=GOOGLE_API_KEY
)

# -- Text-to-Speech Function (Offline) --
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# -- Streamlit UI Setup --
st.set_page_config(page_title="🌍 Language Translator with Voice", layout="centered")
st.title("🌐 Gemini Language Translator Bot with Voice 🎤")

# -- User Input Fields --
text_to_translate = st.text_area("Enter text to translate:", height=100)
target_language = st.selectbox("Select target language:", ["Urdu", "Hindi", "English", "French", "Arabic", "Chinese"])

# -- Prompt Template for Gemini --
prompt = ChatPromptTemplate.from_template(
    "Translate the following text to {language}:\n\n{text}"
)

# -- LangChain Chain Setup --
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# -- Translate + Speak Button Logic --
if st.button("Translate and Speak") and text_to_translate:
    with st.spinner("Translating..."):
        try:
            result = chain.invoke({
                "language": target_language,
                "text": text_to_translate
            })
            st.success("✅ Translation:")
            st.write(result)

            # 🔊 Speak the translated result
            speak_text(result)

        except Exception as e:
            st.error(f"❌ Error: {e}")
