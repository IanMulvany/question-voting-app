# Question Voting App Development Guide

## Build & Run Commands
- Run app: `python main.py`
- Run in dev mode: `FLASK_ENV=development python main.py`
- Initialize DB: `export FLASK_APP=main && flask db upgrade`
- Migration: `flask db migrate -m "Description"`
- Run tests: `pytest -s`
- Run single test: `pytest tests/test_app.py::test_function_name -v`

## Code Style Guidelines
- **Imports**: Group imports (standard library, third-party, local)
- **Naming**: snake_case for variables/functions, CamelCase for classes
- **Types**: Use type hints where appropriate
- **Formatting**: Follow PEP 8 (4-space indentation)
- **Comments**: Docstrings for functions, classes, and modules
- **Error Handling**: Use try/except with specific exceptions
- **Functions**: Single responsibility, clear names, <50 lines
- **Database**: SQLAlchemy ORM for DB operations, follow SQLAlchemy patterns
- **Templates**: Use Jinja2 templates with inheritance patterns
- **WebSockets**: Use SocketIO for real-time updates