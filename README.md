# CRM Chatbot Assistant

A modern CRM chatbot application built with FastAPI backend and Streamlit frontend, connected to MongoDB Atlas for lead management.

## Features

- 🤖 Natural language query processing for CRM data
- 🏢 Lead management with MongoDB Atlas integration
- 📊 Real-time lead statistics and filtering
- 🎨 Modern, responsive UI with Streamlit
- 🚀 RESTful API with FastAPI
- 🔍 Advanced search capabilities

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **Database**: MongoDB Atlas
- **Authentication**: Environment variables
- **Deployment Ready**: Docker support

## Quick Start

### Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/crm-chatbot-assistant.git
   cd crm-chatbot-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB credentials
   ```

5. **Initialize database**
   ```bash
   python setup_mongodb.py
   ```

6. **Run the application**
   ```bash
   # Start backend
   python backend/main.py

   # In another terminal, start frontend
   streamlit run frontend/app.py
   ```

## Environment Variables

Create a `.env` file in the root directory:

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=crmdb
COLLECTION_NAME=leads
```

## API Endpoints

- `GET /` - Health check
- `POST /chat/` - Process natural language queries
- `GET /leads` - Get all leads
- `GET /health` - System health status

## Example Queries

- "Show leads from Delhi"
- "How many converted leads?"
- "Show all interested leads"
- "Highest converted lead by city"

## Project Structure

```
crm-chatbot-assistant/
├── backend/
│   ├── main.py
│   ├── chatbot.py
│   ├── database.py
│   ├── schemas.py
│   └── seed_leads.py
├── frontend/
│   └── app.py
├── data/
│   └── demo_leads.json
├── .env
├── .gitignore
├── requirements.txt
├── setup_mongodb.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
