FROM python:3.9-slim
WORKDIR /app
COPY server.py node.py .
# Desabilita o buffer do log para vermos as mensagens no docker logs em tempo real
ENV PYTHONUNBUFFERED=1
#CMD ["python", "p2p_node.py"]
CMD ["sh", "-c", "while true; do sleep 30; done"]

