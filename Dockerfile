# syntax=docker/dockerfile:1
FROM nginx:alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
