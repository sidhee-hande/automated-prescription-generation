# base image
FROM node:12.2.0-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PA
# install and cache app dependencies
ADD src src

COPY babel.config.js babel.config.js
COPY package.json package.json


RUN npm install
RUN npm install @vue/cli@5.0.8 -g

# start app
CMD ["npm", "run", "serve"]