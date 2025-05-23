# Database Query Assistant

A natural language to SQL query converter powered by Google's Gemini AI and Streamlit. This application allows users to query databases using plain English, which gets converted to SQL and executed against your database.

## Features

- Natural language to SQL conversion using Gemini AI
- Support for multiple database types (MySQL, PostgreSQL, SQLite)
- Interactive web interface built with Streamlit
- Real-time query execution and result display
- Database schema visualization
- Secure credential handling

## Prerequisites

- Python 3.8+
- A Google API key for Gemini AI
- Access to a database (MySQL, PostgreSQL, or SQLite)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app4.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter your database connection details:
   - Select database type
   - Enter credentials
   - Click "Connect to Database"

4. Once connected, you can:
   - Ask questions in plain English
   - View the generated SQL
   - See query results in a table format

## Deployment

This application requires a Python backend and cannot be hosted on static hosting platforms like GitHub Pages. Consider deploying on:

- [Streamlit Cloud](https://streamlit.io/cloud)
- [Heroku](https://heroku.com)
- [DigitalOcean](https://digitalocean.com)
- [AWS](https://aws.amazon.com)

## Security Notes

- Never commit your `.env` file or expose your API keys
- Use environment variables for sensitive information
- Implement proper authentication before deploying publicly
- Consider database connection security in production

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 