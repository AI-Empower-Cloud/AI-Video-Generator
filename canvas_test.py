#!/usr/bin/env python3
"""
Canvas Editor Test
"""

print("🎬 Testing Canvas Editor...")

try:
    import sys
    sys.path.insert(0, 'modules')
    
    from canvas_editor import CanvasEditor, CANVAS_TEMPLATES
    print("✅ Import successful")
    
    # Test basic functionality
    editor = CanvasEditor("test_projects")
    print("✅ Editor initialized")
    
    # Create project
    project = editor.create_project("Test Video")
    print(f"✅ Project created: {project.name}")
    
    # Add text
    text_elem = editor.add_text_element(
        project.id, "Hello Canvas!", 100, 100, font_size=32
    )
    print(f"✅ Text added: {text_elem.properties['text']}")
    
    # Get timeline
    timeline = editor.get_project_timeline(project.id)
    print(f"✅ Timeline: {len(timeline['tracks'])} tracks")
    
    # Templates
    print(f"✅ Templates: {list(CANVAS_TEMPLATES.keys())}")
    
    print("\n🎉 CANVAS EDITOR TEST PASSED!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
import os
import shutil
if os.path.exists("test_projects"):
    shutil.rmtree("test_projects")
    print("🧹 Cleaned up test files")
