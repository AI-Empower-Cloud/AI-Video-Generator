#!/usr/bin/env python3
"""
🎬 SMART VIDEO CREATION WORKFLOW DEMO
====================================

Demonstrates advanced Canvas Editor features:
- Custom tags and use cases creation
- Efficient project organization
- Smart recommendations system
- Workflow optimization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.canvas_editor import CanvasEditor
import json
from datetime import datetime

class SmartWorkflowDemo:
    def __init__(self):
        self.editor = CanvasEditor(projects_dir="smart_workflow_projects")
        self.projects = []
        
    def create_custom_tags(self):
        """Create custom tags for specific video production needs"""
        print("🏷️  Creating Custom Tags")
        print("=" * 40)
        
        custom_tags = [
            # Industry-specific tags
            {"name": "Healthcare", "color": "#00BCD4", "category": "industry", "description": "Healthcare and medical content"},
            {"name": "Tech Startup", "color": "#9C27B0", "category": "industry", "description": "Technology startup content"},
            {"name": "E-commerce", "color": "#FF5722", "category": "industry", "description": "Online retail and shopping"},
            {"name": "Real Estate", "color": "#795548", "category": "industry", "description": "Property and real estate content"},
            
            # Production complexity
            {"name": "Quick & Simple", "color": "#4CAF50", "category": "complexity", "description": "Simple, fast production"},
            {"name": "Professional", "color": "#FF9800", "category": "complexity", "description": "High-end professional production"},
            {"name": "Experimental", "color": "#E91E63", "category": "complexity", "description": "Creative experimental content"},
            
            # Target audience
            {"name": "Gen Z", "color": "#FFEB3B", "category": "audience", "description": "Content for Generation Z"},
            {"name": "Millennials", "color": "#8BC34A", "category": "audience", "description": "Content for Millennials"},
            {"name": "B2B", "color": "#2196F3", "category": "audience", "description": "Business-to-business content"},
            {"name": "Executives", "color": "#607D8B", "category": "audience", "description": "C-level executive audience"},
            
            # Platform specific
            {"name": "TikTok", "color": "#FF0050", "category": "platform", "description": "TikTok optimized content"},
            {"name": "Instagram Reels", "color": "#E4405F", "category": "platform", "description": "Instagram Reels format"},
            {"name": "LinkedIn", "color": "#0077B5", "category": "platform", "description": "LinkedIn professional content"},
            {"name": "YouTube Shorts", "color": "#FF0000", "category": "platform", "description": "YouTube Shorts format"},
        ]
        
        created_tags = []
        for tag_data in custom_tags:
            tag = self.editor.create_tag(
                name=tag_data["name"],
                color=tag_data["color"],
                category=tag_data["category"],
                description=tag_data["description"]
            )
            created_tags.append(tag)
            print(f"   ✅ Created: {tag.name} ({tag.category}) - {tag.color}")
        
        print(f"\n🎯 Total custom tags created: {len(created_tags)}")
        return created_tags
    
    def create_custom_use_cases(self):
        """Create custom use cases for specific scenarios"""
        print("\n🎯 Creating Custom Use Cases")
        print("=" * 40)
        
        custom_use_cases = [
            {
                "name": "Tech Product Launch",
                "description": "High-impact video for launching new technology products",
                "category": "marketing",
                "tags": ["Tech Startup", "Professional", "B2B", "YouTube"],
                "templates": ["corporate_presentation"],
                "workflow_steps": [
                    {"step": "Market Research", "description": "Analyze target market and competitors"},
                    {"step": "Product Demo Script", "description": "Create compelling product demonstration"},
                    {"step": "Visual Identity", "description": "Develop consistent brand visuals"},
                    {"step": "Professional Recording", "description": "High-quality video and audio capture"},
                    {"step": "Post-Production", "description": "Advanced editing with motion graphics"},
                    {"step": "A/B Testing", "description": "Test different versions for optimization"},
                ],
                "estimated_time": "6-8 hours",
                "difficulty": "advanced",
                "assets_needed": ["Product footage", "Brand assets", "Professional voiceover", "Music", "Graphics"],
                "output_specs": {"resolution": "4K", "fps": 60, "format": "MP4", "duration": "2-3 minutes"}
            },
            {
                "name": "Healthcare Education Series",
                "description": "Educational content for healthcare professionals and patients",
                "category": "education",
                "tags": ["Healthcare", "Educational", "Professional", "Long Form"],
                "templates": ["educational_video"],
                "workflow_steps": [
                    {"step": "Medical Review", "description": "Ensure medical accuracy and compliance"},
                    {"step": "Simplified Scripting", "description": "Complex medical concepts in simple terms"},
                    {"step": "Visual Aids", "description": "Charts, diagrams, and illustrations"},
                    {"step": "Expert Interviews", "description": "Include healthcare professional insights"},
                    {"step": "Accessibility", "description": "Add captions and multiple language support"},
                ],
                "estimated_time": "8-12 hours",
                "difficulty": "advanced",
                "assets_needed": ["Medical diagrams", "Expert interviews", "Stock footage", "Compliance materials"],
                "output_specs": {"resolution": "1920x1080", "fps": 30, "format": "MP4", "duration": "10-15 minutes"}
            },
            {
                "name": "Viral Social Media Campaign",
                "description": "Create engaging short-form content designed to go viral",
                "category": "marketing",
                "tags": ["Social Media", "Gen Z", "TikTok", "Instagram Reels", "Quick & Simple"],
                "templates": ["social_media_post"],
                "workflow_steps": [
                    {"step": "Trend Analysis", "description": "Research current viral trends and hashtags"},
                    {"step": "Hook Creation", "description": "Design attention-grabbing opening seconds"},
                    {"step": "Quick Production", "description": "Fast, mobile-friendly content creation"},
                    {"step": "Platform Optimization", "description": "Adapt for different social platforms"},
                    {"step": "Engagement Strategy", "description": "Plan for comments and interactions"},
                ],
                "estimated_time": "3-4 hours",
                "difficulty": "intermediate",
                "assets_needed": ["Trending audio", "Mobile footage", "Quick graphics", "Hashtag research"],
                "output_specs": {"resolution": "1080x1920", "fps": 30, "format": "MP4", "duration": "15-60 seconds"}
            },
            {
                "name": "Executive Presentation",
                "description": "High-stakes presentations for C-level executives and board meetings",
                "category": "corporate",
                "tags": ["Corporate", "Executives", "Professional", "B2B", "Presentation"],
                "templates": ["corporate_presentation"],
                "workflow_steps": [
                    {"step": "Executive Briefing", "description": "Understand key business objectives"},
                    {"step": "Data Visualization", "description": "Transform complex data into clear visuals"},
                    {"step": "Professional Design", "description": "Sleek, executive-appropriate aesthetics"},
                    {"step": "Stakeholder Review", "description": "Multiple rounds of executive feedback"},
                    {"step": "Rehearsal Support", "description": "Support materials for presentation delivery"},
                ],
                "estimated_time": "12-16 hours",
                "difficulty": "advanced",
                "assets_needed": ["Business data", "Corporate branding", "Professional photos", "Charts/graphs"],
                "output_specs": {"resolution": "1920x1080", "fps": 30, "format": "MP4", "duration": "20-30 minutes"}
            },
            {
                "name": "Real Estate Showcase",
                "description": "Stunning property showcase videos for real estate marketing",
                "category": "marketing",
                "tags": ["Real Estate", "Professional", "High Quality", "Marketing"],
                "templates": ["marketing_showcase"],
                "workflow_steps": [
                    {"step": "Property Survey", "description": "Plan shots and highlight key features"},
                    {"step": "Professional Filming", "description": "High-quality videography and drone footage"},
                    {"step": "Luxury Editing", "description": "Cinematic editing with music"},
                    {"step": "Market Positioning", "description": "Align with target buyer demographics"},
                    {"step": "Multi-Platform", "description": "Versions for web, social, and presentations"},
                ],
                "estimated_time": "6-10 hours",
                "difficulty": "intermediate",
                "assets_needed": ["Drone footage", "Professional equipment", "Luxury music", "Property details"],
                "output_specs": {"resolution": "4K", "fps": 24, "format": "MP4", "duration": "2-4 minutes"}
            }
        ]
        
        created_use_cases = []
        for uc_data in custom_use_cases:
            use_case = self.editor.create_use_case(
                name=uc_data["name"],
                description=uc_data["description"],
                category=uc_data["category"],
                tags=uc_data["tags"],
                templates=uc_data["templates"],
                workflow_steps=uc_data["workflow_steps"],
                estimated_time=uc_data["estimated_time"],
                difficulty=uc_data["difficulty"],
                assets_needed=uc_data["assets_needed"],
                output_specs=uc_data["output_specs"]
            )
            created_use_cases.append(use_case)
            print(f"   ✅ Created: {use_case.name}")
            print(f"      Category: {use_case.category} | Difficulty: {use_case.difficulty}")
            print(f"      Time: {use_case.estimated_time} | Tags: {', '.join(use_case.tags[:3])}...")
            print()
        
        print(f"🎯 Total custom use cases created: {len(created_use_cases)}")
        return created_use_cases
    
    def create_organized_projects(self):
        """Create a set of well-organized projects with strategic tagging"""
        print("\n📁 Creating Organized Project Portfolio")
        print("=" * 40)
        
        project_scenarios = [
            {
                "name": "HealthTech Product Demo",
                "tags": ["Healthcare", "Tech Startup", "Professional", "B2B", "Product Demo"],
                "description": "Demo video for new healthcare technology platform"
            },
            {
                "name": "Gen Z Fashion Campaign",
                "tags": ["Gen Z", "TikTok", "Instagram Reels", "Quick & Simple", "Fashion"],
                "description": "Viral campaign for fashion brand targeting Gen Z"
            },
            {
                "name": "Executive Q4 Presentation",
                "tags": ["Corporate", "Executives", "Professional", "Quarterly", "Data"],
                "description": "Q4 results presentation for board meeting"
            },
            {
                "name": "Luxury Real Estate Tour",
                "tags": ["Real Estate", "High Quality", "Professional", "Luxury", "Showcase"],
                "description": "Premium property showcase for high-end listings"
            },
            {
                "name": "Medical Training Series",
                "tags": ["Healthcare", "Educational", "Long Form", "Training", "Compliance"],
                "description": "Educational series for medical professionals"
            },
            {
                "name": "Startup Pitch Deck Video",
                "tags": ["Tech Startup", "B2B", "Professional", "Pitch", "Investment"],
                "description": "Video presentation for investor meetings"
            }
        ]
        
        created_projects = []
        for i, scenario in enumerate(project_scenarios):
            # Create project with appropriate specs based on tags
            if "TikTok" in scenario["tags"] or "Instagram Reels" in scenario["tags"]:
                width, height, duration = 1080, 1920, 30.0  # Vertical short-form
            elif "Executives" in scenario["tags"]:
                width, height, duration = 1920, 1080, 600.0  # Long presentation
            elif "Real Estate" in scenario["tags"]:
                width, height, duration = 3840, 2160, 180.0  # 4K showcase
            else:
                width, height, duration = 1920, 1080, 120.0  # Standard format
            
            project = self.editor.create_project(
                name=scenario["name"],
                width=width,
                height=height,
                duration=duration
            )
            
            # Assign tags
            self.editor.assign_tags_to_project(project.id, scenario["tags"])
            
            # Add some sample elements
            if "Educational" in scenario["tags"]:
                # Educational content structure
                title = self.editor.add_text_element(
                    project.id, "Learning Objectives", 100, 100, font_size=36
                )
                self.editor.assign_tags_to_element(project.id, title.id, ["Educational", "Title"])
                
            elif "Real Estate" in scenario["tags"]:
                # Real estate showcase structure
                title = self.editor.add_text_element(
                    project.id, "Luxury Property Showcase", 200, 150, font_size=48
                )
                self.editor.assign_tags_to_element(project.id, title.id, ["Real Estate", "Title"])
                
            elif any(tag in scenario["tags"] for tag in ["TikTok", "Instagram Reels"]):
                # Social media structure
                hook = self.editor.add_text_element(
                    project.id, "Stop Scrolling! 👀", 100, 200, font_size=32
                )
                self.editor.assign_tags_to_element(project.id, hook.id, ["Social Media", "Hook"])
            
            created_projects.append(project)
            print(f"   ✅ Created: {project.name}")
            print(f"      Tags: {', '.join(project.tags)}")
            print(f"      Specs: {width}x{height}, {duration}s")
            print()
        
        self.projects = created_projects
        print(f"📁 Total organized projects created: {len(created_projects)}")
        return created_projects
    
    def demonstrate_smart_recommendations(self):
        """Showcase the smart recommendation system"""
        print("\n🧠 Smart Recommendations Demo")
        print("=" * 40)
        
        for project in self.projects[:3]:  # Demo first 3 projects
            print(f"\n🎬 Project: {project.name}")
            print(f"   Current tags: {', '.join(project.tags)}")
            
            # Get recommendations
            recommendations = self.editor.get_recommended_use_cases(project.tags)
            
            if recommendations:
                print(f"   💡 Recommended use cases ({len(recommendations)}):")
                for i, use_case in enumerate(recommendations[:3], 1):
                    matching_tags = set(project.tags) & set(use_case.tags)
                    match_percentage = len(matching_tags) / len(use_case.tags) * 100
                    
                    print(f"      {i}. {use_case.name}")
                    print(f"         Match: {match_percentage:.0f}% ({', '.join(matching_tags)})")
                    print(f"         Time: {use_case.estimated_time} | Difficulty: {use_case.difficulty}")
                
                # Apply the best recommendation
                best_use_case = recommendations[0]
                success = self.editor.apply_use_case_to_project(project.id, best_use_case.id)
                if success:
                    print(f"   ✅ Applied use case: {best_use_case.name}")
                    print(f"   📋 Updated tags: {', '.join(project.tags)}")
                    print(f"   📊 Metadata keys: {list(project.metadata.keys())}")
            else:
                print("   ℹ️  No specific recommendations found")
    
    def show_workflow_optimization(self):
        """Demonstrate workflow optimization features"""
        print("\n⚡ Workflow Optimization")
        print("=" * 40)
        
        # Tag-based project search
        print("🔍 Tag-based Project Search:")
        search_tags = ["Professional", "Healthcare", "Tech Startup"]
        
        for tag in search_tags:
            matching_projects = self.editor.search_projects_by_tags([tag])
            print(f"   '{tag}': {len(matching_projects)} projects")
            for project in matching_projects[:2]:  # Show first 2
                print(f"      • {project.name}")
        
        # Category analysis
        print(f"\n📊 Project Organization by Category:")
        all_tags = self.editor.get_tags()
        categories = {}
        for tag in all_tags:
            if tag.category not in categories:
                categories[tag.category] = []
            categories[tag.category].append(tag.name)
        
        for category, tag_names in categories.items():
            print(f"   {category.title()}: {len(tag_names)} tags")
            print(f"      {', '.join(tag_names[:5])}{'...' if len(tag_names) > 5 else ''}")
        
        # Analytics
        print(f"\n📈 Usage Analytics:")
        analytics = self.editor.get_tag_analytics()
        print(f"   Total tags: {analytics['total_tags']}")
        print(f"   Total use cases: {analytics['total_use_cases']}")
        print(f"   Categories: {len(analytics['category_distribution'])}")
        
        if analytics['most_used_tags']:
            print("   Most used tags:")
            for tag, count in analytics['most_used_tags'][:5]:
                print(f"      • {tag}: {count} uses")
    
    def demonstrate_advanced_features(self):
        """Show advanced workflow features"""
        print("\n🚀 Advanced Workflow Features")
        print("=" * 40)
        
        # Template suggestions based on tags
        print("📋 Template Suggestions:")
        for project in self.projects[:2]:
            print(f"\n   Project: {project.name}")
            
            # Suggest templates based on project tags
            template_suggestions = []
            if any(tag in project.tags for tag in ["Social Media", "TikTok", "Instagram"]):
                template_suggestions.append("social_media_post")
            if any(tag in project.tags for tag in ["Corporate", "Executives"]):
                template_suggestions.append("corporate_presentation") 
            if any(tag in project.tags for tag in ["Educational", "Healthcare"]):
                template_suggestions.append("educational_video")
            
            print(f"   Suggested templates: {', '.join(template_suggestions) if template_suggestions else 'Standard templates'}")
        
        # Workflow step optimization
        print(f"\n⚙️  Workflow Steps Analysis:")
        use_cases = self.editor.get_use_cases()
        
        # Analyze common workflow patterns
        all_steps = []
        for uc in use_cases:
            for step in uc.workflow_steps:
                all_steps.append(step['step'])
        
        from collections import Counter
        step_frequency = Counter(all_steps)
        
        print("   Most common workflow steps:")
        for step, count in step_frequency.most_common(5):
            print(f"      • {step}: appears in {count} use cases")
        
        # Time estimation
        print(f"\n⏱️  Production Time Analysis:")
        difficulty_times = {"beginner": [], "intermediate": [], "advanced": []}
        
        for uc in use_cases:
            if uc.difficulty in difficulty_times:
                # Extract numeric time estimate
                time_str = uc.estimated_time.split('-')[0].strip()
                try:
                    hours = int(time_str.split()[0])
                    difficulty_times[uc.difficulty].append(hours)
                except:
                    pass
        
        for difficulty, times in difficulty_times.items():
            if times:
                avg_time = sum(times) / len(times)
                print(f"   {difficulty.title()}: ~{avg_time:.1f} hours average")
    
    def generate_workflow_report(self):
        """Generate a comprehensive workflow report"""
        print("\n📄 Workflow Analysis Report")
        print("=" * 40)
        
        # Project summary
        total_projects = len(self.projects)
        total_elements = sum(len(p.elements) for p in self.projects)
        
        print(f"📊 Portfolio Summary:")
        print(f"   Projects: {total_projects}")
        print(f"   Elements: {total_elements}")
        print(f"   Avg elements per project: {total_elements/total_projects:.1f}")
        
        # Tag distribution
        project_tags = []
        for project in self.projects:
            project_tags.extend(project.tags)
        
        from collections import Counter
        tag_usage = Counter(project_tags)
        
        print(f"\n🏷️  Tag Usage Distribution:")
        for tag, count in tag_usage.most_common(10):
            percentage = (count / total_projects) * 100
            print(f"   {tag}: {count} projects ({percentage:.0f}%)")
        
        # Use case application
        applied_use_cases = [p.use_case_id for p in self.projects if p.use_case_id]
        print(f"\n🎯 Use Case Application:")
        print(f"   Projects with use cases: {len(applied_use_cases)}/{total_projects}")
        print(f"   Application rate: {len(applied_use_cases)/total_projects*100:.0f}%")
        
        # Recommendations efficiency
        total_recommendations = 0
        successful_matches = 0
        
        for project in self.projects:
            recommendations = self.editor.get_recommended_use_cases(project.tags)
            total_recommendations += len(recommendations)
            if recommendations:
                successful_matches += 1
        
        print(f"\n💡 Recommendation Efficiency:")
        print(f"   Projects with recommendations: {successful_matches}/{total_projects}")
        print(f"   Average recommendations per project: {total_recommendations/total_projects:.1f}")
        print(f"   Recommendation success rate: {successful_matches/total_projects*100:.0f}%")
    
    def run_complete_demo(self):
        """Run the complete smart workflow demonstration"""
        print("🎬 SMART VIDEO CREATION WORKFLOW DEMO")
        print("=" * 50)
        print("Demonstrating advanced Canvas Editor capabilities")
        print("for efficient video production workflows!\n")
        
        try:
            # Step 1: Create custom tags
            self.create_custom_tags()
            
            # Step 2: Create custom use cases
            self.create_custom_use_cases()
            
            # Step 3: Create organized projects
            self.create_organized_projects()
            
            # Step 4: Demonstrate smart recommendations
            self.demonstrate_smart_recommendations()
            
            # Step 5: Show workflow optimization
            self.show_workflow_optimization()
            
            # Step 6: Advanced features
            self.demonstrate_advanced_features()
            
            # Step 7: Generate report
            self.generate_workflow_report()
            
            print("\n" + "=" * 50)
            print("✅ SMART WORKFLOW DEMO COMPLETED!")
            print("🎯 Your Canvas Editor now includes:")
            print("   • Custom industry-specific tags")
            print("   • Advanced use case templates")
            print("   • Intelligently organized projects")
            print("   • Smart recommendation system")
            print("   • Workflow optimization tools")
            print("   • Advanced analytics and insights")
            print("\n🚀 Ready for professional video production!")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    demo = SmartWorkflowDemo()
    demo.run_complete_demo()
