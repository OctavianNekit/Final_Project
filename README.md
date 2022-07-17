# Final_Project

1. git clone https://github.com/OctavianNekit/Final_Project
2. cd Final_project
3. docker build -t octaviannekit/ml .
4. docker run -d -p 8180:8180 -p 8181:8181 -v <...>:/app/app/models octaviannekit/ml
(Вместо <...> прописать путь к модели)
