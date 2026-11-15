# Enterprise AI Knowledge Assistant

An AI-powered knowledge assistant that allows users to upload company PDF documents and ask questions about their contents using Retrieval-Augmented Generation (RAG).

## Project Overview

The Enterprise AI Knowledge Assistant helps employees retrieve information from company documents quickly using an AI-based question-answering system.

Users can upload PDF files, extract their text, store document chunks in a vector database, and ask questions using natural language.

## Key Features

- Upload PDF documents.
- Extract text from PDF files.
- Split documents into smaller chunks.
- Generate embeddings and store chunks in ChromaDB.
- Retrieve relevant document content using semantic search.
- Generate AI answers using Google Gemini.
- Web-based interface using Streamlit.
- Containerization using Docker.
- Kubernetes deployment configuration.
- Prometheus metrics instrumentation.
- GitHub Actions CI workflow.

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| PDF Processing | PyMuPDF |
| Vector Database | ChromaDB |
| AI Model | Google Gemini |
| Containerization | Docker |
| Orchestration | Kubernetes, Minikube |
| CI | GitHub Actions |
| Metrics | Prometheus Client |

## Project Architecture

1. User uploads a PDF through Streamlit.
2. PyMuPDF extracts text from the PDF.
3. Extracted text is divided into smaller chunks.
4. ChromaDB stores document chunks and embeddings.
5. User submits a question.
6. ChromaDB retrieves relevant document chunks.
7. Retrieved context is sent to Google Gemini.
8. Gemini generates an answer.
9. Streamlit displays the answer to the user.

## Project Structure

```text
enterprise-ai-assistance/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── pvc.yaml
│
├── app.py
├── pdf_processor.py
├── rag_pipeline.py
├── metrics.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ankitbaghel9975/enterprise-ai-assistant.git
cd enterprise-ai-assistance
```

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Never upload your actual API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open:

http://localhost:8501

## Docker

Build the Docker image:

```bash
docker build -t enterprise-ai-assistant:v1 .
```

Run the container:

```bash
docker run -p 8501:8501 --env-file .env enterprise-ai-assistant:v1
```

## Kubernetes Deployment

The project includes Kubernetes manifests for:

- Deployment
- NodePort Service
- Persistent Volume Claim

Apply the manifests:

```bash
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check deployment status:

```bash
kubectl get pods
kubectl get services
kubectl get deployments
```

## CI Pipeline

GitHub Actions automatically runs when code is pushed to the main branch or a pull request is created.

The current CI workflow performs:

1. Repository checkout.
2. Python 3.12 setup.
3. Dependency installation.
4. Python syntax validation.

Workflow location:

`.github/workflows/ci.yml`

## Monitoring

Prometheus client metrics instrumentation has been added to the application.

Prometheus endpoint verification and Grafana dashboard integration are still in progress.

## Future Enhancements

- Complete Prometheus monitoring integration.
- Grafana dashboard for application metrics.
- Centralized logging using Loki.
- Automated Docker build and deployment pipeline.
- Improved document management and retrieval.

## Author

**Ankit Baghel**

GitHub: https://github.com/Ankitbaghel9975

## License

This project is developed as an educational and technical assessment project.

