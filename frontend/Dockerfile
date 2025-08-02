FROM node:20-alpine

WORKDIR /frontend

COPY package.json yarn.lock ./
RUN yarn install
COPY . .
CMD ["yarn", "start"]
