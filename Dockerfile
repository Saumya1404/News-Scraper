
FROM python3.11-slim
#set a working directory
WORKDIR /app
#copy files from container
COPY . /app
#install dependencies
RUN pip install --no-cache-dir -r requirements.txt
#port for fastapi
EXPOSE 8000 8501
#start both fastapi and streamlit
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/app.py --server.port 8501"]