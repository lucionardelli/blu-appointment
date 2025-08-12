# Use an official Node.js runtime as a parent image
FROM node:20-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy frontend application's source code
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Make port 5173 available to the world outside this container
EXPOSE 5173

# Run the Vite development server
CMD ["npm", "run", "dev", "--", "--host"]
