FROM python:3.12

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# torch CPU
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# sentence transformers deps
RUN pip3 install transformers tqdm numpy scikit-learn scipy nltk sentencepiece

# install sentence transformers no deps
RUN pip3 install --no-deps sentence-transformers

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
