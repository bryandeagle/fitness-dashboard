docker rm -f fitness
docker build -t deagle/fitness:stable .
docker run --init --name="fitness" --restart always -d -p 5100:8050 deagle/fitness:stable
