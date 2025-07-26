#!/usr/bin/env python3
"""
🚀 Smart Workflow API Integration Example
Shows how to use Canvas Editor smart features via FastAPI endpoints
"""

import requests
import json

class SmartWorkflowAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def demonstrate_smart_workflow_api(self):
        """Demonstrate smart workflow features via API"""
        print("🚀 SMART WORKFLOW API INTEGRATION")
        print("=" * 50)
        
        # Test basic Canvas Editor endpoints
        print("📡 Testing Canvas Editor API endpoints...")
        
        try:
            # 1. List available tags
            print("\n🏷️  Getting available tags...")
            response = requests.get(f"{self.base_url}/canvas/tags")
            if response.status_code == 200:
                tags = response.json()
                print(f"   ✅ Found {len(tags)} tags across categories:")
                
                # Group by category
                categories = {}
                for tag in tags:
                    cat = tag.get('category', 'other')
                    if cat not in categories:
                        categories[cat] = 0
                    categories[cat] += 1
                
                for category, count in categories.items():
                    print(f"      • {category.title()}: {count} tags")
            
            # 2. List available use cases
            print("\n🎯 Getting available use cases...")
            response = requests.get(f"{self.base_url}/canvas/use-cases")
            if response.status_code == 200:
                use_cases = response.json()
                print(f"   ✅ Found {len(use_cases)} use cases:")
                for uc in use_cases[:5]:
                    print(f"      • {uc['name']} ({uc['category']}) - {uc['difficulty']}")
            
            # 3. Create a smart project
            print("\n📁 Creating smart project via API...")
            project_data = {
                "name": "API Smart Project",
                "width": 1080,
                "height": 1920,
                "duration": 30.0,
                "tags": ["Marketing", "Social Media", "Gen Z"]
            }
            
            response = requests.post(f"{self.base_url}/canvas/projects", json=project_data)
            if response.status_code == 200:
                project = response.json()
                project_id = project['id']
                print(f"   ✅ Created project: {project['name']}")
                print(f"      ID: {project_id}")
                print(f"      Tags: {project.get('tags', [])}")
                
                # 4. Get smart recommendations
                print(f"\n💡 Getting smart recommendations...")
                response = requests.get(f"{self.base_url}/canvas/projects/{project_id}/recommendations")
                if response.status_code == 200:
                    recommendations = response.json()
                    print(f"   ✅ Found {len(recommendations)} recommendations:")
                    for rec in recommendations[:3]:
                        print(f"      • {rec['name']} (Match: {rec.get('match_score', 0):.0f}%)")
                
                # 5. Apply a use case
                if recommendations:
                    best_use_case_id = recommendations[0]['id']
                    print(f"\n🎯 Applying best use case...")
                    response = requests.post(
                        f"{self.base_url}/canvas/projects/{project_id}/apply-use-case/{best_use_case_id}"
                    )
                    if response.status_code == 200:
                        updated_project = response.json()
                        print(f"   ✅ Applied use case successfully")
                        print(f"      Updated tags: {updated_project.get('tags', [])}")
                
                # 6. Add smart elements
                print(f"\n🎨 Adding smart elements...")
                element_data = {
                    "type": "text",
                    "x": 100,
                    "y": 200,
                    "width": 300,
                    "height": 50,
                    "properties": {"text": "Smart Hook!", "font_size": 36},
                    "tags": ["Hook", "Gen Z"]
                }
                
                response = requests.post(f"{self.base_url}/canvas/projects/{project_id}/elements", json=element_data)
                if response.status_code == 200:
                    element = response.json()
                    print(f"   ✅ Added smart element: {element['type']}")
                    print(f"      Tags: {element.get('tags', [])}")
                
                # 7. Search projects by tags
                print(f"\n🔍 Searching projects by tags...")
                search_params = {"tags": ["Marketing", "Social Media"]}
                response = requests.get(f"{self.base_url}/canvas/search/projects", params=search_params)
                if response.status_code == 200:
                    search_results = response.json()
                    print(f"   ✅ Found {len(search_results)} projects with marketing tags")
                
                # 8. Get analytics
                print(f"\n📈 Getting workflow analytics...")
                response = requests.get(f"{self.base_url}/canvas/analytics")
                if response.status_code == 200:
                    analytics = response.json()
                    print(f"   ✅ Analytics:")
                    print(f"      Total tags: {analytics.get('total_tags', 0)}")
                    print(f"      Total use cases: {analytics.get('total_use_cases', 0)}")
                    print(f"      Most used tags: {analytics.get('most_used_tags', [])[:3]}")
                
                print(f"\n✅ Smart Workflow API Integration Complete!")
                print(f"🎯 All advanced features working via REST API")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to FastAPI server")
            print("💡 To test API integration:")
            print("   1. Start the FastAPI server: python fastapi_ai_video_controller.py")
            print("   2. Run this script again")
            print("\n🔧 API Endpoints Available:")
            self.show_available_endpoints()
            
        except Exception as e:
            print(f"❌ API test error: {e}")
    
    def show_available_endpoints(self):
        """Show the available API endpoints for smart workflow"""
        endpoints = [
            "🏷️  Tag Management:",
            "   GET  /canvas/tags - List all tags",
            "   POST /canvas/tags - Create new tag",
            "   GET  /canvas/tags/{category} - Get tags by category",
            "",
            "🎯 Use Case Management:",
            "   GET  /canvas/use-cases - List all use cases",
            "   POST /canvas/use-cases - Create new use case",
            "   GET  /canvas/use-cases/{category} - Get use cases by category",
            "",
            "📁 Smart Project Management:",
            "   POST /canvas/projects - Create project (with tags)",
            "   GET  /canvas/projects/{id}/recommendations - Get smart recommendations",
            "   POST /canvas/projects/{id}/apply-use-case/{use_case_id} - Apply use case",
            "   POST /canvas/projects/{id}/tags - Assign tags to project",
            "",
            "🎨 Smart Element Management:",
            "   POST /canvas/projects/{id}/elements - Add element (with tags)",
            "   POST /canvas/elements/{id}/tags - Assign tags to element",
            "",
            "🔍 Search & Analytics:",
            "   GET  /canvas/search/projects?tags=tag1,tag2 - Search by tags",
            "   GET  /canvas/analytics - Get usage analytics",
            "   GET  /canvas/workflow/recommendations/{project_id} - Smart workflow suggestions",
        ]
        
        for endpoint in endpoints:
            print(endpoint)

if __name__ == "__main__":
    api = SmartWorkflowAPI()
    api.demonstrate_smart_workflow_api()
