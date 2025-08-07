FROM node:20-alpine

WORKDIR /frontend

# Copy package files first for better caching
COPY package.json yarn.lock ./
RUN yarn install

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy the rest of the application
COPY . .

# Make sure tsconfig.json exists
RUN test -f tsconfig.json || echo '{"compilerOptions":{"jsx":"react-jsx"}}' > tsconfig.json

# Build the React app
RUN yarn build

# Install 'serve' to serve the production build
RUN yarn global add serve

EXPOSE 3000

# Command to run the server
CMD ["serve", "-s", "build", "-l", "3000"]
