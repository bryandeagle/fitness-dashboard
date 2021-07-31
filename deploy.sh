docker rm -f fitness
docker build -t deagle/fitness:stable .
docker run -d \
    --init \
    --volume /opt/fitness/config:/config
    --env FITNESS_CONFIG=/config
    --name="fitness" \
    --restart always \
    --publish 127.0.0.1:5100:8080 \
    deagle/fitness:stable
docker logs fitness