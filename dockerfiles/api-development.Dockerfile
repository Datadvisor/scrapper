FROM node:17-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install

COPY . /app

EXPOSE 80

ENTRYPOINT ["yarn"]

CMD ["dev"]
