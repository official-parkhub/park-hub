test-coverage:
	dotenv -f env/.env.test run pytest --cov=src

test:
	dotenv -f env/.env.test run pytest tests/
