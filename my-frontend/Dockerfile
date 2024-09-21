# my-frontend/Dockerfile

# Use the official Node.js image to build the frontend assets
FROM node:16 as build-stage

# Set working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the entire frontend source code
COPY . .

EXPOSE 8000

# Start Nginx server
CMD ["npm", "run", "serve"]
