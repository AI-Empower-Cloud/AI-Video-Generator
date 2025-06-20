#!/bin/bash

# 🎓 Universal Education Video Creator
# Quick setup and run script for creating educational videos for ALL SUBJECTS

echo "🎓 Universal Educational Video Generator"
echo "========================================"
echo ""

# Function to show available subjects
show_subjects() {
    echo "📚 Available Subjects:"
    echo "   1. Mathematics"
    echo "   2. Science (Physics, Chemistry, Biology)"
    echo "   3. History"
    echo "   4. Language Arts & Literature"
    echo "   5. Computer Science"
    echo "   6. Sanskrit/Spiritual"
    echo "   7. Psychology"
    echo "   8. Economics"
    echo "   9. Geography"
    echo "  10. Art & Music"
    echo "  11. Philosophy"
    echo "  12. Engineering"
    echo "  13. Medicine"
    echo "  14. Business"
    echo "  15. Law"
    echo "  16. Environmental Science"
    echo ""
}bash

# 🎓 Educational Video Creator Launcher
# Quick script to run the educational video generator

echo "🎓 Educational Video Creator"
echo "============================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q streamlit

echo ""
echo "Choose your option:"
echo "1. 🌐 Launch Web Interface (Streamlit)"
echo "2. 🎬 Create Gayatri Mantra Video"
echo "3. 📚 Batch Create Sanskrit Series"
echo "4. 🎓 Batch Create Educational Series"
echo "5. ⚙️ Run Custom Script"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🌐 Starting Educational Video Creator Web Interface..."
        streamlit run educational_app.py --server.port 8504 --server.address 0.0.0.0
        ;;
    2)
        echo "🕉️ Creating Gayatri Mantra teaching video..."
        python3 -c "
from educational_video_generator import create_gayatri_mantra_video
video_path, metadata = create_gayatri_mantra_video()
print(f'✅ Video created: {video_path}')
print(f'📝 Title: {metadata[\"title\"]}')
"
        ;;
    3)
        echo "📚 Creating Sanskrit Learning Series..."
        python3 batch_educational_creator.py --series sanskrit
        ;;
    4)
        echo "🎓 Creating Educational Content Series..."
        python3 batch_educational_creator.py --series educational
        ;;
    5)
        echo "⚙️ Running custom educational video script..."
        python3 educational_video_generator.py
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Educational Video Creator - Complete!"
echo "📚 Documentation: https://ai-empower-cloud.github.io/AI-Video-Generator/"
