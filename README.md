# Change Detection & Monitoring System

A robust, automated change detection and alert system using multi-temporal satellite imagery for user-defined Areas of Interest (AOIs).

## 🎯 Project Overview

This system provides:
- **Automated change detection** with cloud/shadow masking
- **Web-based AOI selection** and visualization tools
- **Real-time monitoring** and alert notifications
- **GIS-compatible outputs** for spatial analysis

## 🏗️ Architecture

```
├── backend/                 # Python backend services
│   ├── api/                # REST API endpoints
│   ├── core/               # Core change detection algorithms
│   ├── models/             # Data models and database schemas
│   └── services/           # Business logic services
├── frontend/               # Vue.js web application
│   ├── components/         # Vue components
│   ├── views/              # Page views
│   └── assets/             # Static assets
├── database/               # Database migrations and schemas
├── config/                 # Configuration files
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ with PostGIS
- Docker (optional)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
npm run serve
```

### Database Setup
```bash
# Create database and enable PostGIS
createdb change_detection_db
psql change_detection_db -c "CREATE EXTENSION postgis;"
```

## 📋 Development Roadmap

- [x] Project structure setup
- [ ] Backend API development
- [ ] Change detection algorithms
- [ ] Frontend web interface
- [ ] Database integration
- [ ] Alert system implementation
- [ ] Testing and optimization
- [ ] Deployment

## 🔧 Configuration

Copy `config/config.example.yml` to `config/config.yml` and update with your settings:
- Database credentials
- Bhoonidhi API credentials
- Email service configuration
- File storage paths

## 📚 API Documentation

API endpoints and usage examples are available in the `docs/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.
