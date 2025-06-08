from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Product
from app.scraper import scrape_product_price

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/track', methods=['POST'])
def track_product():
    email = request.form.get('email')
    phone = request.form.get('phone')
    product_url = request.form.get('product_url')
    desired_price = float(request.form.get('desired_price'))
    
    # Check if user exists or create new
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, phone=phone)
        db.session.add(user)
        db.session.commit()
    
    # Get product details
    product_name = "Product Name"  # You can scrape this similarly to price
    current_price = scrape_product_price(product_url)
    
    # Create product record
    product = Product(
        name=product_name,
        url=product_url,
        current_price=current_price,
        desired_price=desired_price,
        user_id=user.id
    )
    db.session.add(product)
    db.session.commit()
    
    flash('Product is now being tracked! You will be notified when the price drops.')
    return redirect(url_for('main.index'))