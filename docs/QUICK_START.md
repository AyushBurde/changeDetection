# 🚀 Quick Start Guide

Get the Change Detection System up and running in 30 minutes!

## ⚡ Prerequisites Check

Before starting, ensure you have:

- ✅ **Python 3.8+** installed
- ✅ **Node.js 16+** installed  
- ✅ **PostgreSQL 12+** with PostGIS extension
- ✅ **Redis** (optional, for task queuing)

## 🛠️ Step-by-Step Setup

### 1. Clone and Navigate
```bash
cd "cursor demo"
```

### 2. Run Automated Setup
```bash
python setup_dev.py
```

This script will:
- Create all necessary directories
- Set up Python virtual environment
- Install Python dependencies
- Install Node.js dependencies
- Create configuration files

### 3. Database Setup

#### Install PostgreSQL + PostGIS
- **Windows**: Download from [PostgreSQL.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql postgis`
- **Linux**: `sudo apt-get install postgresql postgis`

#### Create Database
```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE change_detection_db;

-- Connect to new database
\c change_detection_db

-- Enable PostGIS extension
CREATE EXTENSION postgis;

-- Exit
\q
```

### 4. Configuration

#### Copy Configuration File
```bash
cp config/config.example.yml config/config.yml
```

#### Update `config/config.yml`
```yaml
database:
  host: localhost
  port: 5432
  name: change_detection_db
  user: postgres
  password: your_actual_password

bhoonidhi:
  api_key: your_bhoonidhi_api_key
  username: your_bhoonidhi_username
  password: your_bhoonidhi_password
```

### 5. Test Backend

#### Activate Python Environment
```bash
cd backend
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### Start API Server
```bash
python main.py
```

#### Test API
Open browser to: `http://localhost:8000/docs`

You should see the FastAPI interactive documentation!

### 6. Test Frontend

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm run serve
```

#### Open Frontend
Navigate to: `http://localhost:8080`

## 🧪 Verify Installation

### Backend Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Change Detection System",
  "version": "1.0.0"
}
```

### Database Connection
```bash
cd backend
python -c "from models.database import check_db_connection; check_db_connection()"
```

## 🚨 Troubleshooting

### Common Issues

#### Python Dependencies
```bash
# If you get import errors
pip install --upgrade pip
pip install -r requirements.txt
```

#### PostgreSQL Connection
```bash
# Test connection
psql -h localhost -U postgres -d change_detection_db -c "SELECT PostGIS_Version();"
```

#### Node.js Issues
```bash
# Clear npm cache
npm cache clean --force
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'rasterio'` | Run `pip install -r requirements.txt` |
| `connection refused` | Check PostgreSQL is running |
| `PostGIS extension not found` | Run `CREATE EXTENSION postgis;` |
| `npm ERR!` | Clear cache and reinstall: `npm cache clean --force` |

## 📱 Next Steps

### 1. Create Your First AOI
- Open the web interface
- Draw a polygon on the map
- Save it as an AOI

### 2. Test Change Detection
- Upload two satellite images
- Run change detection analysis
- View results and statistics

### 3. Configure Alerts
- Set up change thresholds
- Configure email notifications
- Test alert system

## 🔗 Useful Commands

### Backend Development
```bash
# Start API server
python main.py

# Run tests
pytest

# Check database
python -c "from models.database import check_db_connection; check_db_connection()"
```

### Frontend Development
```bash
# Start dev server
npm run serve

# Build for production
npm run build

# Run linter
npm run lint
```

### Database Management
```bash
# Connect to database
psql -U postgres -d change_detection_db

# View tables
\dt

# Check PostGIS
SELECT PostGIS_Version();
```

## 📚 Need Help?

- 📖 **Documentation**: Check `docs/` folder
- 🐛 **Issues**: Look at error logs in `logs/` folder
- 💬 **Community**: Check the project README for resources
- 🔧 **Debug**: Set `LOG_LEVEL=DEBUG` in your config

## 🎯 Success Indicators

You're ready to proceed when:

- ✅ Backend API responds at `http://localhost:8000/health`
- ✅ Frontend loads at `http://localhost:8080`
- ✅ Database connection test passes
- ✅ No error messages in console/logs
- ✅ All dependencies installed successfully

---

**🎉 Congratulations!** You now have a working Change Detection System development environment.

**Next**: Follow the [Project Execution Plan](PROJECT_EXECUTION_PLAN.md) to continue development!


