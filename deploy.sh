docker rm -f fitness
docker build -t deagle/fitness:stable .
docker run --init --name="fitness" --env PYTHONBUFFERED=1 --restart always -p 5100:8080 deagle/fitness:stable
