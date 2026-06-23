# Frontend / web tier: nginx reverse proxy in front of the Flask backend.
# Build context is the repository root (see docker-compose.yml).
FROM nginx:1.27-alpine

# Replace the default site with our reverse-proxy config.
RUN rm /etc/nginx/conf.d/default.conf
COPY infrastructure/nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
