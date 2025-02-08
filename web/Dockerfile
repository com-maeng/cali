# Deploy web app's prototype.

FROM node:20-alpine

WORKDIR /cali/web
COPY . .

RUN npm install
RUN npm run build

CMD ["npm", "start"]
