# langchain-demo

A Python project that uses the LangChain framework and different Chat models to demo langchain capabilities.

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Your Python Environment**

   Ensure you have Python 3.13.2 installed.

   This project uses Pipenv for dependency management. Install the dependencies with:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Environment Variables**

   Create a `.env` file in the root directory and configure any required environment variables.

## Usage

To execute the information processing script:

```bash
python [python_file]
```

The script will process the provided information and stream output to the console.

## Docker Compose

A `docker-compose.yml` file is included if you require additional services (e.g., model serving or a web UI) in your workflow. To start the services defined in Docker Compose:

```bash
docker-compose up -d
```

## Dependencies

The project relies on the following primary packages:

- `langchain`
- `langchain-community`
- `langchain-openai`
- `langchainhub`
- `python-dotenv`
- `rich`
- `black` (for code formatting)

All dependencies are listed in the Pipfile.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions, please open an issue or a pull request.

## License

This project is provided for educational purposes. Please update this section with your chosen license.