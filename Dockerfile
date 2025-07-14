# Dockerfile - for the Streamlit frontend app

FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /src

# Copy only required files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync

# Copy client source code
COPY src ./src

# Expose port used by Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["uv", "run", "streamlit", "run", "src/main.py", "--server.address", "0.0.0.0"]