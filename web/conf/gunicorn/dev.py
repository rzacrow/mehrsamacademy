wsgi_app = "ma.wsgi:application"
loglevel = "debug"
workers = 2
bind = "0.0.0.0:8000"
reload = True #delete in production
#accesslog = errorlog = "/var/log/gunicorn/dev.log" #uncomment in production
#capture_output = True #uncomment in production
#pidfile = "/var/run/gunicorn/dev.pid" #uncomment in production
#daemon = True