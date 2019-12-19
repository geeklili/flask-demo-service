import multiprocessing

timeout = 30

workers = 2 * multiprocessing.cpu_count() + 1

bind = 'unix:flask-demo-service.sock'

umask = 0x7

loglevel = 'info'

pidfile = '/var/run/flask-demo-service.pid'

accesslog = '/var/log/flask-demo-service/access.log'

errorlog = '/var/log/flask-demo-service/error.log'
