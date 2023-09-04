# API Images

**Summary**

The goal of this project is to create an HTTP API for uploading, optimizing, and serving images. The API follows a modern architecture and leverages tools like RabbitMQ, Celery, and AWS S3 for efficient image processing and storage.

## Features

1. **Image Upload and Optimization**:
   - The API exposes an endpoint for uploading images.
   - Uploaded images are sent for optimization asynchronously via a RabbitMQ queue to prevent system overload during concurrent uploads.
   - Each original image is optimized to generate three smaller-size variants with 75%, 50%, and 25% quality.

2. **Image Download**:
   - The API provides an endpoint for downloading images by ID.
   - Users can specify the desired image quality using query parameters (e.g., `?quality=100/75/50/25`).

## Technology Stack

- **Framework**: FastAPI
- **Message Broker**: RabbitMQ
- **Task Queue**: Celery
- **Storage**: AWS S3
- **Docker**: Containerization

## Project Structure

The project follows good software development practices, including SOLID principles and separation of concerns. It's organized into the following main components:

- `src/main.py`: Defines the FastAPI endpoints for image upload and download.
- `src/repository.py`: Manages interactions with AWS S3 for image storage.
- `src/service.py`: Implements the image processing and optimization logic.
- `src/tasks.py`: Configures Celery for asynchronous task execution.
- `src/utils.py`: Contains utility functions for image processing.

## Getting Started

1. **Prerequisites**:
   - Docker: Ensure you have Docker installed on your system.

2. **Clone the Repository**:
```shell
git clone https://github.com/inrock1/API-images.git
cd API-images
```
3. **Put your credentials**:
   - rename .env.sample to .env and put your credentials in it.
   - If you don't have ~/.aws/credentials file, rename the `aws_config_sample` file to `config` and put your AWS S3 credentials in it.

4.**Build and Run the Docker Containers**:
```shell
docker-compose up --build
```

5.**Access the API**:
- The API will be available at `http://localhost:80` by default.
- Use `http://localhost:80/docs` to interact with the API endpoints.

## Testing

- The project includes unit tests for its functionality. You can run tests using the following command:
```shell
docker-compose exec app pytest
```

## Contributing

Contributions to this project are welcome! Feel free to submit issues or pull requests to improve the code or add new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

