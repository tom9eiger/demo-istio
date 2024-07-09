FROM node:14-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY server.js ./
COPY keys ./keys

CMD ["node", "server.js"]
