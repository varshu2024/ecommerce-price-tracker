from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import create_app, db
from app.models import Product, User, PriceHistory  # Add PriceHistory import
from app.scraper import scrape_product_price  # Add scraper import
from config import Config

app = create_app()

def send_email_notification(user_email, product_name, current_price, product_url):
    try:
        message = Mail(
            from_email='notifications@yourdomain.com',
            to_emails=user_email,
            subject=f'Price Drop Alert for {product_name}',
            html_content=f'''
            <h2>Price Drop Alert!</h2>
            <p>The price for {product_name} has dropped to ${current_price}.</p>
            <p><a href="{product_url}">Check it out now!</a></p>
            '''
        )
        
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_sms_notification(phone_number, product_name, current_price, product_url):
    try:
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=f"Price drop! {product_name} is now ${current_price}. {product_url}",
            from_=Config.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        return message.sid is not None
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

def check_price_drops():
    with app.app_context():
        products = Product.query.all()
        for product in products:
            current_price = scrape_product_price(product.url)
            if current_price and current_price <= product.desired_price:
                user = User.query.get(product.user_id)
                
                # Send email notification
                if user.email:
                    send_email_notification(
                        user.email,
                        product.name,
                        current_price,
                        product.url
                    )
                
                # Send SMS notification
                if user.phone:
                    send_sms_notification(
                        user.phone,
                        product.name,
                        current_price,
                        product.url
                    )
                
                # Update product price
                product.current_price = current_price
                db.session.add(product)
                
                # Add to price history
                price_history = PriceHistory(
                    price=current_price,
                    product_id=product.id
                )
                db.session.add(price_history)
                
                db.session.commit()