# Format and check the code.
check:
  -black src/osman
  -isort src/osman
  -flake8 src/osman
  -mypy src/osman
