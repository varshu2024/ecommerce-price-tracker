from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from app.notifications import check_price_drops

app = create_app()

if __name__ == '__main__':
    # Create scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_price_drops, 'interval', hours=1)
    scheduler.start()
    
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()