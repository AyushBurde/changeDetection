#!/usr/bin/env python3
"""
Development setup script for Change Detection System
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/imagery",
        "data/results", 
        "data/temp",
        "logs",
        "uploads"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_python_env():
    """Set up Python virtual environment"""
    if not Path("backend/venv").exists():
        print("🐍 Setting up Python virtual environment...")
        os.chdir("backend")
        
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
            
        # Activate virtual environment and install dependencies
        if os.name == 'nt':  # Windows
            activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
        else:  # Unix/Linux/Mac
            activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
            
        if not run_command(activate_cmd, "Installing Python dependencies"):
            return False
            
        os.chdir("..")
    else:
        print("✅ Python virtual environment already exists")
    
    return True

def setup_node_env():
    """Set up Node.js environment"""
    if not Path("frontend/node_modules").exists():
        print("🟢 Setting up Node.js environment...")
        os.chdir("frontend")
        
        if not run_command("npm install", "Installing Node.js dependencies"):
            return False
            
        os.chdir("..")
    else:
        print("✅ Node.js dependencies already installed")
    
    return True

def create_env_file():
    """Create .env file with development settings"""
    env_content = """# Development Environment Variables
DATABASE_URL=postgresql://postgres:password@localhost:5432/change_detection_db
REDIS_URL=redis://localhost:6379/0
BHOONIDHI_API_KEY=your_api_key_here
BHOONIDHI_USERNAME=your_username_here
BHOONIDHI_PASSWORD=your_password_here
LOG_LEVEL=DEBUG
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("📝 Created .env file with development settings")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Change Detection System Development Environment")
    print("=" * 60)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    
    # Check Python
    try:
        python_version = subprocess.run(["python", "--version"], capture_output=True, text=True)
        print(f"✅ Python: {python_version.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Python not found. Please install Python 3.8+")
        return False
    
    # Check Node.js
    try:
        node_version = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✅ Node.js: {node_version.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False
    
    # Check npm
    try:
        npm_version = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        print(f"✅ npm: {npm_version.stdout.strip()}")
    except FileNotFoundError:
        print("❌ npm not found. Please install npm")
        return False
    
    print("\n📁 Creating project directories...")
    create_directories()
    
    print("\n🐍 Setting up Python environment...")
    if not setup_python_env():
        print("❌ Python environment setup failed")
        return False
    
    print("\n🟢 Setting up Node.js environment...")
    if not setup_node_env():
        print("❌ Node.js environment setup failed")
        return False
    
    print("\n📝 Creating environment configuration...")
    create_env_file()
    
    print("\n" + "=" * 60)
    print("🎉 Development environment setup completed!")
    print("\n📋 Next steps:")
    print("1. Copy config/config.example.yml to config/config.yml")
    print("2. Update database credentials in config/config.yml")
    print("3. Set up PostgreSQL with PostGIS extension")
    print("4. Update Bhoonidhi API credentials")
    print("5. Run 'python backend/main.py' to start the backend")
    print("6. Run 'npm run serve' in frontend/ to start the frontend")
    print("\n📚 Check README.md for detailed setup instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


