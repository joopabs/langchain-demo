# langchain-demo

A Python project that uses the LangChain framework and various Chat models to demo LangChain capabilities.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Docker Compose and Containerized Services](#docker-compose-and-containerized-services)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Your Python Environment**

   Ensure you have Python 3.13.2 installed. This project uses Pipenv for dependency management. Install the dependencies with:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Environment Variables**

   Create a `.env` file in the root directory and configure any required environment variables.

## Usage

To execute the information processing script, run:

```bash
python [python_file]
```

The script will process the provided information and stream the output to the console.

## Docker Compose and Containerized Services

For those who require additional services such as model serving or a web UI, a `docker-compose.yml` file has been included. This configuration sets up an Ollama container with specific resource allocations:

- **Ollama Service Details:**
   - **Image:** Uses the Ollama image.
   - **Resource Limits:**
      - CPUs: 16 (of 24 available cores)
      - Memory: 24GB
   - **Resource Reservations:**
      - CPUs: 8
      - Memory: 16GB
      - GPU: Configured to use an NVIDIA GPU (if available)
   - **Restart Policy:** Always

To start the services defined in Docker Compose, run:

```bash
docker-compose up -d
```

To pull and run a model inside the Ollama container (for example, "llama3"), execute:

```bash
docker exec -it ollama ollama run llama3
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

This project is licensed under the GPL.