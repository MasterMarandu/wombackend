# Wombackend API

API RESTful con arquitectura hexagonal, autenticación JWT y despliegue en Google Cloud Run.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <repository-url>
   cd todo-api


2. Construir la imagen

~~~
gcloud builds submit --tag gcr.io/wombackend/wombackend .
~~~

3. Despliega la imagen en Cloud Run:

gcloud run deploy wombackend \
  --image gcr.io/wombackend/wombackend \
  --allow-unauthenticated \
  --set-env-vars JWT_SECRET=8Zz5tw0Ionm3XPZZfN0NOml3z9FMfmpgXwovR9fp6ryDIoGRM8EPHAB6iHsc0fb


4. Probar el endpoint

~~~
  curl -X POST "https://wombackend-158550194403.us-east1.run.app/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpassword"
~~~