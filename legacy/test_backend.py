
#!/usr/bin/env python3
import requests
import json
import os

def test_backend_health():
    """Test if backend server is running"""
    try:
        response = requests.get("http://localhost:7071/health", timeout=5)
        print(f"✅ Backend Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend Health Check Failed: {str(e)}")
        return False

def test_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Environment Variables Check:")
    
    azure_key = os.getenv("AZURE_KEY")
    azure_endpoint = os.getenv("AZURE_ENDPOINT") 
    deepseek_endpoint = os.getenv("DEEPSEEK_ENDPOINT")
    
    if azure_key:
        print(f"✅ AZURE_KEY: Set (ends with ...{azure_key[-4:]})")
    else:
        print("❌ AZURE_KEY: Not set")
        
    if azure_endpoint:
        print(f"✅ AZURE_ENDPOINT: {azure_endpoint}")
    else:
        print("❌ AZURE_ENDPOINT: Not set")
        
    if deepseek_endpoint:
        print(f"✅ DEEPSEEK_ENDPOINT: {deepseek_endpoint}")
    else:
        print("❌ DEEPSEEK_ENDPOINT: Not set")
    
    return all([azure_key, azure_endpoint, deepseek_endpoint])

def test_chatgpt_api():
    """Test ChatGPT API endpoint"""
    if not test_environment_variables():
        print("❌ Skipping API tests - environment variables not set")
        return
        
    try:
        payload = {"message": "Hello, this is a test"}
        response = requests.post(
            "http://localhost:7071/api/ChatGpt_api",
            json=payload,
            timeout=30
        )
        print(f"\n🤖 ChatGPT API Test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Reply: {data.get('reply', 'No reply')[:100]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ ChatGPT API Test Failed: {str(e)}")

def test_deepseek_api():
    """Test DeepSeek API endpoint"""
    try:
        payload = {"message": "Hello, this is a test"}
        response = requests.post(
            "http://localhost:7071/api/DeepSeek_api",
            json=payload,
            timeout=30
        )
        print(f"\n🧠 DeepSeek API Test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Reply: {data.get('reply', 'No reply')[:100]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ DeepSeek API Test Failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 Backend API Testing Tool")
    print("=" * 40)
    
    # Test backend health
    if test_backend_health():
        print("\n🧪 Testing API endpoints...")
        test_chatgpt_api()
        test_deepseek_api()
    else:
        print("\n❌ Backend server is not running. Please start it first.")
        print("   Run: python backend_server.py")
    
    print("\n" + "=" * 40)
    print("🏁 Testing complete!")
