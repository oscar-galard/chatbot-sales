# Sales Chatbot for Guitar Classes

A sales chatbot application built with Clean Architecture using FastAPI, Uvicorn, and OpenAI/DeepSeek APIs. This chatbot guides customers through a sales process and appointment scheduling for guitar classes.

## Features

- Clean Architecture implementation with separation of concerns
- Natural Language Processing using OpenAI or DeepSeek APIs
- RESTful API with FastAPI
- Interactive web UI and command-line interface
- Session-based conversation management
- Sales process with lead qualification and appointment scheduling

## Prerequisites

- Python 3.8 or higher
- An API key from either:
  - OpenAI (https://platform.openai.com/api-keys)
  - DeepSeek (https://platform.deepseek.com/)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chatbot-sales
   ```

2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   If requirements.txt doesn't exist, install the required packages directly:
   ```bash
   pip install fastapi uvicorn openai python-dotenv instructor
   ```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API key:
   ```env
   # Set MODEL_PROVIDER to either "openai" or "deepseek"
   MODEL_PROVIDER=openai

   # OpenAI API Configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # DeepSeek API Configuration
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

## Running the Application

### Start the API Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Access the Web Interface

Open `chat-ui/chat.html` in your browser to use the web-based chat interface.

### Using the Command Line Interface

Run the interactive shell script:
```bash
cd chat-ui
chmod +x interact_api.sh
./interact_api.sh
```

## API Endpoints

### POST /api/v1/lead

Process a user message and return the chatbot response.

**Request Body:**
```json
{
  "session_id": "unique-session-identifier",
  "message": "User's message"
}
```

**Response:**
```json
{
  "session_id": "unique-session-identifier",
  "response": "Bot's response message",
  "phase": "current-conversation-phase",
  "data": { }
}
```

## Project Structure

```
chatbot-sales/
├── main.py                 # Application entry point
├── .env                    # Environment variables
├── .env.example           # Example environment file
├── requirements.txt       # Python dependencies
├── wah_sales_api/         # Main application package
│   ├── domain/            # Domain models and business rules
│   ├── application/       # Application services and use cases
│   ├── infrastructure/    # External services (NLP, storage)
│   └── presentation/      # API endpoints and interfaces
└── chat-ui/               # User interfaces
    ├── chat.html          # Web-based chat interface
    └── interact_api.sh    # Command-line interface
```

## Conversation Flow

1. **Introduction**: Bot greets user and asks for information about who the classes are for and their age
2. **Motivation**: Bot asks about the reason for learning guitar
3. **Time Availability**: Bot asks about weekly time availability
4. **Plan Recommendation**: Bot analyzes the profile and recommends a suitable plan
5. **Sales Pitch**: Bot presents a personalized sales pitch for the recommended plan
6. **Appointment Scheduling**: If user is interested, bot collects contact information for scheduling
7. **Closure**: Conversation ends with appointment confirmation or polite goodbye

## Development

### Adding New Features

The Clean Architecture makes it easy to extend the application:

1. **Domain Layer**: Add new models in `domain/models.py`
2. **Application Layer**: Add new services in `application/services.py`
3. **Infrastructure Layer**: Add new external service integrations in `infrastructure/`
4. **Presentation Layer**: Add new endpoints in `presentation/api.py`

### Testing

Run the FastAPI development server with auto-reload:
```bash
uvicorn main:app --reload
```

## Troubleshooting

### Common Issues

1. **API Key Not Set**: Make sure you've configured your API key in the `.env` file
2. **Module Not Found**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Already in Use**: Change the port in `main.py` or use a different port with uvicorn

### Getting Help

If you encounter any issues, please check:
1. All environment variables are correctly set
2. Dependencies are properly installed
3. The API service is running before using the interfaces

## License

This project is licensed under the MIT License - see the LICENSE file for details.