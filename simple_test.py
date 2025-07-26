#!/usr/bin/env python3
"""
Simple test for tags and use cases
"""

print("Starting test...")

try:
    print("Importing modules...")
    from modules.canvas_editor import CanvasEditor, Tag, UseCase
    print("Import successful!")
    
    print("Creating editor...")
    editor = CanvasEditor(projects_dir="test_canvas_projects")
    print("Editor created!")
    
    print(f"Tags count: {len(editor.tags)}")
    print(f"Use cases count: {len(editor.use_cases)}")
    
    # Test tag creation  
    print("Creating a test tag...")
    tag = editor.create_tag("Test Tag", "#FF0000", "test", "A test tag")
    print(f"Tag created: {tag.name}")
    
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
