# DECOLOG

A lightweight Python logging decorator that automatically logs function calls, arguments, execution time, and exceptions. Provides both console and file logging with configurable verbosity.

## Installation

```bash
pip install decolog
```

## Quick Start

### Basic Usage

```python
from decolog import Logger
import logging

# Initialize logger
logger = Logger(
    app_name="my_app",
    dir_path="./logs",
    log_level=logging.DEBUG,
    console_handler_level=logging.DEBUG,
    file_handler_level=logging.DEBUG
)

# Decorate functions - logs calls automatically
@logger
def add_numbers(a, b):
    return a + b

@logger
def greet(name):
    return f"Hello, {name}!"

# Function calls are automatically logged
result = add_numbers(5, 3)  # Logs: function name, args, execution time
message = greet("World")    # Logs: function name, args, execution time
```

### Per-Function Verbosity Control

Control whether function arguments are truncated in logs:

```python
# Default: arguments are truncated (verbose=False)
@logger
def function1(x, y, z):
    return x + y + z

# Explicit verbose=False (same as default)
@logger(is_verbose=False)
def function2(x, y, z):
    return x + y + z

# Full arguments shown (verbose=True)
@logger(is_verbose=True)
def function3(x, y, z):
    return x + y + z
```

## Features

- **Automatic function logging**: Logs function name, arguments, execution time
- **Exception logging**: Automatically logs exceptions with traceback
- **Dual output**: Logs to both console and file
- **Per-function verbosity**: Control argument display per function
- **Configurable log levels**: Set different levels for console and file output
- **Daily log rotation**: Creates new log files daily

## Parameters

### Logger Initialization

```python
Logger(
    app_name: str,              # Application name (used in log files)
    dir_path: str | Path,       # Directory for log files
    log_level: int = logging.DEBUG,  # Overall log level
    console_handler_level: int = logging.DEBUG,  # Console log level
    file_handler_level: int = logging.DEBUG      # File log level
)
```

### Decorator Usage

```python
@logger(is_verbose=False)  # Truncate function arguments in logs (default)
@logger(is_verbose=True)   # Show full function arguments in logs
```

## Log Format

Logs follow this format:
```
YYYY-MM-DD HH:MM:SS|app_name|LOG_LEVEL:message
```

Example log entry:
```
2023-11-15 14:30:45|my_app|DEBUG:add_numbers(*(5, 3), **{})
2023-11-15 14:30:45|my_app|DEBUG:executed add_numbers(*(5, 3), **{}) in 0.0001 seconds
```

## Advanced Example

```python
from decolog import Logger
import logging

# Configure logger
logger = Logger(
    app_name="data_processor",
    dir_path="/var/log/myapp",
    console_handler_level=logging.INFO,   # Less verbose console output
    file_handler_level=logging.DEBUG      # Detailed file logs
)

# Decorate multiple functions with different verbosity
@logger
def load_data(file_path):
    # ... implementation ...
    pass

@logger(is_verbose=True)
def process_data(data, config):
    # ... implementation ...
    pass

@logger(is_verbose=False)
def save_results(results, output_path):
    # ... implementation ...
    pass

# All function calls are automatically logged
load_data("input.csv")
process_data(data, config={"param": "value"})
save_results(results, "output.json")
```



