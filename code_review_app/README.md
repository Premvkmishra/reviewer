# AI Code Review Application

An AI-powered code review application that analyzes code for bugs, vulnerabilities, and quality issues using Hugging Face models.

## Features

- 🔍 **Code Analysis**: Analyze code snippets for bugs, vulnerabilities, and quality issues
- 📁 **File Upload**: Upload code files for analysis with automatic language detection
- 🌐 **Web Interface**: Modern React frontend with real-time analysis
- 🔗 **GitHub Integration**: Webhook support for automatic PR analysis
- 📊 **Detailed Reports**: Markdown-formatted analysis with actionable insights

## Backend Setup

### Prerequisites

- Python 3.8+
- Hugging Face API token
- (Optional) GitHub Personal Access Token for webhooks

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd code_review_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env with your credentials
   ```

4. **Required Environment Variables:**
   - `HF_API_TOKEN`: Your Hugging Face API token
   - `GITHUB_TOKEN`: GitHub Personal Access Token (optional)
   - `WEBHOOK_SECRET`: Secret for webhook verification (optional)

### Running the Backend

```bash
python start.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `POST /api/analyze` - Analyze code snippet
- `POST /api/analyze-file` - Analyze uploaded file
- `GET /api/supported-languages` - Get supported programming languages
- `POST /api/webhook` - GitHub webhook endpoint
- `GET /health` - Health check

## Frontend Setup

### React Frontend Specifications

The frontend should be built with the following specifications:

#### Core Features
1. **Code Input Section**
   - Large text area for pasting code
   - Language selector dropdown
   - Syntax highlighting for common languages
   - Character count and validation

2. **File Upload Section**
   - Drag & drop file upload
   - File type validation
   - Progress indicator
   - Support for common code file extensions

3. **Analysis Results**
   - Markdown rendering of analysis results
   - Syntax highlighting for code snippets in results
   - Collapsible sections for different analysis categories
   - Copy-to-clipboard functionality

4. **UI/UX Requirements**
   - Modern, clean design with dark/light theme toggle
   - Responsive design for mobile and desktop
   - Loading states and error handling
   - Toast notifications for user feedback

#### Technical Requirements
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS or styled-components
- **State Management**: React Context or Zustand
- **HTTP Client**: Axios or fetch API
- **Markdown**: react-markdown with syntax highlighting
- **File Upload**: react-dropzone
- **Icons**: Lucide React or Heroicons

#### API Integration
- Base URL: `http://localhost:8000/api`
- Endpoints to integrate:
  - `POST /analyze` - For code snippet analysis
  - `POST /analyze-file` - For file upload analysis
  - `GET /supported-languages` - For language options

#### Component Structure
```
src/
├── components/
│   ├── CodeEditor/
│   ├── FileUpload/
│   ├── AnalysisResults/
│   ├── LanguageSelector/
│   └── common/
├── hooks/
│   ├── useCodeAnalysis.ts
│   └── useFileUpload.ts
├── services/
│   └── api.ts
├── types/
│   └── index.ts
└── utils/
    └── helpers.ts
```

## Getting Hugging Face API Token

1. Go to [Hugging Face](https://huggingface.co/)
2. Create an account or sign in
3. Go to Settings → Access Tokens
4. Create a new token with "read" permissions
5. Copy the token and add it to your `.env` file

## Getting GitHub Token (Optional)

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` and `write:discussion` permissions
3. Add it to your `.env` file

## Usage

1. **Start the backend:**
   ```bash
   python start.py
   ```

2. **Start the React frontend:**
   ```bash
   # After creating the React app
   npm start
   ```

3. **Use the application:**
   - Paste code in the text area or upload a file
   - Select the programming language (optional)
   - Click "Analyze" to get AI-powered feedback
   - View detailed analysis with security, bug, and quality insights

## API Response Format

```json
{
  "markdown_feedback": "Detailed analysis in markdown format",
  "language_detected": "Python",
  "analysis_time": 2.5,
  "code_length": 150
}
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid API tokens
- Rate limiting
- File size limits
- Unsupported file types
- Network timeouts
- Model loading issues

## Development

### Adding New Languages

1. Update the `allowed_extensions` list in `analyze.py`
2. Add language mapping in the file upload endpoint
3. Update the supported languages endpoint

### Customizing Analysis

1. Modify the prompt in `huggingface.py`
2. Adjust model parameters (temperature, max_length)
3. Add custom analysis rules in the fallback function

## Troubleshooting

- **API Token Issues**: Ensure your Hugging Face token is valid and has proper permissions
- **CORS Errors**: Check that the frontend URL is in the allowed origins list
- **File Upload Issues**: Verify file size and type restrictions
- **Model Loading**: Some models may take time to load on first request

## License

MIT License 