FROM python:3.9-slim

WORKDIR /app

# Don't run as root.
RUN useradd --create-home user
USER user
ENV PATH /home/user/.local/bin:$PATH

RUN pip install --no-cache-dir weitersager==0.8.1

EXPOSE 8080

CMD ["weitersager", "config.toml"]
