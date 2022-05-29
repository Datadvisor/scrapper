FROM node:17-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install

COPY . /app

RUN yarn prisma generate

RUN yarn build

FROM node:17-alpine

WORKDIR /app

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/prisma /app/prisma/
COPY --from=builder /app/docker-entrypoint.sh /app/docker-entrypoint.sh
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/yarn.lock /app/yarn.lock

RUN yarn install --production

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["yarn", "start"]
