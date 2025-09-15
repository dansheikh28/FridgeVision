# 🚀 Production Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ **Environment Setup**
- [ ] Python 3.8+ installed
- [ ] Docker and Docker Compose installed (for containerized deployment)
- [ ] API keys obtained:
  - [ ] Google Gemini API key
  - [ ] Spoonacular API key (optional but recommended)
- [ ] SSL certificates (for HTTPS in production)
- [ ] Domain name configured (if applicable)

### ✅ **Security Checklist**
- [ ] API keys stored securely (environment variables, not in code)
- [ ] `.env` file added to `.gitignore`
- [ ] Rate limiting configured
- [ ] HTTPS enabled (production)
- [ ] Security headers configured
- [ ] File upload size limits set
- [ ] Input validation implemented

## 🐳 Docker Deployment (Recommended)

### **1. Quick Start**
```bash
# Clone repository
git clone https://github.com/yourusername/fridgevision.git
cd fridgevision

# Copy environment template
cp env.example .env

# Edit .env with your API keys
nano .env

# Build and run with Docker Compose
docker-compose up -d
```

### **2. Production with Nginx**
```bash
# Run with nginx reverse proxy
docker-compose --profile production up -d
```

### **3. Environment Variables**
Create `.env` file:
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
SPOONACULAR_API_KEY=your_spoonacular_api_key_here

# Optional Configuration
CONFIDENCE_THRESHOLD=0.6
MAX_RECIPES=10
LOG_LEVEL=INFO
STREAMLIT_HOST=0.0.0.0
STREAMLIT_PORT=8501
```

## 🖥️ Manual Deployment

### **1. System Requirements**
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB minimum
- **Network**: Stable internet connection for API calls

### **2. Installation Steps**
```bash
# 1. Clone and setup
git clone https://github.com/yourusername/fridgevision.git
cd fridgevision
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp env.example .env
# Edit .env with your API keys

# 4. Run application
python scripts/run_app.py
```

## ☁️ Cloud Deployment Options

### **Streamlit Cloud**
1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in Streamlit dashboard:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   SPOONACULAR_API_KEY = "your_key_here"
   ```
4. Deploy with one click

### **Heroku**
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set SPOONACULAR_API_KEY=your_key_here

# Deploy
git push heroku main
```

### **AWS/GCP/Azure**
- Use Docker container deployment
- Configure load balancer for high availability
- Set up auto-scaling based on traffic
- Use managed databases for caching (optional)

## 🔧 Configuration Options

### **Application Settings**
```env
# Detection Settings
CONFIDENCE_THRESHOLD=0.6        # AI detection confidence (0.3-0.9)
MAX_RECIPES=10                  # Maximum recipes to return
DEFAULT_CUISINE=Any             # Default cuisine filter
DEFAULT_DIET=None               # Default dietary restriction
MAX_COOKING_TIME=60             # Default max cooking time

# Performance Settings
MAX_IMAGE_SIZE=20971520         # 20MB max upload size
RATE_LIMIT_REQUESTS=100         # Requests per hour per IP
CACHE_DIR=data/cache            # Cache directory

# Security Settings
LOG_LEVEL=INFO                  # Logging level
DEBUG=False                     # Debug mode (never True in production)
```

### **Nginx Configuration**
For production with high traffic:
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;

# SSL termination
ssl_certificate /path/to/cert.pem;
ssl_certificate_key /path/to/key.pem;

# Caching
location ~* \.(js|css|png|jpg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 📊 Monitoring & Logging

### **Application Logs**
```bash
# View logs
docker-compose logs -f fridgevision

# Log files location
logs/app.log      # General application logs
logs/error.log    # Error logs only
```

### **Health Checks**
- **Application**: `http://your-domain:8501/_stcore/health`
- **Docker**: Built-in health check configured
- **Monitoring**: Set up alerts for API quota limits

### **Performance Monitoring**
```bash
# Monitor resource usage
docker stats

# Check API usage
# Monitor Gemini API quota in Google AI Studio
# Monitor Spoonacular usage in dashboard
```

## 🔒 Security Best Practices

### **API Key Management**
- ✅ Store in environment variables
- ✅ Use different keys for dev/staging/prod
- ✅ Rotate keys regularly
- ✅ Monitor API usage for anomalies

### **Network Security**
- ✅ Use HTTPS in production
- ✅ Configure rate limiting
- ✅ Set up firewall rules
- ✅ Use reverse proxy (Nginx)

### **Application Security**
- ✅ Input validation on all uploads
- ✅ File size limits enforced
- ✅ Security headers configured
- ✅ Regular dependency updates

## 🚨 Troubleshooting

### **Common Issues**

**1. API Quota Exceeded**
```bash
# Check logs for quota errors
grep "quota" logs/app.log

# Solution: Wait for quota reset or upgrade plan
```

**2. Image Upload Fails**
```bash
# Check file size and format
# Supported: JPG, PNG, WebP, HEIC (max 20MB)
```

**3. Container Won't Start**
```bash
# Check environment variables
docker-compose config

# Check logs
docker-compose logs fridgevision
```

**4. High Memory Usage**
```bash
# Monitor memory
docker stats

# Restart if needed
docker-compose restart fridgevision
```

### **Performance Optimization**

**1. Image Processing**
- Resize large images before upload
- Use appropriate image formats
- Implement client-side compression

**2. API Optimization**
- Cache recipe results
- Implement request batching
- Use CDN for static assets

**3. Scaling**
```yaml
# docker-compose.yml
services:
  fridgevision:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

## 📈 Scaling for Production

### **Horizontal Scaling**
```bash
# Scale to multiple instances
docker-compose up --scale fridgevision=3

# Use load balancer
# Configure session affinity if needed
```

### **Database Integration**
```python
# Optional: Add database for user data
# PostgreSQL, MongoDB, or Redis for caching
```

### **CDN Integration**
- Use CloudFlare, AWS CloudFront, or similar
- Cache static assets
- Reduce server load

## 🔄 CI/CD Pipeline

The included GitHub Actions workflow provides:
- ✅ Automated testing
- ✅ Security scanning
- ✅ Docker image building
- ✅ Deployment automation

### **Setup GitHub Secrets**
```
DOCKERHUB_USERNAME=your_username
DOCKERHUB_TOKEN=your_token
GEMINI_API_KEY=your_key
SPOONACULAR_API_KEY=your_key
```

## 📞 Support & Maintenance

### **Regular Maintenance**
- [ ] Update dependencies monthly
- [ ] Monitor API usage and costs
- [ ] Review logs for errors
- [ ] Update SSL certificates
- [ ] Backup configuration and data

### **Monitoring Alerts**
Set up alerts for:
- High error rates
- API quota approaching limits
- High memory/CPU usage
- SSL certificate expiration

---

## 🎯 Quick Production Checklist

**Before Going Live:**
- [ ] All tests passing
- [ ] Security scan completed
- [ ] API keys configured
- [ ] HTTPS enabled
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Documentation updated

**Post-Deployment:**
- [ ] Health checks working
- [ ] Logs being collected
- [ ] Performance monitoring active
- [ ] User feedback system ready

---

**Need Help?** Check the [README.md](README.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md) for additional information.
