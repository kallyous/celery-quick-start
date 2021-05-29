from celery import Celery
from celery.schedules import crontab


app = Celery('celeryapp',
        broker='redis://localhost',
        backend='redis://localhost',
        include=['tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='America/Maceio',
    enable_utc=True,
)

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'tasks.add',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'test-message': {
        'task': 'tasks.test',
        'schedule': 10.0,
        'args': ('FUCK THIS SHIT!!!',)
    }
}

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 5 seconds.
    sender.add_periodic_task(5.0, test.s('hello'), name='hello every 5s')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(10.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

if __name__ == '__main__':
    app.start()
