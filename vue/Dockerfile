# build stage
FROM node:10.15.2-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install -f
COPY . .
RUN npm run build

# production stage
FROM nginx:1.15.9-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
