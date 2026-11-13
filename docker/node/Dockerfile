FROM node:22.11.0
ENV NODE_ENV=production
WORKDIR /node
# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY node/package*.json /node
ENV NODE_PATH=/node/node_modules/
# Retry flaky downloads (e.g. the git-hosted difflib tarball from codeload.github.com) instead of failing the build
RUN npm config set fetch-retries 5 \
    && npm config set fetch-retry-mintimeout 20000 \
    && npm config set fetch-retry-maxtimeout 120000 \
    && npm install
WORKDIR /srv
