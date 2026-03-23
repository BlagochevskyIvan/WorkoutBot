FROM node:22-alpine 

WORKDIR /app

COPY package*.json ./

RUN npm install && npm audit fix

EXPOSE 3000

COPY . .

CMD [ "npm", "run", "dev" ]