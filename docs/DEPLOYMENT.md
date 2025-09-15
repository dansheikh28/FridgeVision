# 🚀 Deployment Guide

This guide covers how to deploy FridgeVision to various platforms.

## Streamlit Cloud Deployment

### Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Spoonacular API key

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Initial FridgeVision implementation"
   git push origin main
   ```

2. **Create `secrets.toml` for Streamlit Cloud**:
   Create `.streamlit/secrets.toml` in your repo:
   ```toml
   [general]
   SPOONACULAR_API_KEY = "your_api_key_here"
   MODEL_PATH = "models/trained/food_yolo.pt"
   CONFIDENCE_THRESHOLD = 0.5
   IOU_THRESHOLD = 0.45
   ```

3. **Add required files**:
   Ensure these files are in your repository root:
   - `requirements.txt`
   - `src/app/main.py` (main Streamlit app)
   - Model files in `models/trained/`

### Step 2: Deploy to Streamlit Cloud

1. **Connect your repository**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select your repository

2. **Configure deployment**:
   - **Main file path**: `src/app/main.py`
   - **Python version**: 3.8+
   - **Branch**: main

3. **Add secrets**:
   - In the Streamlit Cloud dashboard
   - Go to app settings → Secrets
   - Paste your `secrets.toml` content

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://your-app-name.streamlit.app`

### Step 3: Configure Custom Domain (Optional)

1. **Purchase domain** (e.g., from Namecheap, GoDaddy)
2. **Set up DNS**:
   - Add CNAME record pointing to your Streamlit app
3. **Configure in Streamlit Cloud**:
   - App settings → General → Custom domain

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Prepare for Heroku

1. **Create `Procfile`**:
   ```
   web: streamlit run src/app/main.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `runtime.txt`**:
   ```
   python-3.9.16
   ```

3. **Update `requirements.txt`** with additional dependencies:
   ```
   streamlit>=1.28.0
   gunicorn>=21.0.0
   ```

### Step 2: Deploy to Heroku

1. **Login to Heroku**:
   ```bash
   heroku login
   ```

2. **Create Heroku app**:
   ```bash
   heroku create your-fridgevision-app
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set SPOONACULAR_API_KEY=your_api_key_here
   heroku config:set MODEL_PATH=models/trained/food_yolo.pt
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Heroku deployment"
   git push heroku main
   ```

5. **Open your app**:
   ```bash
   heroku open
   ```

## AWS EC2 Deployment

### Prerequisites
- AWS account
- EC2 instance (t3.medium or larger recommended)
- Domain name (optional)

### Step 1: Set Up EC2 Instance

1. **Launch EC2 instance**:
   - Ubuntu 20.04 LTS
   - t3.medium (2 vCPU, 4GB RAM)
   - Security group allowing HTTP (80), HTTPS (443), SSH (22)

2. **Connect to instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

### Step 2: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git -y

# Install nginx (for reverse proxy)
sudo apt install nginx -y

# Clone your repository
git clone https://github.com/your-username/fridgevision.git
cd fridgevision

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure Application

1. **Set environment variables**:
   ```bash
   cp config.env.example config.env
   # Edit config.env with your API keys
   nano config.env
   ```

2. **Download models**:
   ```bash
   python scripts/download_model.py
   ```

### Step 4: Set Up Service

1. **Create systemd service**:
   ```bash
   sudo nano /etc/systemd/system/fridgevision.service
   ```

   Content:
   ```ini
   [Unit]
   Description=FridgeVision Streamlit App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/fridgevision
   Environment=PATH=/home/ubuntu/fridgevision/venv/bin
   ExecStart=/home/ubuntu/fridgevision/venv/bin/streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable fridgevision
   sudo systemctl start fridgevision
   ```

### Step 5: Configure Nginx

1. **Create nginx configuration**:
   ```bash
   sudo nano /etc/nginx/sites-available/fridgevision
   ```

   Content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

2. **Enable site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/fridgevision /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Step 6: Set Up SSL (Optional)

1. **Install certbot**:
   ```bash
   sudo apt install snapd
   sudo snap install core; sudo snap refresh core
   sudo snap install --classic certbot
   sudo ln -s /snap/bin/certbot /usr/bin/certbot
   ```

2. **Get SSL certificate**:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download models
RUN python scripts/download_model.py

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
ENTRYPOINT ["streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  fridgevision:
    build: .
    ports:
      - "8501:8501"
    environment:
      - SPOONACULAR_API_KEY=${SPOONACULAR_API_KEY}
      - MODEL_PATH=models/trained/food_yolo.pt
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    restart: unless-stopped
```

### Deploy with Docker

```bash
# Build image
docker build -t fridgevision .

# Run container
docker run -p 8501:8501 \
  -e SPOONACULAR_API_KEY=your_api_key \
  fridgevision

# Or use docker-compose
docker-compose up -d
```

## Performance Optimization

### 1. Model Optimization
- Use model quantization for faster inference
- Implement model caching
- Use GPU acceleration when available

### 2. Application Optimization
- Implement session state caching
- Optimize image processing pipeline
- Use async operations for API calls

### 3. Infrastructure Optimization
- Use CDN for static assets
- Implement load balancing for high traffic
- Set up monitoring and alerting

## Monitoring and Maintenance

### Health Checks
```python
# Add to your Streamlit app
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Monitoring Tools
- **Streamlit Cloud**: Built-in analytics
- **Heroku**: Heroku Metrics
- **AWS**: CloudWatch
- **Custom**: Prometheus + Grafana

## Troubleshooting

### Common Issues

1. **Model loading errors**:
   - Check model file paths
   - Verify model compatibility
   - Ensure sufficient memory

2. **API timeouts**:
   - Implement retry logic
   - Check API rate limits
   - Use caching for frequent requests

3. **Memory issues**:
   - Optimize image processing
   - Implement garbage collection
   - Use streaming for large files

4. **Slow performance**:
   - Enable model caching
   - Optimize inference pipeline
   - Use appropriate instance size

### Getting Help

- Check application logs
- Monitor resource usage
- Use debugging tools
- Consult platform documentation
