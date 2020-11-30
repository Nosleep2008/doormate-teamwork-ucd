from apscheduler.schedulers.background import BlockingScheduler
from main.Event_Fetcher import event_fetcher

# this scheduler need google_service as a parameter
def scheduler(google_service):
    # create event fetcher instance
    fetcher = event_fetcher(google_service)
    # create background scheduler
    sched = BlockingScheduler(timezone='MST')
    # set job1
    sched.add_job(fetcher.display_current_event, 'interval', id='10_second_display_current_event', seconds=10)
    # set job2
    sched.add_job(fetcher.update_database, 'interval', id='10_minutes_update_database', seconds=60 * 10)
    # set job3
    # sched.add_job(fetcher.clear_passed_events, 'interval', id='10_hours_clear_passed_events', seconds=60 * 60 * 10)
    # start non-block background scheduler
    sched.start()
