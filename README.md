# Anidong API

Anidong API is a powerful and open-source RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) that provides information about Anime and Donghua. It compiles data from various sources to provide a unified interface for developers.

## 🚀 Features

- **Anime & Donghua Data**: Comprehensive endpoints to search and retrieve details about Anime and Donghua.
- **Fast & Async**: Built on top of Starlette and Pydantic for high performance.
- **Documentation**: Automatic interactive API documentation via Swagger UI.
- **Rate Limiting**: Built-in rate limiting support (requires Redis).
- **Docker Support**: Easy deployment using Docker and Docker Compose.
- **Monitoring**: Stats and logging middleware included.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Data Parsing**: BeautifulSoup4, lxml
- **Caching/Rate Limiting**: Redis
- **HTTP Client**: HTTPX, Aiohttp

## 📋 Prerequisites

- Python 3.10+
- Redis Server (for rate limiting)
- Docker & Docker Compose (optional, for containerized deployment)

## 🔧 Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone git@github.com:zhadevv/anidong-api.git
   cd anidong-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   Create a `.env` file in the root directory (optional, defaults are set in code):
   ```env
   host=0.0.0.0
   port=8008
   debug=True
   REDIS_URL=redis://localhost:6379/0
   ```
   *Make sure you have a Redis instance running locally if you want to enable all features.*

5. **Run the application**
   ```bash
   python start.py
   ```
   The API will be available at `http://localhost:8008`.

### 🐳 Docker Deployment

The easiest way to run the project is using Docker Compose, which handles the Redis dependency automatically.

1. **Build and Run**
   ```bash
   docker-compose up -d --build
   ```

2. **Access the API**
   - API Root: `http://localhost:8008/`
   - Documentation: `http://localhost:8008/docs`

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc` (if enabled)

### Key Endpoints
- `GET /api/v1/anime`: Search/List Anime
- `GET /api/v1/donghua`: Search/List Donghua
- `GET /api/v1/keycheck`: Check API Key validity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Credits

- **Contributors**: [Yughoz](https://github.com/yughoz)
- **Inspiration**: Sanka

---
*Made with ♥️ for the Weeb community.*
