# Excel Combination Generator

A FastAPI web application that generates all possible combinations from selected Excel columns while preserving original data structure.

## Features

- 📊 Upload Excel files (.xlsx, .xls)
- 🔍 Automatically detect and preview columns
- 🎯 Select specific columns for combination generation
- 📁 Custom output directory and filename selection
- 💾 Download generated Excel files
- 🔄 Preserves original data in unselected columns

## How It Works

1. **Upload Excel File**: Select your Excel file through the web interface
2. **Preview Data**: View sample data and available columns
3. **Select Columns**: Choose which columns to generate combinations for
4. **Set Output**: Specify output directory and filename
5. **Generate**: Create all possible combinations
6. **Download**: Get your result file

## Example

If you have data like:
```
| Name | Age | City | State |
|------|-----|------|-------|
| John | 25  | NYC  | NY    |
| Jane | 30  | LA   | CA    |
```

And select `City` and `State` for combinations, you'll get:
```
| Name | Age | City | State |
|------|-----|------|-------|
| John | 25  | NYC  | NY    |
| John | 25  | NYC  | CA    |
| John | 25  | LA   | NY    |
| John | 25  | LA   | CA    |
| Jane | 30  | NYC  | NY    |
| Jane | 30  | NYC  | CA    |
| Jane | 30  | LA   | NY    |
| Jane | 30  | LA   | CA    |
```

## Installation & Running

### Local Development

```bash
# Clone the repository
git clone https://github.com/ksrinu11/excel-combination-generator.git
cd excel-combination-generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Visit `http://localhost:8000` to use the application.

### Docker Deployment

```bash
# Build Docker image
docker build -t excel-combination-generator .

# Run container
docker run -p 8000:8000 excel-combination-generator
```

## Deployment

This application can be deployed on various platforms:

- **Heroku**: Use the included `Procfile`
- **Railway**: Direct deployment from GitHub
- **Render**: Web service deployment
- **Docker**: Containerized deployment
- **VPS**: Traditional server deployment

## Project Structure

```
├── main.py              # FastAPI application
├── templates/
│   └── index.html       # Web interface
├── uploads/             # Temporary file storage
├── outputs/             # Generated files
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── Procfile           # Heroku configuration
└── README.md          # This file
```

## API Endpoints

- `GET /` - Web interface
- `POST /upload` - Generate combinations
- `POST /get-columns` - Get Excel file columns
- `GET /download/{directory}/{filename}` - Download generated files

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas
- **Excel Handling**: OpenPyXL
- **Deployment**: Docker, Uvicorn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please create an issue in the GitHub repository.