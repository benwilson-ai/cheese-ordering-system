# Cheeses Ordering AI Assistant

A Streamlit-based chatbot application powered by OpenAI that helps users analyze and understand retail cheese data. The application combines vector similarity search and SQL querying capabilities to provide comprehensive insights about retail cheeses.

## Features

- 📊 CSV file upload and processing
- 💬 Interactive chat interface
- 📈 Data visualization capabilities
- 🔍 Hybrid search (SQL + Vector) for cheese information
- 🤖 AI-powered natural language understanding
- 📋 Comprehensive cheese data management

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Databases**:
  - MySQL (Structured data storage)
  - Pinecone (Vector database for semantic search)
- **AI/ML**:
  - OpenAI GPT-4
  - LangChain
  - LangGraph

## Prerequisites

- Python 3.8+
- MySQL Server (We used [Aiven sql database](https://aiven.io/) for this project)
- Pinecone Account
- OpenAI API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chai-dev682/hybrid_retail_lease.git
cd hybrid_retail_lease
```

2. Create a virtual environment:
```bash
python -m virtualenv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables with your own API keys:
```bash
cp .env.example .env
```


## Project Structure

```README.MD
├── app/
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   ├── logging.py         # Logging setup
│   │   └── prompt_templates/  # LLM prompt templates
│   ├── db/
│   │   ├── mysql.py          # MySQL database service
│   │   └── vectordb.py       # Pinecone vector database service
│   ├── schemas/
│   │   └── retail_lease.py   # Data models
│   └── services/
│       ├── chat.py           # Chat service
│       ├── upload.py         # File upload service
│       └── graph/            # LangGraph workflow
├── main.py                   # Application entry point
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables
└── README.md                 # README file
```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Upload a CSV file containing retail lease data through the sidebar.

3. Interact with the chatbot by asking questions about the retail leases. Example queries:
   - "What is the average rent in Townsville Shopping Centre?"
   - "Show me all beauty stores in the database"
   - "Compare rent prices across different tenant categories"

## Features in Detail

### Data Upload
The application supports CSV file upload with automatic encoding detection and data processing. The data is simultaneously stored in:
- MySQL for structured queries
- Pinecone for semantic search capabilities

### Chat Interface
The chat interface uses a sophisticated workflow powered by LangGraph to:
1. Transform user queries into appropriate database queries
2. Determine the best database to use (MySQL or Pinecone)
3. Execute queries and retrieve relevant data
4. Generate natural language responses
5. Create visualizations when appropriate

### Visualization
The system automatically determines the best visualization type based on the query and data:
- Bar charts for comparisons
- Line charts for trends
- Tables for detailed data views

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.