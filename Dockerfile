# Build the front-end static assets
FROM node:18-alpine AS builder
COPY /frontend ./
RUN yarn install --frozen-lockfile
RUN yarn build

# Production image
FROM python:3.10 as runner
WORKDIR /code
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY --from=builder ./out /code/frontend/out
COPY ./backend /code/backend
EXPOSE 5000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5000"]