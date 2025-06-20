#!/usr/bin/env python3
"""
🎓 Educational Subject Demo
Demonstrates how ANY educator can use this platform for their subject
"""

import streamlit as st

def main():
    st.set_page_config(
        page_title="Educational Video Generator - All Subjects Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Educational Video Generator - EVERY SUBJECT SUPPORTED")
    
    st.markdown("""
    ## 🌟 Perfect for ALL Educators
    
    This platform generates professional educational videos for **EVERY academic subject and topic**.
    Whether you teach in elementary school, university, or professional training, we've got you covered!
    """)
    
    # Create columns for different subject categories
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔬 **STEM Fields**
        - **Mathematics**: All levels from basic arithmetic to advanced calculus
        - **Physics**: Classical mechanics to quantum physics
        - **Chemistry**: General, organic, inorganic, physical chemistry
        - **Biology**: Cell biology, genetics, ecology, human anatomy
        - **Computer Science**: Programming, AI/ML, cybersecurity
        - **Engineering**: All disciplines - civil, mechanical, electrical
        - **Data Science**: Statistics, analytics, visualization
        - **Environmental Science**: Climate, ecology, sustainability
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 **Languages & Humanities**
        - **World Languages**: English, Spanish, French, German, Chinese, Arabic, Japanese, Russian, Hindi, and 50+ more
        - **Literature**: Classic and modern works from all cultures
        - **History**: Ancient civilizations to modern times
        - **Geography**: Physical, human, and cultural geography
        - **Philosophy**: Western, Eastern, and comparative philosophy
        - **Psychology**: All branches and applications
        - **Sociology**: Social theory and cultural studies
        - **Anthropology**: Cultural and archaeological studies
        """)
    
    with col3:
        st.markdown("""
        ### 🎨 **Arts & Professional**
        - **Visual Arts**: Drawing, painting, digital art, photography
        - **Music**: Theory, instruments, composition, history
        - **Theater & Film**: Acting, directing, production
        - **Creative Writing**: Fiction, poetry, screenwriting
        - **Business**: Management, marketing, finance, strategy
        - **Healthcare**: Medical education, nursing, public health
        - **Law**: All legal specializations and systems
        - **Education**: Teaching methods and curriculum design
        """)
    
    st.markdown("---")
    
    # Special focus on spiritual and cultural education
    st.markdown("""
    ## 🙏 **Spiritual & Cultural Education**
    
    We especially support educators in spiritual and cultural subjects:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📿 **World Religions & Spirituality**
        - **Christianity**: Biblical studies, theology, church history
        - **Islam**: Quranic studies, Islamic history, jurisprudence
        - **Judaism**: Torah studies, Jewish history, rabbinical literature
        - **Buddhism**: Buddhist philosophy, meditation, sangha teachings
        - **Hinduism**: Vedic literature, yoga philosophy, Sanskrit texts
        - **Sikhism**: Guru Granth Sahib, Sikh history, philosophy
        - **Indigenous Spiritualities**: Native traditions worldwide
        - **Comparative Religion**: Inter-faith studies and dialogue
        """)
    
    with col2:
        st.markdown("""
        ### 🕉️ **Eastern Philosophy & Practices**
        - **Sanskrit Studies**: Vedic texts, mantras, slokas
        - **Yoga Philosophy**: Classical texts, modern applications
        - **Meditation**: Various traditions and techniques
        - **Ayurveda**: Traditional medicine and holistic health
        - **Martial Arts Philosophy**: Spiritual aspects of practice
        - **Eastern Philosophy**: Confucianism, Taoism, Zen
        - **Mindfulness**: Buddhist and secular approaches
        - **Energy Healing**: Traditional and modern modalities
        """)
    
    st.markdown("---")
    
    # Usage examples
    st.markdown("""
    ## 🚀 **How Educators Use This Platform**
    
    ### 👩‍🏫 **Elementary School Teachers**
    > "I create engaging math and science videos for my 4th graders. The visual explanations help them understand complex concepts!"
    
    ### 👨‍🎓 **University Professors**
    > "Perfect for my advanced physics courses. I can create 40-minute lectures with detailed explanations and upload directly to our LMS."
    
    ### 🕉️ **Spiritual Teachers**
    > "I use this to create beautiful videos explaining Sanskrit mantras and Vedic wisdom for my global students."
    
    ### 🌍 **Language Instructors**
    > "Amazing for creating immersive language lessons. I've made videos for Spanish, French, and Mandarin classes."
    
    ### 💼 **Corporate Trainers**
    > "Essential for creating professional development content. Our employees love the engaging format!"
    """)
    
    st.markdown("---")
    
    # Call to action
    st.markdown("""
    ## 🎯 **Ready to Transform Your Teaching?**
    
    ### ✨ **What You Get:**
    - **Professional Quality**: HD videos with smooth transitions and clear audio
    - **Any Duration**: 10-40 minute videos (or custom length)
    - **All Languages**: Create content in 50+ languages
    - **Auto Upload**: Direct publishing to YouTube with SEO optimization
    - **Multiple Formats**: Works on all devices and platforms
    - **Free to Use**: Open source and community-driven
    
    ### 🚀 **Get Started in 3 Steps:**
    1. **Choose Your Subject**: Any topic from any field
    2. **Customize Settings**: Duration, level, language, style
    3. **Generate & Upload**: AI creates your video and uploads to YouTube automatically
    
    **Start creating exceptional educational content today!**
    """)
    
    # Demo button
    if st.button("🎬 Try the Video Generator Now", type="primary"):
        st.success("🎉 Redirecting to the main video generator interface...")
        st.markdown("**[Click here to open the main app](http://localhost:8501)**")

if __name__ == "__main__":
    main()
