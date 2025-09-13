CONTAINER_NAME=nametex

# 如果容器存在，先停止并删除
if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "容器 $CONTAINER_NAME 已存在，正在删除..."
  docker rm -f $CONTAINER_NAME
  if [ $? -ne 0 ]; then
    echo "删除容器失败，退出脚本"
    exit 1
  fi
fi


docker run -d \
  --name $CONTAINER_NAME \
  --env TZ=Asia/Shanghai \
  --restart unless-stopped \
  --network host \
  nametex