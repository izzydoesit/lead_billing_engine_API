import multiprocessing

# Bind to the specified host and port
bind = "0.0.0.0:8080"

# Automatically determine the number of workers based on CPU count
workers = multiprocessing.cpu_count() * 2 + 1

# Log level
loglevel = "info"

# Other gunicorn settings can be added here as needed
