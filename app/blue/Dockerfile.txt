FROM node:16
WORKDIR /app
COPY app.js .
RUN npm init -y && npm install express
EXPOSE 3000
CMD ["node", "app.js"]
