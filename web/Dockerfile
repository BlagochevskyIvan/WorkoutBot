FROM node:22-alpine

WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1

COPY package.json package-lock.json ./
RUN npm ci --prefer-offline --no-audit --no-fund

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
