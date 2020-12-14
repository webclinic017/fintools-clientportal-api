FROM alpine
COPY package.json /app/package.json
WORKDIR /app
RUN apk add nodejs npm
RUN npm install
