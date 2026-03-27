#!/bin/bash

# PDM项目启动脚本
# 确保从正确的目录执行

cd "$(dirname "$0")/code" || exit 1

echo "当前目录: $(pwd)"
echo "启动Docker Compose..."

docker compose up -d postgres minio pgadmin backend

echo "等待服务启动..."
sleep 10

echo "检查容器状态..."
docker ps -a

echo "=== 服务访问地址 ==="
echo "PostgreSQL: localhost:5432"
echo "MinIO: http://localhost:9000 (API), http://localhost:9001 (Console)"
echo "pgAdmin: http://localhost:5050"
echo "后端API: http://localhost:8000"
echo "前端: http://localhost:3000"
