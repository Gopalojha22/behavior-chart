# Behavior Chart 📊

A modern Flask web application for visualizing investment behavior and performance comparison through interactive animated charts. Upload CSV files, customize visualizations, and record chart animations as videos.

## ✨ Features

- **📁 CSV File Upload**: Upload any two CSV files with historical data for comparison
- **🎨 Field Customization**: Select X/Y axis fields, dataset names, and colors
- **📈 Interactive Charts**: Dynamic visualization using Chart.js with smooth animations
- **🎥 Video Recording**: Auto-record chart animations and download as video files
- **💰 Lakhs Formatting**: Indian number format (1.0L, 23.3L) for financial data
- **📱 Responsive Design**: Works on desktop and mobile devices
- **⚡ Animation Speed Control**: Adjust chart animation speed (Very Slow to Instant)
- **🔄 Default Year Axis**: Auto-generate year sequences for datasets without dates

## 🚀 Live Demo

[View Live Demo](https://behavior-chart-orpin.vercel.app/)

## 📋 CSV File Format

Your CSV files should have headers in the first row:

```csv
Month,PortfolioValue
2014-01,10000
2014-02,20307.82
2014-03,31690.10
```

**Supported formats:**
- **Dates**: YYYY-MM, MM/DD/YYYY, DD/MM/YYYY, YYYY
- **Numbers**: Plain numbers, with commas (10,000), with currency symbols (₹10,000)
- **Any CSV structure** with numeric data columns

## 🛠️ Installation & Local Development

### Prerequisites
- Python 3.8+
- Git

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/OjhaGopal/behavior-chart.git
cd behavior-chart
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run locally:**
```bash
python app.py
```

5. **Open browser:** `http://localhost:5000`

## 🌐 Production Deployment

### Deploy to Vercel (Recommended)

1. **Fork this repository**
2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your forked repository
   - Deploy automatically

3. **Features on Vercel:**
   - ✅ Client-side CSV processing
   - ✅ No server storage needed
   - ✅ Fast global CDN
   - ✅ Automatic HTTPS

### Deploy to Railway

1. **Connect repository to Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect GitHub repository
   - Deploy automatically

2. **Features on Railway:**
   - ✅ Full server functionality
   - ✅ File upload support
   - ✅ Persistent storage

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

## 🎯 How to Use

### 1. Upload CSV Files
- Click "Upload CSV Files"
- Select two CSV files for comparison
- Files are processed in your browser (no server upload)

### 2. Configure Chart
- **Select X-axis field** or use "Default Year Sequence"
- **Select Y-axis fields** for both datasets
- **Customize names and colors** for each dataset
- **Choose animation speed** (Very Slow to Instant)

### 3. View & Record Chart
- Chart animates automatically on page load
- **Recording starts automatically** when chart loads
- **Click "Stop Recording"** to download video
- Video saves as `.webm` or `.mp4` format

## 🎥 Video Recording Features

- **Auto-start recording** when chart page loads
- **High-quality output** (60 FPS, 5+ Mbps bitrate)
- **Clean background** (no black borders)
- **Multiple formats** (WebM VP9, WebM VP8, MP4)
- **One-click download** when recording stops

## 🔧 Technical Features

### Frontend
- **Chart.js** for interactive visualizations
- **MediaRecorder API** for video recording
- **localStorage** for client-side data storage
- **Responsive CSS** with modern design

### Backend
- **Flask** lightweight web framework
- **Client-side processing** for Vercel compatibility
- **Secure file handling** with validation
- **Cross-platform support**

### Browser Compatibility
- **Chrome/Edge**: Full video recording support
- **Firefox**: WebM recording support
- **Safari**: Basic functionality (limited recording)

## 📊 Sample Data

The app includes sample datasets:
- **Nifty 50 vs Nifty Next 50** comparison
- **Monthly portfolio values** from 2014-2025
- **Indian Rupee formatting** with lakhs display

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Chart.js** for excellent charting library
- **Flask** for lightweight web framework
- **Vercel** for seamless deployment platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/OjhaGopal/behavior-chart/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OjhaGopal/behavior-chart/discussions)

---

**Made with ❤️ for investment analysis and data visualization**