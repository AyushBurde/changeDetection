# PostgreSQL Setup Guide for Change Detection System

## 🎯 **What You Need for This Project**

### **Essential Components:**
1. **PostgreSQL Database Server** - Core database engine
2. **PostGIS Spatial Extension** - Handles geometric data and spatial operations
3. **Python Drivers** - psycopg2 for database connectivity
4. **Database Management Tool** - pgAdmin or DBeaver for database administration

### **Why PostGIS is Critical:**
- **AOI Management**: Store and query Areas of Interest as polygons
- **Spatial Indexing**: Fast geospatial queries for large datasets
- **Coordinate Systems**: Handle different map projections and coordinate systems
- **Spatial Operations**: Calculate intersections, buffers, distances between geometries
- **Satellite Data**: Store imagery footprints and metadata with spatial references

## 🚀 **Installation Methods**

### **Method 1: PostgreSQL + PostGIS Bundle (RECOMMENDED)**
**Best for beginners - everything included in one installer**

1. **Download PostGIS Bundle**: https://postgis.net/windows_downloads/
2. **Choose**: "PostGIS Bundle for PostgreSQL" (includes PostgreSQL + PostGIS)
3. **Version**: PostgreSQL 15 or 16 with PostGIS 3.3+
4. **Run installer** and follow the setup wizard

### **Method 2: Separate Installation**
**More control but requires multiple steps**

1. **Install PostgreSQL**: https://www.postgresql.org/download/windows/
2. **Install PostGIS extension** after PostgreSQL setup
3. **Install pgAdmin** for database management

## 📋 **Step-by-Step Installation (Method 1 - Recommended)**

### **Step 1: Download and Install**
1. Go to: https://postgis.net/windows_downloads/
2. Download: "PostGIS Bundle for PostgreSQL 15/16"
3. Run the installer as Administrator
4. **Important Settings**:
   - **Port**: 5432 (default)
   - **Password**: Set a strong password (remember this!)
   - **Install PostGIS**: Make sure this is checked
   - **Install pgAdmin**: Check this for database management

### **Step 2: Verify Installation**
After installation, you should have:
- ✅ PostgreSQL service running
- ✅ PostGIS extension available
- ✅ pgAdmin web interface accessible
- ✅ psql command-line tool available

### **Step 3: Create Your Database**
1. **Open pgAdmin** (usually at http://localhost:8080)
2. **Connect to PostgreSQL** using your password
3. **Create new database**:
   ```sql
   CREATE DATABASE change_detection_db;
   ```
4. **Enable PostGIS extension**:
   ```sql
   \c change_detection_db
   CREATE EXTENSION postgis;
   CREATE EXTENSION postgis_topology;
   ```

## 🔧 **Configuration for Your Project**

### **Database Connection String**
Update your `backend/config/config.yml`:
```yaml
database:
  url: "postgresql://postgres:your_password@localhost:5432/change_detection_db"
  host: "localhost"
  port: 5432
  name: "change_detection_db"
  user: "postgres"
  password: "your_password"
```

### **Environment Variables**
Create `.env` file in backend directory:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/change_detection_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=change_detection_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

## 🧪 **Testing Your Setup**

### **Test Database Connection**
1. **Start your backend**: `python main.py`
2. **Test health endpoint**: http://localhost:8000/health
3. **Check database connectivity** (after implementing database models)

### **Test PostGIS Functions**
In pgAdmin, run:
```sql
-- Test PostGIS installation
SELECT PostGIS_Version();

-- Test spatial functions
SELECT ST_AsText(ST_GeomFromText('POINT(0 0)'));
```

## 🚨 **Common Issues and Solutions**

### **Issue 1: "pg_config not found"**
- **Solution**: Install PostgreSQL with development tools
- **Alternative**: Use `psycopg2-binary` instead of `psycopg2`

### **Issue 2: "PostGIS extension not available"**
- **Solution**: Make sure PostGIS was installed with PostgreSQL
- **Check**: Look for PostGIS in PostgreSQL extensions list

### **Issue 3: "Connection refused"**
- **Solution**: Check if PostgreSQL service is running
- **Windows**: Services → PostgreSQL → Start

### **Issue 4: "Authentication failed"**
- **Solution**: Verify username/password in connection string
- **Check**: pg_hba.conf file for authentication settings

## 📊 **What This Enables in Your Project**

### **Immediate Benefits:**
- ✅ **Store AOI geometries** as PostGIS polygons
- ✅ **Spatial queries** for finding overlapping areas
- ✅ **Coordinate system handling** for different map projections
- ✅ **Spatial indexing** for fast geospatial operations

### **Advanced Features:**
- 🚀 **Buffer analysis** around AOIs
- 🚀 **Intersection detection** between areas
- 🚀 **Distance calculations** between features
- 🚀 **Spatial joins** for complex queries

## 🎯 **Next Steps After Installation**

1. **Test database connection** in your backend
2. **Run database migrations** to create tables
3. **Test AOI model** with PostGIS geometry
4. **Implement spatial queries** in your API
5. **Connect frontend** to display spatial data

## 🔗 **Useful Resources**

- **PostGIS Documentation**: https://postgis.net/documentation/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **pgAdmin Documentation**: https://www.pgadmin.org/docs/
- **Spatial SQL Examples**: https://postgis.net/workshops/

---

**Ready to install?** Start with Method 1 (PostGIS Bundle) for the easiest setup experience!

