
FROM python:3.11-slim
# Set environment variables for Hugging Face cache
ENV TRANSFORMERS_CACHE=/app/.cache
ENV HF_HOME=/app/.cache
#set a working directory
WORKDIR /app
# Create a writable cache directory
RUN mkdir -p /app/.cache && chmod -R 777 /app/.cache
# Download NLTK data (VADER lexicon)
RUN python -c "import nltk; nltk.download('vader_lexicon')"
#copy files from container
COPY . /app
#install dependencies
RUN pip install --no-cache-dir -r requirements.txt
#port for fastapi
EXPOSE 8000 8501
#start both fastapi and streamlit
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/app.py --server.port 8501"]