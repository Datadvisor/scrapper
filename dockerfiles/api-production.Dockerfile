FROM node:17-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --production

RUN yarn global add typescript

COPY . /app

RUN yarn build

FROM node:17-alpine

WORKDIR /app

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules/ /app/node_modules/
COPY --from=builder /app/package.json /app/package.json

EXPOSE 80

ENTRYPOINT ["yarn"]

CMD ["start"]
