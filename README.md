# goit-pythonweb-hw-03

## description

This project is a simple Python web application using an HTTP server and Jinja2 templates. The application allows you to save messages in JSON.

\* It uses Docker for containerization.

[Demo](https://goit-pythonweb-hw-03.onrender.com/)

### Routes

- **/** — home page.
- **/message** — add new message.
- **/read** — messages list.
- **/error** — error page.

## Dependencies

- Python 3.11
- Docker
- Poetry
- Jinja2

## Installation instructions

```bash
   git clone https://github.com/zharuk-alex/goit-pythonweb-hw-03.git

   cd your-repo

   docker-compose up --build
```

Open your browser and navigate to http://localhost:3000 to access the app.
