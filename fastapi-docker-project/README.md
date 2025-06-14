# fastapi-docker-project/fastapi-docker-project/README.md

# FastAPI Docker Project

This project is a FastAPI application that provides a visualization API. It allows users to submit questions and receive generated visualizations in the form of video files.

## Project Structure

```
fastapi-docker-project
├── app
│   ├── main.py          # Contains the FastAPI application and endpoint definitions
│   ├── modular.py       # Contains the logic for processing visualization requests
│   └── __init__.py      # Marks the app directory as a Python package
├── Dockerfile            # Instructions to build the Docker image for the application
├── requirements.txt      # Lists the Python dependencies required for the project
├── .dockerignore         # Specifies files to ignore when building the Docker image
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-docker-project
   ```

2. **Build the Docker image:**
   ```
   docker build -t fastapi-docker-project .
   ```

3. **Run the Docker container:**
   ```
   docker run -d -p 8000:8000 fastapi-docker-project
   ```

4. **Access the API:**
   Open your browser and go to `http://localhost:8000/docs` to view the API documentation and test the endpoints.

## Usage

To create a visualization, send a POST request to the `/visualise/` endpoint with a JSON body containing the question. For example:

```json
{
  "question": "What is the significance of the Pythagorean theorem?"
}
```

The response will include the generated video file if successful.

## Dependencies

The project requires the following Python packages:

- FastAPI
- Uvicorn
- Pydantic

These dependencies are listed in the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.