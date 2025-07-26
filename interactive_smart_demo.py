#!/usr/bin/env python3
"""
🎬 Interactive Smart Workflow Demo
Shows how to use the advanced Canvas Editor features
"""

from modules.canvas_editor import CanvasEditor

def interactive_demo():
    """Interactive demonstration of smart workflow features"""
    print("🎬 SMART VIDEO WORKFLOW DEMO")
    print("=" * 40)
    
    # Initialize the smart workflow editor
    editor = CanvasEditor(projects_dir="smart_workflow_projects")
    
    print(f"✅ Loaded Canvas Editor with Smart Workflow")
    print(f"📊 Available: {len(editor.tags)} tags, {len(editor.use_cases)} use cases")
    
    # Show available tags by category
    print(f"\n🏷️  Available Tag Categories:")
    categories = {}
    for tag in editor.tags.values():
        if tag.category not in categories:
            categories[tag.category] = []
        categories[tag.category].append(tag.name)
    
    for category, tag_names in sorted(categories.items()):
        print(f"   {category.title()}: {len(tag_names)} tags")
    
    # Show use cases
    print(f"\n🎯 Available Use Cases:")
    for i, use_case in enumerate(list(editor.use_cases.values())[:5], 1):
        print(f"   {i}. {use_case.name}")
        print(f"      Category: {use_case.category} | Difficulty: {use_case.difficulty}")
    
    # Create a new project
    print(f"\n📁 Creating New Project...")
    project = editor.create_project(
        name="Demo Marketing Video",
        width=1080,
        height=1920,  # Vertical for social media
        duration=30.0
    )
    print(f"   ✅ Created: {project.name}")
    
    # Apply smart tags
    demo_tags = ["Marketing", "Social Media", "Gen Z", "TikTok"]
    success = editor.assign_tags_to_project(project.id, demo_tags)
    print(f"   🏷️  Applied tags: {', '.join(demo_tags)}")
    
    # Get smart recommendations
    recommendations = editor.get_recommended_use_cases(project.tags)
    print(f"\n💡 Smart Recommendations for your project:")
    
    if recommendations:
        for i, use_case in enumerate(recommendations[:3], 1):
            matching_tags = set(project.tags) & set(use_case.tags)
            match_score = len(matching_tags) / len(use_case.tags) * 100
            print(f"   {i}. {use_case.name}")
            print(f"      Match: {match_score:.0f}% | Time: {use_case.estimated_time}")
            print(f"      Matching tags: {', '.join(matching_tags)}")
        
        # Apply best recommendation
        best_use_case = recommendations[0]
        success = editor.apply_use_case_to_project(project.id, best_use_case.id)
        if success:
            print(f"\n✅ Applied use case: {best_use_case.name}")
            print(f"📋 Updated project tags: {', '.join(project.tags)}")
    
    # Add elements with smart tagging
    print(f"\n🎨 Adding Smart Elements...")
    
    # Add a hook element
    hook = editor.add_text_element(
        project.id,
        "Stop Scrolling! 🔥",
        x=100, y=200,
        font_size=36,
        color="#FF0050"
    )
    editor.assign_tags_to_element(project.id, hook.id, ["Hook", "Gen Z", "Attention"])
    print(f"   ✅ Added hook element with smart tags")
    
    # Add main content
    content = editor.add_text_element(
        project.id,
        "Amazing Product Feature",
        x=100, y=400,
        font_size=28,
        color="#FFFFFF"
    )
    editor.assign_tags_to_element(project.id, content.id, ["Content", "Marketing"])
    print(f"   ✅ Added content element with smart tags")
    
    # Show project analytics
    print(f"\n📈 Project Analytics:")
    analytics = editor.get_tag_analytics()
    print(f"   Total projects: {len(editor.projects)}")
    print(f"   Most used tags: {analytics['most_used_tags'][:3] if analytics['most_used_tags'] else 'None yet'}")
    
    # Search demonstration
    print(f"\n🔍 Smart Search Demo:")
    marketing_projects = editor.search_projects_by_tags(["Marketing"])
    social_projects = editor.search_projects_by_tags(["Social Media"])
    print(f"   Projects tagged 'Marketing': {len(marketing_projects)}")
    print(f"   Projects tagged 'Social Media': {len(social_projects)}")
    
    print(f"\n🎯 Demo Complete!")
    print(f"Your Canvas Editor now has:")
    print(f"   • Smart tagging system with {len(editor.tags)} tags")
    print(f"   • {len(editor.use_cases)} professional use cases")
    print(f"   • Intelligent recommendations")
    print(f"   • Organized project workflows")
    print(f"   • Advanced analytics and insights")
    
    return editor, project

if __name__ == "__main__":
    try:
        editor, project = interactive_demo()
        print(f"\n✅ Smart workflow system ready for professional video production!")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
