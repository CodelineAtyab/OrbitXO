# Use official Node.js image (change version if needed)
FROM node:20
 
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 3000

# Start the app (change if your entrypoint is different)
CMD ["npm", "start"]
