"""
Simple API tests for the Resilience2Relief AI system
Tests the main functionality without complex dependencies
"""

import requests
import json
import time
import tempfile
import os

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 30

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing health check endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"  ❌ Health check failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Health check failed: {str(e)}")
        return False

def test_api_info():
    """Test the API info endpoint"""
    print("ℹ️  Testing API info endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'Resilience2Relief AI' in data.get('message', ''):
                print(f"  ✅ API info passed: {data['data']['name']}")
                return True
            else:
                print(f"  ❌ API info failed: Unexpected response format")
                return False
        else:
            print(f"  ❌ API info failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ API info failed: {str(e)}")
        return False

def test_project_generation():
    """Test the project generation endpoint"""
    print("🚀 Testing project generation endpoint...")
    
    test_request = {
        "query": "Generate disaster recovery projects for cyclone-affected communities in Pacific islands",
        "disaster_type": "cyclone",
        "region": "vanuatu",
        "max_projects": 3,
        "sectors": ["housing", "infrastructure"],
        "priority": "high"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json=test_request,
            headers={"Content-Type": "application/json"},
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if (data.get('success') and 
                data.get('data', {}).get('projects') and
                len(data['data']['projects']) > 0):
                
                projects = data['data']['projects']
                print(f"  ✅ Project generation passed: Generated {len(projects)} projects")
                
                # Validate project structure
                first_project = projects[0]
                required_fields = ['title', 'description', 'sector', 'budget']
                
                for field in required_fields:
                    if field not in first_project:
                        print(f"  ⚠️  Missing field in project: {field}")
                
                print(f"  📋 Sample project: {first_project.get('title', 'No title')}")
                print(f"  💰 Budget: {first_project.get('budget', 'Not specified')}")
                print(f"  🏢 Sector: {first_project.get('sector', 'Not specified')}")
                
                return True
            else:
                print(f"  ❌ Project generation failed: Invalid response format")
                print(f"  📄 Response: {response.text[:200]}...")
                return False
        else:
            print(f"  ❌ Project generation failed with status: {response.status_code}")
            print(f"  📄 Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"  ❌ Project generation failed: {str(e)}")
        return False

def test_file_upload():
    """Test the file upload endpoint"""
    print("📤 Testing file upload endpoint...")
    
    # Create a test file
    test_content = """
    Disaster Recovery Assessment - Test Document
    
    This is a test document for the Resilience2Relief AI system.
    
    Key sectors:
    - Housing reconstruction
    - Infrastructure repair
    - Healthcare system strengthening
    
    Estimated budget: $50 million
    Timeline: 24 months
    Beneficiaries: 100,000 people
    """
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as file:
                files = {'file': ('test_document.txt', file, 'text/plain')}
                response = requests.post(f"{BASE_URL}/upload", files=files, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"  ✅ File upload passed: {data['data']['filename']}")
                    print(f"  📊 File size: {data['data']['file_size']} bytes")
                    return True
                else:
                    print(f"  ❌ File upload failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                print(f"  ❌ File upload failed with status: {response.status_code}")
                return False
                
        finally:
            # Clean up test file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        print(f"  ❌ File upload failed: {str(e)}")
        return False

def test_system_stats():
    """Test the system statistics endpoint"""
    print("📊 Testing system statistics endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if (data.get('success') and 
                'total_documents' in data.get('data', {})):
                
                stats = data['data']
                print(f"  ✅ System stats passed")
                print(f"  📄 Total documents: {stats.get('total_documents', 0)}")
                print(f"  🚀 Projects generated: {stats.get('total_projects_generated', 0)}")
                print(f"  🏢 Available sectors: {len(stats.get('available_sectors', []))}")
                print(f"  🌍 Supported regions: {len(stats.get('supported_regions', []))}")
                
                return True
            else:
                print(f"  ❌ System stats failed: Invalid response format")
                return False
        else:
            print(f"  ❌ System stats failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ System stats failed: {str(e)}")
        return False

def test_search_functionality():
    """Test the search endpoint"""
    print("🔍 Testing search functionality...")
    
    search_params = {
        'q': 'housing reconstruction',
        'sector': 'infrastructure',
        'region': 'vanuatu',
        'priority': 'high'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/search", params=search_params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"  ✅ Search functionality passed")
                results = data.get('data', {})
                print(f"  🔍 Query: {results.get('query', 'N/A')}")
                print(f"  📊 Total matches: {results.get('total_matches', 0)}")
                return True
            else:
                print(f"  ❌ Search failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"  ❌ Search failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Search failed: {str(e)}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🧪 Resilience2Relief AI - API Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("API Info", test_api_info),
        ("Project Generation", test_project_generation),
        ("File Upload", test_file_upload),
        ("System Statistics", test_system_stats),
        ("Search Functionality", test_search_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} Test...")
        try:
            if test_func():
                passed += 1
                print(f"   ✅ {test_name}: PASSED")
            else:
                print(f"   ❌ {test_name}: FAILED")
        except Exception as e:
            print(f"   ❌ {test_name}: ERROR - {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! API is fully functional.")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. Review errors above.")
        return False

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    success = run_all_tests()
    exit(0 if success else 1)