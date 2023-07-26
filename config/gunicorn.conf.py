bind = "127.0.0.1:8000"
workers = 4
accesslog = "/app/logs/gunicorn.access.log" #incoming http request info
errorlog = "/app/logs/gunicorn.app.log"
capture_output = True #redirect stdout/stderr (print to console) to specified file in errorlog
loglevel = "info"