import streamlit as st
import time
from difflib import SequenceMatcher
import random
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Typing Speed Tester", layout="wide")

# List of paragraphs for typing tests
paragraphs = [
    """The technology industry continues to evolve at an unprecedented pace, transforming how we live, work, and communicate. 
    From artificial intelligence and machine learning to quantum computing and blockchain, innovations are reshaping our world. 
    Companies must adapt quickly to stay competitive in this rapidly changing landscape.""",
    
    """Climate change represents one of the most significant challenges facing humanity today. 
    Scientists worldwide are working tirelessly to understand its impacts and develop solutions. 
    Renewable energy, sustainable practices, and environmental conservation have become crucial priorities.""",
    
    """The human brain is perhaps the most complex structure in the known universe. 
    Neuroscientists are constantly discovering new insights about how we think, learn, and remember. 
    Understanding brain function has implications for education, medicine, and artificial intelligence."""
]

st.title("⌨️ Advanced Typing Speed & Mistake Analyzer")

# Session state initialization
if 'test_history' not in st.session_state:
    st.session_state.test_history = []
if 'current_paragraph' not in st.session_state:
    st.session_state.current_paragraph = random.choice(paragraphs)
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Sidebar for test selection
with st.sidebar:
    st.header("🎯 Test Options")
    if st.button("New Random Paragraph"):
        st.session_state.current_paragraph = random.choice(paragraphs)
        st.session_state.start_time = None

# Show current paragraph
st.markdown("### Type this paragraph:")
st.code(st.session_state.current_paragraph)

# Typing input and timing
if st.button("Start Typing"):
    st.session_state.start_time = time.time()

typed_text = st.text_area("Start typing here...", height=200)

if st.button("Submit"):
    if not st.session_state.start_time:
        st.warning("Click 'Start Typing' first!")
    else:
        end_time = time.time()
        total_time = round(end_time - st.session_state.start_time, 2)

        # Calculate metrics
        word_count = len(typed_text.split())
        wpm = round(word_count / (total_time / 60), 2)
        matcher = SequenceMatcher(None, st.session_state.current_paragraph, typed_text)
        accuracy = round(matcher.ratio() * 100, 2)
        mistakes = sum(1 for a, b in zip(st.session_state.current_paragraph, typed_text) 
                      if a != b) + abs(len(st.session_state.current_paragraph) - len(typed_text))

        # Store results
        st.session_state.test_history.append({
            'wpm': wpm,
            'accuracy': accuracy,
            'mistakes': mistakes,
            'time': total_time
        })

        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Current Results")
            st.write(f"⏱️ Time Taken: {total_time} seconds")
            st.write(f"🚀 Typing Speed: {wpm} WPM")
            st.write(f"✅ Accuracy: {accuracy}%")
            st.write(f"❌ Mistakes: {mistakes}")

        with col2:
            # Speed gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=wpm,
                title={'text': "Words Per Minute"},
                gauge={'axis': {'range': [0, 150]},
                       'steps': [
                           {'range': [0, 50], 'color': "lightgray"},
                           {'range': [50, 80], 'color': "gray"},
                           {'range': [80, 150], 'color': "darkgray"}],
                       'threshold': {
                           'line': {'color': "red", 'width': 4},
                           'thickness': 0.75,
                           'value': wpm}}))
            st.plotly_chart(fig)

        # Historical performance
        if len(st.session_state.test_history) > 1:
            st.subheader("📈 Performance History")
            
            # Create performance trend charts
            fig = px.line(
                st.session_state.test_history,
                y=['wpm', 'accuracy'],
                title="Speed and Accuracy Trends",
                labels={'index': 'Test Number', 'value': 'Score', 'variable': 'Metric'}
            )
            st.plotly_chart(fig)

        st.session_state.start_time = None
