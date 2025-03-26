FROM node:latest

WORKDIR /app

COPY package.json /app/package.json  
COPY . /app                         

RUN npm install && npm run build

EXPOSE 3000

CMD ["npm", "start"]