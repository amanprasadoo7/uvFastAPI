uv --version

uv init my_project

uv venv
source .venv/bin/activate

uv add fastapi uvicorn pydantic pydantic_settings

uv run python -m test.db_test
