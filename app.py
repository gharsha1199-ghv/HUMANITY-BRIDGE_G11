from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db=mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Sharjina@74802',
    database='humanity_bridge'
)



app = Flask(__name__)
app.secret_key = 'humanity_bridge_secret_key'

@app.before_request
def check_db_connection():
    try:
        db.ping(reconnect=True, attempts=3, delay=2)
    except Exception as e:
        print("Database ping failed:", e)  



 
                                                         # before login pages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def beforelogin_about():
    return render_template('beforelogin_Script_html/about_pg.html')

@app.route('/donate')
def beforelogin_donate():
    return render_template('beforelogin_Script_html/donate_pg.html')

@app.route('/gallery')
def beforelogin_gallery():
    return render_template('beforelogin_Script_html/gallery_pg.html')

@app.route('/login')
def beforelogin_login():
    session.clear()
    return render_template('beforelogin_Script_html/login_pg.html')

@app.route('/ourwork')
def beforelogin_ourwork():
    return render_template('beforelogin_Script_html/ourwork_pg.html')

@app.route('/signup')
def beforelogin_signup1():
    return render_template('beforelogin_Script_html/signup1.html')

@app.route('/signupRdonar')
def beforelogin_signupRdonar():
    return render_template('beforelogin_Script_html/signupRdonar.html')

@app.route('/signupdonar')
def beforelogin_signupdonar():
    return render_template('beforelogin_Script_html/signupdonar.html')

@app.route('/signupreciever')
def beforelogin_signupreciever():
    return render_template('beforelogin_Script_html/signupreciever.html')

@app.route('/signupvolunteer')
def beforelogin_signupvolunteer():
    return render_template('beforelogin_Script_html/signupvolunteer.html')








                                                              # donor login pages


@app.route('/donardashboard')
def donorlogin_donardashboard():
    name = session.get('name', 'Harsha Vardhan')
    phone = session.get('phone', '+91 98765 43210')
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, donation_type, amount, quantity, created_at, status FROM donor_donations WHERE donor_name = %s AND phone = %s ORDER BY created_at DESC", (name, phone))
        donations = cursor.fetchall()
        for idx, d in enumerate(donations):
            d['sno'] = idx + 1
            d['formatted_date'] = d['created_at'].strftime('%d %b %Y') if d['created_at'] else 'N/A'
            if d['donation_type'] == 'money':
                d['formatted_type'] = "Money Donation"
                d['social_impact'] = "Funded NGO community operations"
                d['eco_impact'] = "Supported carbon footprint offset"
            elif d['donation_type'] == 'food':
                d['formatted_type'] = "Food Donation"
                q = d['quantity'] or 0
                d['social_impact'] = f"Fed {int(q * 1.5)} people in local shelters"
                d['eco_impact'] = f"Saved {int(q * 0.45)}kg food from landfill"
            else:
                d['formatted_type'] = "Clothes Donation"
                q = d['quantity'] or 0
                d['social_impact'] = f"Provided warmth to {q} families"
                d['eco_impact'] = "Recycled fabric waste"
        cursor.close()
    except Exception as e:
        donations = []
        print("Error in donor dashboard:", e)
        
    return render_template('donorlogin_Script_html/donardashboard_pg.html', donations=donations)

@app.route('/donarmyaccount', methods=['GET', 'POST'])
def donorlogin_myaccount():
    email = session.get('email')
    if not email:
        return redirect('/login')
        
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donors WHERE email = %s", (email,))
        user = cursor.fetchone() or {}
        
        name = user.get('name', session.get('name', 'Harsha Vardhan'))
        phone = user.get('phone', session.get('phone', '+91 98765 43210'))
        
        cursor.execute("SELECT COUNT(*) as c, SUM(CASE WHEN donation_type='money' THEN amount ELSE 0 END) as money_sum FROM donor_donations WHERE donor_name = %s AND phone = %s", (name, phone))
        stats = cursor.fetchone()
        total_donations = stats['c'] or 0
        total_contributed = f"Rs. {int(stats['money_sum'] or 0)}"
        people_helped = total_donations * 15
        
        cursor.execute("SELECT COUNT(*) as c FROM donor_donations WHERE donor_name = %s AND phone = %s AND donation_type = 'food'", (name, phone))
        food_count = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM donor_donations WHERE donor_name = %s AND phone = %s AND donation_type = 'clothes'", (name, phone))
        clothes_count = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM donor_donations WHERE donor_name = %s AND phone = %s AND donation_type = 'money'", (name, phone))
        money_count = cursor.fetchone()['c'] or 0
        
        cursor.close()
    except Exception as e:
        print("Error in donor myaccount:", e)
        user = {}
        total_donations = 0
        total_contributed = "Rs. 0"
        people_helped = 0
        food_count = 0
        clothes_count = 0
        money_count = 0
        
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        full_name = f"{first_name} {last_name}" if first_name and last_name else (first_name or last_name or name)
        phone = request.form.get('phone')
        city = request.form.get('city')
        pincode = request.form.get('zipCode') or request.form.get('pincode')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE donors 
                SET name = %s, phone = %s, city = %s, pincode = %s 
                WHERE email = %s
            """, (full_name, phone, city, pincode, email))
            db.commit()
            
            session['name'] = full_name
            session['phone'] = phone
            session['city'] = city
            session['pincode'] = pincode
            cursor.close()
        except Exception as e:
            print("Error updating donor profile:", e)
        return redirect('/donarmyaccount')
        
    name_parts = user.get('name', '').split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    return render_template(
        'donorlogin_Script_html/myaccount_pg.html',
        user=user,
        first_name=first_name,
        last_name=last_name,
        total_donations=total_donations,
        total_contributed=total_contributed,
        people_helped=people_helped,
        food_count=food_count,
        clothes_count=clothes_count,
        money_count=money_count
    )



@app.route('/donorabout')
def donorlogin_about():
    return render_template('donorlogin_Script_html/about_pg.html')

@app.route('/donordonate')
def donorlogin_donate():
    return render_template('donorlogin_Script_html/donate_pg.html')

@app.route('/donordonatecloths', methods=['GET', 'POST'])
def donorlogin_donatecloths():
    if session.get('role') == 'regulardonor':
        return redirect('/regulardonorhome')
    if request.method == 'POST':
        donor_name = request.form.get('donor_name') or session.get('name', 'Anonymous')
        phone = request.form.get('phone') or session.get('phone', '0000000000')
        city = request.form.get('city') or session.get('city', 'Hyderabad')
        pincode = request.form.get('pincode') or session.get('pincode', '500001')
        full_address = request.form.get('full_address') or session.get('address', 'Online Contribution')
        
        target_groups = request.form.getlist('target_group')
        target_group_str = ','.join(target_groups)
        
        clothing_category = request.form.get('clothing_category')
        condition_type = request.form.get('condition_type')
        
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity) if quantity else None
        except ValueError:
            quantity = None
            
        is_clean = 1 if request.form.get('is_clean') in ['1', 'true', 'on'] else 0
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO donor_donations (
                    donation_type, donor_name, phone, city, pincode, full_address,
                    target_group, clothing_category, condition_type, quantity, is_clean
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'clothes', donor_name, phone, city, pincode, full_address,
                target_group_str, clothing_category, condition_type, quantity, is_clean
            ))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in clothes donation:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/donorformsubmit')
        
    return render_template('donorlogin_Script_html/donatecloths_pg.html')

@app.route('/donordonatefood', methods=['GET', 'POST'])
def donorlogin_donatefood():
    if request.method == 'POST':
        food_category = request.form.get('food_category')
        donor_name = request.form.get('donor_name') or session.get('name', 'Anonymous')
        phone = request.form.get('phone') or session.get('phone', '0000000000')
        city = request.form.get('city') or session.get('city', 'Hyderabad')
        pincode = request.form.get('pincode') or session.get('pincode', '500001')
        full_address = request.form.get('full_address') or session.get('address', 'Online Contribution')
        
        expiry_date = request.form.get('expiry_date')
        if not expiry_date:
            expiry_date = None
        expiry_time = request.form.get('expiry_time')
        if not expiry_time:
            expiry_time = None
            
        food_quantity = request.form.get('food_quantity')
        try:
            food_quantity_int = int(food_quantity) if food_quantity else None
        except ValueError:
            food_quantity_int = None

        food_unit = request.form.get('food_unit')
        description_notes = request.form.get('description_notes')
        if food_quantity and food_unit:
            description = f"Quantity: {food_quantity} {food_unit}. Details: {description_notes or ''}"
        else:
            description = description_notes or ''
        
        is_hygienic = 1 if request.form.get('is_hygienic') in ['1', 'true', 'on'] else 0
        prepared_time = request.form.get('prepared_time')
        if not prepared_time:
            prepared_time = None
        pickup_time = request.form.get('pickup_time')
        if not pickup_time:
            pickup_time = None
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO donor_donations (
                    donation_type, donor_name, phone, city, pincode, full_address,
                    food_category, expiry_date, expiry_time, description, is_hygienic, 
                    prepared_time, pickup_time, quantity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'food', donor_name, phone, city, pincode, full_address,
                food_category, expiry_date, expiry_time, description, is_hygienic,
                prepared_time, pickup_time, food_quantity_int
            ))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in food donation:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/donorformsubmit')
        
    return render_template('donorlogin_Script_html/donatefood_pg.html')

@app.route('/donordonatemoney', methods=['GET', 'POST'])
def donorlogin_donatemoney():
    if request.method == 'POST':
        amount = request.form.get('amount')
        try:
            amount = float(amount) if amount else None
        except ValueError:
            amount = None
        purpose = request.form.get('purpose')
        payment_method = request.form.get('payment_method')
        upi_id = request.form.get('upi_id')
        
        donor_name = session.get('name', 'Anonymous')
        phone = session.get('phone', '0000000000')
        city = session.get('city', 'Hyderabad')
        pincode = session.get('pincode', '500001')
        full_address = session.get('address', 'Online Contribution')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO donor_donations (
                    donation_type, donor_name, phone, city, pincode, full_address, 
                    amount, purpose, payment_method, upi_id, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'money', donor_name, phone, city, pincode, full_address,
                amount, purpose, payment_method, upi_id, 'Completed'
            ))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in money donation:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/donorformsubmit')
        
    return render_template('donorlogin_Script_html/donatemoney.html')

@app.route('/donordonation_history')
def donorlogin_donation_history():
    name = session.get('name', 'Harsha Vardhan')
    phone = session.get('phone', '+91 98765 43210')
    month = request.args.get('month')
    try:
        cursor = db.cursor(dictionary=True)
        if month and month != 'All Time':
            cursor.execute("SELECT id, donation_type, amount, quantity, created_at, status FROM donor_donations WHERE donor_name = %s AND phone = %s AND MONTHNAME(created_at) = %s ORDER BY created_at DESC", (name, phone, month))
        else:
            cursor.execute("SELECT id, donation_type, amount, quantity, created_at, status FROM donor_donations WHERE donor_name = %s AND phone = %s ORDER BY created_at DESC", (name, phone))
        donations = cursor.fetchall()
        for idx, d in enumerate(donations):
            d['sno'] = idx + 1
            d['formatted_date'] = d['created_at'].strftime('%d %b %Y') if d['created_at'] else 'N/A'
            if d['donation_type'] == 'money':
                d['details'] = f"Rs. {int(d['amount'] or 0)}"
                d['social_impact'] = "Funded NGO operations"
                d['eco_impact'] = "Supported carbon offset"
            elif d['donation_type'] == 'food':
                q = d['quantity'] or 0
                d['details'] = f"{q} Meals"
                d['social_impact'] = f"Fed {int(q * 1.5)} people"
                d['eco_impact'] = f"Reduced {int(q * 0.4)}kg food waste"
            else:
                q = d['quantity'] or 0
                d['details'] = f"{q} Clothes"
                d['social_impact'] = f"Helped {q} families"
                d['eco_impact'] = "Recycled fabric waste"
        cursor.close()
    except Exception as e:
        donations = []
        print("Error fetching donor donation history:", e)
        
    return render_template('donorlogin_Script_html/donation_history_pg.html', donations=donations)

@app.route('/donorformsubmit')
def donorlogin_formsubmit():
    return render_template('donorlogin_Script_html/formsubmit.html')

@app.route('/donorgallery')
def donorlogin_gallery():
    return render_template('donorlogin_Script_html/gallery_pg.html')

@app.route('/donorhome')
def donorlogin_index():
    return render_template('donorlogin_Script_html/index.html')

@app.route('/donorourwork')
def donorlogin_ourwork():
    return render_template('donorlogin_Script_html/ourwork_pg.html')








                                                      # regular donor login pages



@app.route('/regulardonorabout')
def regulardonar_about():
    return render_template('regulardonar_Script_html/about_pg.html')

@app.route('/regulardonordashboard')
def regulardonar_donardashboard():
    name = session.get('name', 'Santhosh Dhaba')
    phone = session.get('phone', '+91 99999 88888')
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, donation_type, amount, quantity, created_at, status FROM regular_donor_donations WHERE donor_name = %s AND phone = %s ORDER BY created_at DESC", (name, phone))
        donations = cursor.fetchall()
        for idx, d in enumerate(donations):
            d['sno'] = idx + 1
            d['formatted_date'] = d['created_at'].strftime('%d %b %Y') if d['created_at'] else 'N/A'
            if d['donation_type'] == 'money':
                d['formatted_type'] = "Money Donation"
                d['social_impact'] = "Funded NGO shelter operations"
                d['eco_impact'] = "None"
            else:
                d['formatted_type'] = "Food Donation"
                q = d['quantity'] or 0
                d['social_impact'] = f"Fed {q} families in local shelters"
                d['eco_impact'] = f"Reduced {int(q * 0.5)}kg food waste"
        cursor.close()
    except Exception as e:
        donations = []
        print("Error in regular donor dashboard:", e)
        
    return render_template('regulardonar_Script_html/donardashboard_pg.html', donations=donations)

@app.route('/regulardonordonate')
def regulardonar_donate():
    return render_template('regulardonar_Script_html/donate_pg.html')

@app.route('/regulardonordonatecloths')
def regulardonar_donatecloths():
    return redirect('/regulardonorhome')

@app.route('/regulardonordonatefood', methods=['GET', 'POST'])
def regulardonar_donatefood():
    if request.method == 'POST':
        food_type = request.form.get('food_type')
        food_category = request.form.get('food_category')
        
        donor_name = request.form.get('donor_name') or session.get('name', 'Anonymous')
        phone = request.form.get('phone') or session.get('phone', '0000000000')
        city = request.form.get('city') or session.get('city', 'Hyderabad')
        pincode = request.form.get('pincode') or session.get('pincode', '500001')
        full_address = request.form.get('full_address') or session.get('city', 'Hyderabad')
        
        expiry_date = request.form.get('expiry_date')
        if not expiry_date:
            expiry_date = None
        expiry_time = request.form.get('expiry_time')
        if not expiry_time:
            expiry_time = None
            
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity) if quantity else None
        except ValueError:
            quantity = None
            
        description = request.form.get('description')
        is_hygienic = 1 if request.form.get('is_hygienic') in ['1', 'true', 'on'] else 0
        prepared_time = request.form.get('prepared_time')
        if not prepared_time:
            prepared_time = None
        pickup_time = request.form.get('pickup_time')
        if not pickup_time:
            pickup_time = None
            
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO regular_donor_donations (
                    donation_type, donor_name, phone, city, pincode, full_address,
                    food_type, food_category, expiry_date, expiry_time, quantity, 
                    description, is_hygienic, prepared_time, pickup_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'food', donor_name, phone, city, pincode, full_address,
                food_type, food_category, expiry_date, expiry_time, quantity,
                description, is_hygienic, prepared_time, pickup_time
            ))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in regular food donation:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/regulardonorformsubmit')
        
    return render_template('regulardonar_Script_html/donatefood_pg.html')

@app.route('/regulardonordonatemoney', methods=['GET', 'POST'])
def regulardonar_donatemoney():
    if request.method == 'POST':
        amount = request.form.get('amount')
        try:
            amount = float(amount) if amount else None
        except ValueError:
            amount = None
        purpose = request.form.get('purpose')
        payment_method = request.form.get('payment_method')
        upi_id = request.form.get('upi_id')
        
        donor_name = session.get('name', 'Anonymous')
        phone = session.get('phone', '0000000000')
        city = session.get('city', 'Hyderabad')
        pincode = session.get('pincode', '500001')
        full_address = session.get('address', 'Online Contribution')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO regular_donor_donations (
                    donation_type, donor_name, phone, city, pincode, full_address,
                    amount, purpose, payment_method, upi_id, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'money', donor_name, phone, city, pincode, full_address,
                amount, purpose, payment_method, upi_id, 'Completed'
            ))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in regular money donation:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/regulardonorformsubmit')
        
    return render_template('regulardonar_Script_html/donatemoney.html')

@app.route('/regulardonordonation_history')
def regulardonar_donation_history():
    name = session.get('name', 'Santhosh Dhaba')
    phone = session.get('phone', '+91 99999 88888')
    month = request.args.get('month')
    try:
        cursor = db.cursor(dictionary=True)
        if month and month != 'All Time':
            cursor.execute("SELECT id, donation_type, amount, quantity, created_at, status FROM regular_donor_donations WHERE donor_name = %s AND phone = %s AND MONTHNAME(created_at) = %s ORDER BY created_at DESC", (name, phone, month))
        else:
            cursor.execute("SELECT id, donation_type, amount, quantity, created_at, status FROM regular_donor_donations WHERE donor_name = %s AND phone = %s ORDER BY created_at DESC", (name, phone))
        donations = cursor.fetchall()
        for idx, d in enumerate(donations):
            d['sno'] = idx + 1
            d['formatted_date'] = d['created_at'].strftime('%d %b %Y') if d['created_at'] else 'N/A'
            if d['donation_type'] == 'money':
                d['donation'] = "Money"
                d['quantity_str'] = f"Rs. {int(d['amount'] or 0)}"
                d['social_impact'] = "Funded NGO shelter operations"
                d['eco_impact'] = "None"
            else:
                d['donation'] = "Food"
                q = d['quantity'] or 0
                d['quantity_str'] = f"{q} Meals"
                d['social_impact'] = f"Fed {q} families"
                d['eco_impact'] = f"Reduced {int(q * 0.5)}kg food waste"
        cursor.close()
    except Exception as e:
        donations = []
        print("Error fetching regular donor donation history:", e)
        
    return render_template('regulardonar_Script_html/donation_history_pg.html', donations=donations)

@app.route('/regulardonorformsubmit')
def regulardonar_formsubmit():
    return render_template('regulardonar_Script_html/formsubmit.html')

@app.route('/regulardonorgallery')
def regulardonar_gallery():
    return render_template('regulardonar_Script_html/gallery_pg.html')

@app.route('/regulardonorhome')
def regulardonar_index():
    return render_template('regulardonar_Script_html/index.html')

@app.route('/regulardonormyaccount', methods=['GET', 'POST'])
def regulardonar_myaccount():
    email = session.get('email')
    if not email:
        return redirect('/login')
        
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM regulardonors WHERE email = %s", (email,))
        user = cursor.fetchone() or {}
        
        name = user.get('name', session.get('name', 'Santhosh Dhaba'))
        phone = user.get('phone', session.get('phone', '+91 99999 88888'))
        
        cursor.execute("SELECT COUNT(*) as c, SUM(CASE WHEN donation_type='money' THEN amount ELSE 0 END) as money_sum FROM regular_donor_donations WHERE donor_name = %s AND phone = %s", (name, phone))
        stats = cursor.fetchone()
        total_donations = stats['c'] or 0
        total_contributed = f"Rs. {int(stats['money_sum'] or 0)}"
        people_helped = total_donations * 25
        
        cursor.execute("SELECT COUNT(*) as c FROM regular_donor_donations WHERE donor_name = %s AND phone = %s AND donation_type = 'food'", (name, phone))
        food_count = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM regular_donor_donations WHERE donor_name = %s AND phone = %s AND donation_type = 'money'", (name, phone))
        money_count = cursor.fetchone()['c'] or 0
        
        cursor.close()
    except Exception as e:
        print("Error in regular donor myaccount:", e)
        user = {}
        total_donations = 0
        total_contributed = "Rs. 0"
        people_helped = 0
        food_count = 0
        money_count = 0
        
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        full_name = f"{first_name} {last_name}" if first_name and last_name else (first_name or last_name or name)
        phone = request.form.get('phone')
        city = request.form.get('city')
        pincode = request.form.get('zipCode') or request.form.get('pincode')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE regulardonors 
                SET name = %s, phone = %s, city = %s, pincode = %s 
                WHERE email = %s
            """, (full_name, phone, city, pincode, email))
            db.commit()
            
            session['name'] = full_name
            session['phone'] = phone
            session['city'] = city
            session['pincode'] = pincode
            cursor.close()
        except Exception as e:
            print("Error updating regulardonor profile:", e)
        return redirect('/regulardonormyaccount')
        
    name_parts = user.get('name', '').split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    return render_template(
        'regulardonar_Script_html/myaccount_pg.html',
        user=user,
        first_name=first_name,
        last_name=last_name,
        total_donations=total_donations,
        total_contributed=total_contributed,
        people_helped=people_helped,
        food_count=food_count,
        money_count=money_count
    )

@app.route('/regulardonorourwork')
def regulardonar_ourwork():
    return render_template('regulardonar_Script_html/ourwork_pg.html')

@app.route('/regulardonorregulardonarverification')
def regulardonar_regulardonarverification():
    email = session.get('email')
    if not email:
        return redirect('/login')
    try:
        cursor = db.cursor()
        cursor.execute("SELECT status FROM regulardonors WHERE email = %s", (email,))
        row = cursor.fetchone()
        status = row[0] if row else 'Pending'
        cursor.close()
    except Exception as e:
        status = 'Pending'
        print("Error getting regular donor status:", e)
    return render_template('regulardonar_Script_html/regulardonarverification.html', status=status)










                                                     # ngo login pages


@app.route('/ngoabout')
def ngo_about():
    return render_template('ngo_Script_html/about_pg.html')

@app.route('/ngoformsubmit')
def ngo_formsubmit():
    return render_template('ngo_Script_html/formsubmit.html')

@app.route('/ngogallery')
def ngo_gallery():
    return render_template('ngo_Script_html/gallery_pg.html')

@app.route('/ngogethelp_clothes', methods=['GET', 'POST'])
def ngo_gethelp_clothes():
    if request.method == 'POST':
        clothing_items = request.form.get('clothing_items') or ''
        urgency = request.form.get('urgency', 'Normal')
        additional_details = request.form.get('additional_details') or ''
        agreement_checked = 1 if request.form.get('agreement_checked') in ['1', 'true', 'on'] else 0
        
        ngo_name = session.get('name', 'Anonymous NGO')
        city = session.get('city', 'Hyderabad')
        pincode = session.get('pincode', '500001')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO ngo_requests (
                    request_type, meals_needed, clothing_items, amount_needed,
                    urgency, additional_details, agreement_checked, ngo_name, city, pincode
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ('Clothes', '', clothing_items, 0.00, urgency, additional_details, agreement_checked, ngo_name, city, pincode))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in NGO clothes support request:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/ngoformsubmit')
        
    return render_template('ngo_Script_html/gethelp_clothes.html')

@app.route('/ngogethelp_food', methods=['GET', 'POST'])
def ngo_gethelp_food():
    if request.method == 'POST':
        meals_needed = request.form.get('meals_needed') or ''
        urgency = request.form.get('urgency', 'Normal')
        additional_details = request.form.get('additional_details') or ''
        agreement_checked = 1 if request.form.get('agreement_checked') in ['1', 'true', 'on'] else 0
        
        ngo_name = session.get('name', 'Anonymous NGO')
        city = session.get('city', 'Hyderabad')
        pincode = session.get('pincode', '500001')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO ngo_requests (
                    request_type, meals_needed, clothing_items, amount_needed,
                    urgency, additional_details, agreement_checked, ngo_name, city, pincode
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ('Food', meals_needed, '', 0.00, urgency, additional_details, agreement_checked, ngo_name, city, pincode))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in NGO food support request:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/ngoformsubmit')
        
    return render_template('ngo_Script_html/gethelp_food.html')

@app.route('/ngogethelp_money', methods=['GET', 'POST'])
def ngo_gethelp_money():
    if request.method == 'POST':
        amount_needed = request.form.get('amount_needed')
        try:
            amount_needed = float(amount_needed) if amount_needed else 0.00
        except ValueError:
            amount_needed = 0.00
        urgency = request.form.get('urgency', 'Normal')
        additional_details = request.form.get('additional_details') or ''
        agreement_checked = 1 if request.form.get('agreement_checked') in ['1', 'true', 'on'] else 0
        
        ngo_name = session.get('name', 'Anonymous NGO')
        city = session.get('city', 'Hyderabad')
        pincode = session.get('pincode', '500001')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO ngo_requests (
                    request_type, meals_needed, clothing_items, amount_needed,
                    urgency, additional_details, agreement_checked, ngo_name, city, pincode
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ('Money', '', '', amount_needed, urgency, additional_details, agreement_checked, ngo_name, city, pincode))
            db.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database error in NGO money support request:", err)
            return f"Database error: {err.msg}", 400
            
        return redirect('/ngoformsubmit')
        
    return render_template('ngo_Script_html/gethelp_money.html')

@app.route('/ngogethelp_page')
def ngo_gethelp_page():
    return render_template('ngo_Script_html/gethelp_page.html')

@app.route('/ngohome')
def ngo_index():
    return render_template('ngo_Script_html/index.html')

@app.route('/ngomyaccount', methods=['GET', 'POST'])
def ngo_myaccount():
    email = session.get('email')
    if not email:
        return redirect('/login')
        
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ngo_receivers WHERE email = %s", (email,))
        user = cursor.fetchone() or {}
        
        name = user.get('name', session.get('name', 'Sunshine Orphanage'))
        
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE ngo_name = %s", (name,))
        total_requests = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE ngo_name = %s AND status = 'Approved'", (name,))
        approved_requests = cursor.fetchone()['c'] or 0
        people_helped = approved_requests * 50
        
        cursor.close()
    except Exception as e:
        print("Error in ngo myaccount:", e)
        user = {}
        total_requests = 0
        approved_requests = 0
        people_helped = 0
        
    if request.method == 'POST':
        name = request.form.get('orgName') or name
        org_type = request.form.get('orgType')
        phone = request.form.get('phone')
        address = request.form.get('address')
        capacity = request.form.get('capacity')
        established_year = request.form.get('established')
        needs_list = request.form.getlist('needs')
        needs = ', '.join(needs_list) if needs_list else ''
        bio = request.form.get('bio')
        city = request.form.get('city')
        pincode = request.form.get('zipCode') or request.form.get('pincode')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE ngo_receivers 
                SET name = %s, org_type = %s, phone = %s, address = %s,
                    capacity = %s, established_year = %s, needs = %s,
                    bio = %s, city = %s, pincode = %s 
                WHERE email = %s
            """, (name, org_type, phone, address, capacity, established_year, needs, bio, city, pincode, email))
            db.commit()
            
            session['name'] = name
            session['phone'] = phone
            session['city'] = city
            session['pincode'] = pincode
            cursor.close()
        except Exception as e:
            print("Error updating ngo profile:", e)
        return redirect('/ngomyaccount')
        
    name_parts = user.get('name', '').split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    return render_template(
        'ngo_Script_html/myaccount_pg.html',
        user=user,
        first_name=first_name,
        last_name=last_name,
        total_requests=total_requests,
        approved_requests=approved_requests,
        people_helped=people_helped
    )

@app.route('/ngongo_history')
def ngo_ngo_history():
    name = session.get('name', 'Sunshine Orphanage')
    month = request.args.get('month')
    try:
        cursor = db.cursor(dictionary=True)
        if month and month != 'All Time':
            cursor.execute("SELECT id, request_type, meals_needed, clothing_items, amount_needed, urgency, created_at, status FROM ngo_requests WHERE ngo_name = %s AND MONTHNAME(created_at) = %s ORDER BY created_at DESC", (name, month))
        else:
            cursor.execute("SELECT id, request_type, meals_needed, clothing_items, amount_needed, urgency, created_at, status FROM ngo_requests WHERE ngo_name = %s ORDER BY created_at DESC", (name,))
        requests_list = cursor.fetchall()
        for idx, r in enumerate(requests_list):
            r['sno'] = idx + 1
            r['formatted_date'] = r['created_at'].strftime('%d %b %Y') if r['created_at'] else 'N/A'
            if r['request_type'] == 'Food':
                r['requirement'] = r['meals_needed'] or 'Food Support'
                r['social_impact'] = "Meals for shelter children"
                r['eco_impact'] = "Reduced food waste"
            elif r['request_type'] == 'Clothes':
                r['requirement'] = r['clothing_items'] or 'Clothing Support'
                r['social_impact'] = "Warmth for children"
                r['eco_impact'] = "Recycled fabric waste"
            else:
                r['requirement'] = f"Rs. {int(r['amount_needed'] or 0)}"
                r['social_impact'] = "Funded education & operations"
                r['eco_impact'] = "None"
        cursor.close()
    except Exception as e:
        requests_list = []
        print("Error fetching NGO requests history:", e)
        
    return render_template('ngo_Script_html/ngo_history_pg.html', requests=requests_list)

@app.route('/ngongoverification')
def ngo_ngoverification():
    email = session.get('email')
    if not email:
        return redirect('/login')
    try:
        cursor = db.cursor()
        cursor.execute("SELECT status FROM ngo_receivers WHERE email = %s", (email,))
        row = cursor.fetchone()
        status = row[0] if row else 'Pending'
        cursor.close()
    except Exception as e:
        status = 'Pending'
        print("Error getting NGO status:", e)
    return render_template('ngo_Script_html/ngoverification.html', status=status)

@app.route('/ngoourwork')
def ngo_ourwork():
    return render_template('ngo_Script_html/ourwork_pg.html')

@app.route('/ngorecieverdash')
def ngo_recieverdash():
    name = session.get('name', 'Sunshine Orphanage')
    try:
        cursor = db.cursor(dictionary=True)
        # Food count from completed deliveries
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE receiver_name = %s AND donation_type = 'Food' AND status = 'Delivered'", (name,))
        food_count = cursor.fetchone()['c'] or 0
        
        # Clothes count from completed deliveries
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE receiver_name = %s AND donation_type = 'Clothes' AND status = 'Delivered'", (name,))
        clothes_count = cursor.fetchone()['c'] or 0
        
        # Money count from completed NGO requests
        cursor.execute("SELECT SUM(amount_needed) as s FROM ngo_requests WHERE ngo_name = %s AND request_type = 'Money' AND status = 'Completed'", (name,))
        money_sum = cursor.fetchone()['s'] or 0
        
        # Eco impact metrics
        eco_food = int(food_count * 55)
        eco_clothes_reused = int(clothes_count * 20)
        eco_clothes_co2 = int(clothes_count * 52)
        
        # Request counts
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE ngo_name = %s AND status IN ('Pending', 'Matched')", (name,))
        pending_count = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE ngo_name = %s AND status = 'Approved'", (name,))
        approved_count = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE ngo_name = %s AND status = 'On The Way'", (name,))
        onway_count = cursor.fetchone()['c'] or 0
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE ngo_name = %s AND status = 'Completed'", (name,))
        completed_count = cursor.fetchone()['c'] or 0
        
        cursor.close()
    except Exception as e:
        print("Error fetching NGO dashboard stats:", e)
        food_count = 0
        clothes_count = 0
        money_sum = 0
        eco_food = 0
        eco_clothes_reused = 0
        eco_clothes_co2 = 0
        pending_count = 0
        approved_count = 0
        onway_count = 0
        completed_count = 0
        
    return render_template(
        'ngo_Script_html/recieverdash.html',
        food_count=food_count,
        clothes_count=clothes_count,
        money_sum=int(money_sum),
        eco_food=eco_food,
        eco_clothes_reused=eco_clothes_reused,
        eco_clothes_co2=eco_clothes_co2,
        pending_count=pending_count,
        approved_count=approved_count,
        onway_count=onway_count,
        completed_count=completed_count
    )








                                                # volunteer login pages


@app.route('/volunteerhome')
def volunteer_index():
    volunteer_name = session.get('name', 'Volunteer User')
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE volunteer_name = %s AND status = 'Delivered'", (volunteer_name,))
        total_deliveries = cursor.fetchone()['c'] or 0
        people_helped = total_deliveries * 25
        distance_covered = int(total_deliveries * 6.2)
        volunteer_hours = total_deliveries * 2
        cursor.close()
    except Exception as e:
        print("Error fetching volunteer stats:", e)
        total_deliveries = 0
        people_helped = 0
        distance_covered = 0
        volunteer_hours = 0
        
    return render_template(
        'volunteer_Script_html/index.html',
        total_deliveries=total_deliveries,
        people_helped=people_helped,
        distance_covered=distance_covered,
        volunteer_hours=volunteer_hours
    )

@app.route('/volunteermyaccount', methods=['GET', 'POST'])
def volunteer_myaccount():
    volunteer_email = session.get('email', 'volunteer@gmail.com')
    volunteer_name = session.get('name', 'Volunteer User')
    
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        full_name = f"{first_name} {last_name}" if first_name and last_name else (first_name or last_name or volunteer_name)
        phone = request.form.get('phone')
        city = request.form.get('city')
        pincode = request.form.get('zipCode')
        vehicle_type = request.form.get('vehicle')
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE volunteers 
                SET name = %s, phone = %s, city = %s, pincode = %s, vehicle_type = %s 
                WHERE email = %s
            """, (full_name, phone, city, pincode, vehicle_type, volunteer_email))
            db.commit()
            
            session['name'] = full_name
            session['phone'] = phone
            session['city'] = city
            session['pincode'] = pincode
            session['vehicle_type'] = vehicle_type
            
            cursor.close()
        except Exception as e:
            print("Error updating volunteer profile:", e)
            
        return redirect('/volunteermyaccount')

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE volunteer_name = %s AND status = 'Delivered'", (volunteer_name,))
        total_deliveries = cursor.fetchone()['c'] or 0
        people_helped = total_deliveries * 25
        volunteer_hours = total_deliveries * 2
        cursor.close()
    except Exception as e:
        print("Error in volunteer account stats:", e)
        total_deliveries = 0
        people_helped = 0
        volunteer_hours = 0

    name_parts = volunteer_name.split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    return render_template(
        'volunteer_Script_html/myaccount_pg.html',
        total_deliveries=total_deliveries,
        people_helped=people_helped,
        volunteer_hours=volunteer_hours,
        first_name=first_name,
        last_name=last_name
    )

@app.route('/volunteerorders')
def volunteer_orders():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, delivery_id, date, receiver_name, location, donation_type, quantity_details, status FROM deliveries WHERE volunteer_name = 'Pending' OR volunteer_name = 'To be assigned' OR volunteer_name IS NULL ORDER BY created_at DESC")
        orders = cursor.fetchall()
        for o in orders:
            o['urgency'] = 'Normal'
        cursor.close()
    except Exception as e:
        orders = []
        print("Error fetching available orders:", e)
        
    return render_template('volunteer_Script_html/orders.html', orders=orders)

@app.route('/volunteertracking')
def volunteer_tracking():
    volunteer_name = session.get('name', 'Volunteer User')
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, delivery_id, date, receiver_name, location, donation_type, quantity_details, status FROM deliveries WHERE volunteer_name = %s AND status IN ('Assigned', 'On The Way', 'In Transit') ORDER BY created_at DESC", (volunteer_name,))
        active_deliveries = cursor.fetchall()
        
        cursor.execute("SELECT id, delivery_id, date, receiver_name, location, donation_type, quantity_details, status FROM deliveries WHERE volunteer_name = %s AND status = 'Delivered' ORDER BY date DESC LIMIT 5", (volunteer_name,))
        recent_deliveries = cursor.fetchall()
        cursor.close()
    except Exception as e:
        active_deliveries = []
        recent_deliveries = []
        print("Error fetching tracking data:", e)
        
    return render_template(
        'volunteer_Script_html/tracking.html',
        active_deliveries=active_deliveries,
        recent_deliveries=recent_deliveries
    )

@app.route('/volunteervolunteer_history')
def volunteer_volunteer_history():
    volunteer_name = session.get('name', 'Volunteer User')
    month = request.args.get('month')
    try:
        cursor = db.cursor(dictionary=True)
        if month and month != 'All Time':
            cursor.execute("SELECT id, delivery_id, date, receiver_name, location, quantity_details, status FROM deliveries WHERE volunteer_name = %s AND status = 'Delivered' AND MONTHNAME(date) = %s ORDER BY date DESC", (volunteer_name, month))
        else:
            cursor.execute("SELECT id, delivery_id, date, receiver_name, location, quantity_details, status FROM deliveries WHERE volunteer_name = %s AND status = 'Delivered' ORDER BY date DESC", (volunteer_name,))
        deliveries = cursor.fetchall()
        for d in deliveries:
            d['formatted_date'] = d['date'].strftime('%d %b %Y') if d['date'] else 'N/A'
        cursor.close()
    except Exception as e:
        deliveries = []
        print("Error fetching delivery history:", e)
        
    return render_template('volunteer_Script_html/volunteer_history_pg.html', deliveries=deliveries)

@app.route('/volunteer/accept_order/<int:order_id>')
def volunteer_accept_order(order_id):
    volunteer_name = session.get('name', 'Volunteer User')
    try:
        cursor = db.cursor()
        cursor.execute("UPDATE deliveries SET volunteer_name = %s, status = 'Assigned' WHERE id = %s", (volunteer_name, order_id))
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error accepting order:", e)
        
    return redirect('/volunteertracking')

@app.route('/volunteer/start_delivery/<int:order_id>')
def volunteer_start_delivery(order_id):
    try:
        cursor = db.cursor()
        cursor.execute("UPDATE deliveries SET status = 'On The Way' WHERE id = %s", (order_id,))
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error starting delivery:", e)
        
    return redirect('/volunteertracking')

@app.route('/volunteer/complete_delivery/<int:order_id>')
def volunteer_complete_delivery(order_id):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT delivery_id FROM deliveries WHERE id = %s", (order_id,))
        row = cursor.fetchone()
        
        # Update delivery status
        cursor.execute("UPDATE deliveries SET status = 'Delivered', date = CURDATE() WHERE id = %s", (order_id,))
        
        if row:
            delivery_id = row['delivery_id']
            if delivery_id.startswith("DLV-MAT-"):
                parts = delivery_id.split("-")
                if len(parts) == 5:
                    source = parts[2]
                    donation_id = int(parts[3])
                    request_id = int(parts[4])
                    
                    table_name = 'donor_donations' if source == 'donor' else 'regular_donor_donations'
                    cursor.execute(f"UPDATE {table_name} SET status = 'Completed' WHERE id = %s", (donation_id,))
                    cursor.execute("UPDATE ngo_requests SET status = 'Completed' WHERE id = %s", (request_id,))
                    
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error completing delivery:", e)
        
    return redirect('/volunteertracking')





                                                         # admin login pages


@app.route('/adminabout')
def admin_about():
    return render_template('admin_Script_html/about_pg.html')

@app.route('/adminadd_ngo')
def admin_add_ngo():
    return render_template('admin_Script_html/add_ngo.html')

@app.route('/adminadd_partner')
def admin_add_partner():
    return render_template('admin_Script_html/add_partner.html')

@app.route('/adminadd_regulardonar')
def admin_add_regulardonar():
    return render_template('admin_Script_html/add_regulardonar.html')

@app.route('/adminadmin_history')
def admin_admin_history():
    return render_template('admin_Script_html/admin_history_pg.html')

@app.route('/admindonations')
def admin_donations():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, donation_type, donor_name, phone, city, pincode, full_address, amount, quantity, created_at, status FROM donor_donations")
        donations1 = cursor.fetchall()
        for d in donations1:
            d['source'] = 'donor'
            if d['created_at']:
                d['formatted_date'] = d['created_at'].strftime('%d/%m/%Y')
            else:
                d['formatted_date'] = 'N/A'
            d['formatted_type'] = d['donation_type'].capitalize()
            if d['donation_type'] == 'money':
                d['qty_details'] = f"Rs. {int(d['amount'] or 0)}"
            elif d['donation_type'] == 'food':
                q = d['quantity'] or 0
                d['qty_details'] = f"{q} Meals"
            else:
                q = d['quantity'] or 0
                d['qty_details'] = f"{q} Bags"
                
        cursor.execute("SELECT id, donation_type, donor_name, phone, city, pincode, full_address, amount, quantity, created_at, status FROM regular_donor_donations")
        donations2 = cursor.fetchall()
        for d in donations2:
            d['source'] = 'regular'
            if d['created_at']:
                d['formatted_date'] = d['created_at'].strftime('%d/%m/%Y')
            else:
                d['formatted_date'] = 'N/A'
            d['formatted_type'] = d['donation_type'].capitalize()
            if d['donation_type'] == 'money':
                d['qty_details'] = f"Rs. {int(d['amount'] or 0)}"
            elif d['donation_type'] == 'food':
                q = d['quantity'] or 0
                d['qty_details'] = f"{q} Meals"
            else:
                q = d['quantity'] or 0
                d['qty_details'] = f"{q} Bags"
                
        donations = donations1 + donations2
        donations.sort(key=lambda x: x['created_at'] or datetime.min, reverse=True)
        cursor.close()
    except Exception as e:
        donations = []
        print("Error fetching admin donations:", e)
        
    return render_template('admin_Script_html/donations.html', donations=donations)

@app.route('/admindonations_pie')
def admin_donations_pie():
    return render_template('admin_Script_html/donations_pie.html')

@app.route('/admingallery')
def admin_gallery():
    return render_template('admin_Script_html/gallery_pg.html')

@app.route('/admingraph')
def admin_graph():
    return render_template('admin_Script_html/graph.html')

@app.route('/adminhome')
def admin_index():
    try:
        cursor = db.cursor(dictionary=True)
        
        # 1. Total donations (sum of money)
        cursor.execute("SELECT SUM(amount) as s FROM donor_donations WHERE donation_type = 'money'")
        sum1 = cursor.fetchone()['s'] or 0
        cursor.execute("SELECT SUM(amount) as s FROM regular_donor_donations WHERE donation_type = 'money'")
        sum2 = cursor.fetchone()['s'] or 0
        total_donations_val = sum1 + sum2
        total_donations = f"₹{total_donations_val:,.2f}"
        
        # 2. Successful Receivers (NGOs count)
        cursor.execute("SELECT COUNT(*) as c FROM ngo_receivers")
        total_receivers = cursor.fetchone()['c']
        
        # 3. Meals Served
        cursor.execute("SELECT SUM(quantity) as q FROM donor_donations WHERE donation_type = 'food'")
        q1 = cursor.fetchone()['q'] or 0
        cursor.execute("SELECT SUM(quantity) as q FROM regular_donor_donations WHERE donation_type = 'food'")
        q2 = cursor.fetchone()['q'] or 0
        meals_served = int(q1 + q2)
        
        # 4. Funds Utilised (Approved money requests)
        cursor.execute("SELECT SUM(amount_needed) as s FROM ngo_requests WHERE request_type = 'Money' AND status = 'Approved'")
        funds_utilised_val = cursor.fetchone()['s'] or 0
        funds_utilised = f"₹{funds_utilised_val:,.2f}"
        
        # 5. Clothes Donated
        cursor.execute("SELECT SUM(quantity) as q FROM donor_donations WHERE donation_type = 'clothes'")
        clothes_donated = int(cursor.fetchone()['q'] or 0)
        
        # 6. Pending/Approved counts
        cursor.execute("SELECT COUNT(*) as c FROM donor_donations WHERE status IN ('Pending', 'Matched')")
        pd1 = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM regular_donor_donations WHERE status IN ('Pending', 'Matched')")
        pd2 = cursor.fetchone()['c']
        pending_donations_count = pd1 + pd2
        
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE status IN ('Pending', 'Matched')")
        pending_requests_count = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM donor_donations WHERE status = 'Approved'")
        ad1 = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM regular_donor_donations WHERE status = 'Approved'")
        ad2 = cursor.fetchone()['c']
        approved_donations_count = ad1 + ad2
        
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE status = 'Approved'")
        approved_requests_count = cursor.fetchone()['c']
        
        # 7. Pending Verifications (list)
        pending_verifications = []
        cursor.execute("SELECT id, name, 'Individual Donor' as type, 'donor' as type_raw FROM donors WHERE status = 'Pending'")
        pending_verifications.extend(cursor.fetchall())
        cursor.execute("SELECT id, name, 'Volunteer' as type, 'volunteer' as type_raw FROM volunteers WHERE status = 'Pending'")
        pending_verifications.extend(cursor.fetchall())
        cursor.execute("SELECT id, name, 'Regular Donor' as type, 'regulardonor' as type_raw FROM regulardonors WHERE status = 'Pending'")
        pending_verifications.extend(cursor.fetchall())
        cursor.execute("SELECT id, name, 'NGO Receiver' as type, 'ngo' as type_raw FROM ngo_receivers WHERE status = 'Pending'")
        pending_verifications.extend(cursor.fetchall())
        
        # 8. Tracking stats
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE status = 'Assigned'")
        assigned_deliveries_count = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE status IN ('On The Way', 'In Transit')")
        transit_deliveries_count = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM deliveries WHERE status = 'Delivered'")
        delivered_deliveries_count = cursor.fetchone()['c']
        
        cursor.close()
    except Exception as e:
        print("Error in admin_index stats:", e)
        total_donations = "₹0.00"
        total_receivers = 0
        meals_served = 0
        funds_utilised = "₹0.00"
        clothes_donated = 0
        pending_donations_count = 0
        pending_requests_count = 0
        approved_donations_count = 0
        approved_requests_count = 0
        pending_verifications = []
        assigned_deliveries_count = 0
        transit_deliveries_count = 0
        delivered_deliveries_count = 0
        
    return render_template(
        'admin_Script_html/index.html',
        total_donations=total_donations,
        total_receivers=total_receivers,
        meals_served=meals_served,
        funds_utilised=funds_utilised,
        clothes_donated=clothes_donated,
        pending_donations_count=pending_donations_count,
        pending_requests_count=pending_requests_count,
        approved_donations_count=approved_donations_count,
        approved_requests_count=approved_requests_count,
        pending_verifications=pending_verifications,
        assigned_deliveries_count=assigned_deliveries_count,
        transit_deliveries_count=transit_deliveries_count,
        delivered_deliveries_count=delivered_deliveries_count
    )

@app.route('/adminmyaccount')
def admin_myaccount():
    return render_template('admin_Script_html/myaccount_pg.html')

@app.route('/adminourwork')
def admin_ourwork():
    return render_template('admin_Script_html/ourwork_pg.html')

@app.route('/adminrequestpage')
def admin_requestpage():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, request_type, meals_needed, clothing_items, amount_needed, urgency, additional_details, agreement_checked, created_at, status, ngo_name, city, pincode FROM ngo_requests ORDER BY created_at DESC")
        requests_list = cursor.fetchall()
        for r in requests_list:
            if r['created_at']:
                r['formatted_date'] = r['created_at'].strftime('%b %d')
            else:
                r['formatted_date'] = 'N/A'
            if r['request_type'] == 'Food':
                r['requirement'] = r['meals_needed'] or 'Groceries'
            elif r['request_type'] == 'Clothes':
                r['requirement'] = r['clothing_items'] or 'Clothes'
            else:
                r['requirement'] = f"Rs. {int(r['amount_needed'] or 0)}"
                
        # Calculate Admin Balance
        cursor.execute("SELECT SUM(amount) as s FROM donor_donations WHERE donation_type = 'money'")
        sum1 = cursor.fetchone()['s'] or 0
        cursor.execute("SELECT SUM(amount) as s FROM regular_donor_donations WHERE donation_type = 'money'")
        sum2 = cursor.fetchone()['s'] or 0
        total_donations_val = sum1 + sum2
        
        cursor.execute("SELECT SUM(amount_needed) as s FROM ngo_requests WHERE request_type = 'Money' AND status = 'Completed'")
        funds_utilised_val = cursor.fetchone()['s'] or 0
        
        admin_balance = total_donations_val - funds_utilised_val
                
        cursor.close()
    except Exception as e:
        requests_list = []
        admin_balance = 0
        print("Error fetching NGO requests:", e)
        
    return render_template('admin_Script_html/requestpage.html', requests=requests_list, admin_balance=admin_balance)

@app.route('/admin/transfer_money', methods=['POST'])
def admin_transfer_money():
    request_id = request.form.get('request_id')
    try:
        cursor = db.cursor()
        cursor.execute("UPDATE ngo_requests SET status = 'Completed' WHERE id = %s", (request_id,))
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error completing transfer:", e)
    return redirect('/adminrequestpage')

@app.route('/admintracking')
def admin_tracking():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, delivery_id, date, receiver_name, location, donation_type, quantity_details, volunteer_name, status FROM deliveries ORDER BY created_at DESC")
        deliveries = cursor.fetchall()
        for d in deliveries:
            if d['date']:
                d['formatted_date'] = d['date'].strftime('%Y-%m-%d')
            else:
                d['formatted_date'] = 'N/A'
        cursor.close()
    except Exception as e:
        deliveries = []
        print("Error fetching deliveries:", e)
        
    return render_template('admin_Script_html/tracking.html', deliveries=deliveries)

@app.route('/adminverification')
def admin_verification():
    try:
        cursor = db.cursor(dictionary=True)
        users = []
        
        cursor.execute("SELECT id, name, phone, email, city, pincode, created_at, status FROM donors")
        rows = cursor.fetchall()
        for r in rows:
            r['user_type'] = 'Individual Donor'
            r['user_type_raw'] = 'donor'
            r['contact'] = r['phone'] or r['email']
            r['formatted_date'] = r['created_at'].strftime('%d/%m/%Y') if r['created_at'] else 'N/A'
            users.append(r)
            
        cursor.execute("SELECT id, name, phone, email, city, pincode, created_at, status FROM volunteers")
        rows = cursor.fetchall()
        for r in rows:
            r['user_type'] = 'Volunteer'
            r['user_type_raw'] = 'volunteer'
            r['contact'] = r['phone'] or r['email']
            r['formatted_date'] = r['created_at'].strftime('%d/%m/%Y') if r['created_at'] else 'N/A'
            users.append(r)
            
        cursor.execute("SELECT id, name, phone, email, city, pincode, created_at, status FROM regulardonors")
        rows = cursor.fetchall()
        for r in rows:
            r['user_type'] = 'Regular Donor'
            r['user_type_raw'] = 'regulardonor'
            r['contact'] = r['phone'] or r['email']
            r['formatted_date'] = r['created_at'].strftime('%d/%m/%Y') if r['created_at'] else 'N/A'
            users.append(r)
            
        cursor.execute("SELECT id, name, phone, email, city, pincode, created_at, status FROM ngo_receivers")
        rows = cursor.fetchall()
        for r in rows:
            r['user_type'] = 'NGO Receiver'
            r['user_type_raw'] = 'ngo'
            r['contact'] = r['phone'] or r['email']
            r['formatted_date'] = r['created_at'].strftime('%d/%m/%Y') if r['created_at'] else 'N/A'
            users.append(r)
            
        users.sort(key=lambda x: x['created_at'] or datetime.min, reverse=True)
        cursor.close()
    except Exception as e:
        users = []
        print("Error fetching verification users:", e)
        
    return render_template('admin_Script_html/verification.html', users=users)

@app.route('/adminview')
def admin_view():
    user_type = request.args.get('type')
    user_id = request.args.get('id')
    user_details = {}
    
    if user_type and user_id:
        try:
            cursor = db.cursor(dictionary=True)
            table_map = {
                'donor': 'donors',
                'volunteer': 'volunteers',
                'regulardonor': 'regulardonors',
                'ngo': 'ngo_receivers'
            }
            table_name = table_map.get(user_type)
            if table_name:
                cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (user_id,))
                user_details = cursor.fetchone() or {}
                if user_details:
                    user_details['type_raw'] = user_type
                    user_details['type_display'] = user_type.replace('regular', 'Regular ').replace('ngo', 'NGO Receiver').capitalize()
            cursor.close()
        except Exception as e:
            print("Error fetching user view details:", e)
            
    return render_template('admin_Script_html/view_pg.html', user=user_details)

@app.route('/admin/verify/<user_type>/<int:user_id>/<action>')
def admin_verify_user(user_type, user_id, action):
    table_map = {
        'donor': 'donors',
        'volunteer': 'volunteers',
        'regulardonor': 'regulardonors',
        'ngo': 'ngo_receivers'
    }
    table_name = table_map.get(user_type)
    
    if table_name:
        try:
            cursor = db.cursor()
            if action == 'delete':
                cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (user_id,))
            else:
                status_val = 'Approved' if action == 'approve' else 'Rejected'
                cursor.execute(f"UPDATE {table_name} SET status = %s WHERE id = %s", (status_val, user_id))
            db.commit()
            cursor.close()
        except Exception as e:
            print("Error verifying/deleting user:", e)
            
    referrer = request.referrer
    if referrer and '/adminview_partners' in referrer:
        return redirect('/adminview_partners')
    return redirect('/adminverification')

@app.route('/admin/donation/<source>/<int:donation_id>/<action>')
def admin_update_donation(source, donation_id, action):
    table_name = 'donor_donations' if source == 'donor' else 'regular_donor_donations'
    status_map = {
        'approve': 'Approved',
        'onway': 'On The Way',
        'complete': 'Completed',
        'reject': 'Rejected'
    }
    status_val = status_map.get(action, 'Pending')
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"UPDATE {table_name} SET status = %s WHERE id = %s", (status_val, donation_id))
        
        if status_val == 'Approved':
            if source == 'donor':
                cursor.execute(f"SELECT donation_type, donor_name, city, pincode, quantity, food_category, clothing_category, description FROM {table_name} WHERE id = %s", (donation_id,))
            else:
                cursor.execute(f"SELECT donation_type, donor_name, city, pincode, quantity, food_category, description FROM {table_name} WHERE id = %s", (donation_id,))
            donation = cursor.fetchone()
            if donation and donation['donation_type'] in ['food', 'clothes']:
                dtype = 'Food' if donation['donation_type'] == 'food' else 'Clothes'
                loc = f"{donation['city']} / {donation['pincode']}"
                if dtype == 'Food':
                    qty = donation['quantity'] or 0
                    cat = donation['food_category'] or ''
                    qty_det = f"{qty} Meals ({cat})" if qty else (donation['description'] or 'Food Donation')
                else:
                    qty = donation['quantity'] or 0
                    cat = donation.get('clothing_category') or ''
                    qty_det = f"{qty} Items ({cat})" if qty else (donation['description'] or 'Clothes Donation')
                
                qty_det = qty_det or 'Details Pending'
                deliv_id = f"DLV-DON-{10000 + donation_id}"
                
                cursor.execute("SELECT id FROM deliveries WHERE delivery_id = %s", (deliv_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO deliveries (delivery_id, date, receiver_name, location, donation_type, quantity_details, volunteer_name, status)
                        VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s)
                    """, (deliv_id, 'Pending Receiver', loc, dtype, qty_det, 'Pending', 'Pending'))
        
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error updating donation status:", e)
        
    return redirect('/admindonations')

@app.route('/admin/request/<int:request_id>/<action>')
def admin_update_request(request_id, action):
    status_map = {
        'approve': 'Approved',
        'onway': 'On The Way',
        'complete': 'Completed',
        'reject': 'Rejected'
    }
    status_val = status_map.get(action, 'Pending')
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE ngo_requests SET status = %s WHERE id = %s", (status_val, request_id))
        
        if status_val == 'Approved':
            cursor.execute("SELECT request_type, meals_needed, clothing_items, ngo_name, city, pincode FROM ngo_requests WHERE id = %s", (request_id,))
            req = cursor.fetchone()
            if req and req['request_type'] in ['Food', 'Clothes']:
                dtype = req['request_type']
                loc = f"{req['city']} / {req['pincode']}"
                qty_det = req['meals_needed'] if dtype == 'Food' else req['clothing_items']
                qty_det = qty_det or 'Details Pending'
                ngo_name = req['ngo_name'] or 'Unknown NGO'
                deliv_id = f"DLV-REQ-{10000 + request_id}"
                
                cursor.execute("SELECT id FROM deliveries WHERE delivery_id = %s", (deliv_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO deliveries (delivery_id, date, receiver_name, location, donation_type, quantity_details, volunteer_name, status)
                        VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s)
                    """, (deliv_id, ngo_name, loc, dtype, qty_det, 'Pending', 'Pending'))
                    
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error updating request status:", e)
        
    return redirect('/adminrequestpage')


def extract_qty_val(val):
    if val is None:
        return 0
    if isinstance(val, int) or isinstance(val, float):
        return int(val)
    digits = ''.join(c for c in str(val) if c.isdigit())
    return int(digits) if digits else 0


@app.route('/admin/match/donation/<source>/<int:donation_id>')
def admin_match_donation(source, donation_id):
    table_name = 'donor_donations' if source == 'donor' else 'regular_donor_donations'
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"SELECT id, donation_type, donor_name, city, pincode, quantity, description FROM {table_name} WHERE id = %s", (donation_id,))
        donation = cursor.fetchone()
        if not donation:
            cursor.close()
            return "Donation not found", 404
        
        donation['source'] = source
        donation_qty = extract_qty_val(donation['quantity'])
        d_type = donation['donation_type'].lower()
        
        # Query all pending NGO requests
        cursor.execute("SELECT id, request_type, meals_needed, clothing_items, ngo_name, city, pincode, created_at FROM ngo_requests WHERE status = 'Pending'")
        all_reqs = cursor.fetchall()
        
        matching_requests = []
        for req in all_reqs:
            r_type = req['request_type'].lower()
            r_qty_str = req['meals_needed'] if r_type == 'food' else req['clothing_items']
            r_qty = extract_qty_val(r_qty_str)
            req['qty'] = r_qty
            req['formatted_date'] = req['created_at'].strftime('%d/%m/%Y') if req['created_at'] else 'N/A'
            matching_requests.append(req)
                
        cursor.close()
    except Exception as e:
        donation = {}
        matching_requests = []
        print("Error in admin_match_donation:", e)
        
    return render_template('admin_Script_html/match_pg.html', type='donation', item=donation, matches=matching_requests)


@app.route('/admin/match/request/<int:request_id>')
def admin_match_request(request_id):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, request_type, meals_needed, clothing_items, ngo_name, city, pincode, created_at FROM ngo_requests WHERE id = %s", (request_id,))
        req = cursor.fetchone()
        if not req:
            cursor.close()
            return "Request not found", 404
        
        r_type = req['request_type'].lower()
        r_qty_str = req['meals_needed'] if r_type == 'food' else req['clothing_items']
        req_qty = extract_qty_val(r_qty_str)
        
        # Query all pending donor_donations of same type
        cursor.execute("SELECT id, donation_type, donor_name, city, pincode, quantity, description, created_at FROM donor_donations WHERE status = 'Pending'")
        indiv_donations = cursor.fetchall()
        
        # Query all pending regular_donor_donations
        cursor.execute("SELECT id, donation_type, donor_name, city, pincode, quantity, description, created_at FROM regular_donor_donations WHERE status = 'Pending'")
        reg_donations = cursor.fetchall()
            
        all_donations = []
        for d in indiv_donations:
            d['source'] = 'donor'
            all_donations.append(d)
        for d in reg_donations:
            d['source'] = 'regular'
            all_donations.append(d)
            
        matching_donations = []
        for d in all_donations:
            d_qty = extract_qty_val(d['quantity'])
            d['qty'] = d_qty
            d['formatted_date'] = d['created_at'].strftime('%d/%m/%Y') if d['created_at'] else 'N/A'
            matching_donations.append(d)
                
        cursor.close()
    except Exception as e:
        req = {}
        matching_donations = []
        print("Error in admin_match_request:", e)
        
    return render_template('admin_Script_html/match_pg.html', type='request', item=req, matches=matching_donations)


@app.route('/admin/match/link/<source>/<int:donation_id>/<int:request_id>')
def admin_link_action(source, donation_id, request_id):
    table_name = 'donor_donations' if source == 'donor' else 'regular_donor_donations'
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"SELECT donation_type, donor_name, city, pincode, quantity, description FROM {table_name} WHERE id = %s", (donation_id,))
        donation = cursor.fetchone()
        
        cursor.execute("SELECT request_type, ngo_name, city, pincode, meals_needed, clothing_items FROM ngo_requests WHERE id = %s", (request_id,))
        req = cursor.fetchone()
        
        if donation and req:
            d_type = donation['donation_type'].lower()
            dtype_display = donation['donation_type'].capitalize()
            qty = extract_qty_val(donation['quantity'])
            
            r_type = req['request_type'].lower()
            r_qty_str = req['meals_needed'] if r_type == 'food' else req['clothing_items']
            
            deliv_id = f"DLV-MAT-{source}-{donation_id}-{request_id}"
            loc = f"Pickup: {donation['city']}/{donation['pincode']} -> NGO: {req['ngo_name']} in {req['city']}/{req['pincode']}"
            
            qty_unit = 'Meals' if d_type == 'food' else 'Bags'
            qty_det = f"Donor: {qty} {qty_unit} -> NGO Req: {r_qty_str}"
            
            cursor.execute("SELECT id FROM deliveries WHERE delivery_id = %s", (deliv_id,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO deliveries (delivery_id, date, receiver_name, location, donation_type, quantity_details, volunteer_name, status)
                    VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s)
                """, (deliv_id, req['ngo_name'], loc, dtype_display, qty_det, 'Pending', 'Pending'))
                
                cursor.execute(f"UPDATE {table_name} SET status = 'Matched' WHERE id = %s", (donation_id,))
                cursor.execute("UPDATE ngo_requests SET status = 'Matched' WHERE id = %s", (request_id,))
                db.commit()
        cursor.close()
    except Exception as e:
        print("Error linking donation and request:", e)
        
    return redirect('/admindonations')







                                                      # sending data to database


@app.route('/signup', methods=['POST'])
def signup():
    role = request.form['role']
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    city = request.form['city']
    pincode = request.form['pincode']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return render_template('beforelogin_Script_html/signup1.html', message="Passwords do not match")

    hashed_password = generate_password_hash(password)

    try:
        cursor = db.cursor()

        if role == "donor":
            cursor.execute("""
                INSERT INTO donors (name, phone, email, city, pincode, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, phone, email, city, pincode, hashed_password))

        elif role == "volunteer":
            import os
            from werkzeug.utils import secure_filename
            vehicle_type = request.form.get('vehicle_type', '')
            vehicle_number = request.form.get('vehicleNumber', '')
            
            file = request.files.get('uploadLicence')
            file_name = ''
            file_path = ''
            if file and file.filename:
                file_name = secure_filename(file.filename)
                upload_folder = os.path.join(app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                full_path = os.path.join(upload_folder, file_name)
                file.save(full_path)
                file_path = os.path.join('static', 'uploads', file_name).replace('\\', '/')

            cursor.execute("""
                INSERT INTO volunteers (name, phone, email, city, pincode, vehicle_type, vehicle_number, file_name, file_path, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, phone, email, city, pincode, vehicle_type, vehicle_number, file_name, file_path, hashed_password))

        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return render_template('beforelogin_Script_html/signup1.html', message="Email or phone number already registered")
        return render_template('beforelogin_Script_html/signup1.html', message=f"Database error: {err.msg}")

    return render_template('beforelogin_Script_html/signup1.html', message="Signup Successful")


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    reg_no = request.form.get('reg_no')

    # Admin is a special case since there is no admin table
    if email == "admin@gmail.com" and password == "humanitybridge":
        session['name'] = "Admin"
        session['email'] = email
        session['role'] = "admin"
        return redirect('/adminhome')

    cursor = db.cursor()

                                                    #donors table
    cursor.execute("SELECT password, name, phone, email, city, pincode FROM donors WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
            session['name'] = row[1]
            session['phone'] = row[2]
            session['email'] = row[3]
            session['city'] = row[4]
            session['pincode'] = row[5]
            session['role'] = "donor"
            cursor.close()
            return redirect('/donorhome')
        else:
            cursor.close()
            return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

                                                   #volunteers table
    cursor.execute("SELECT password, name, phone, email, city, pincode, vehicle_type FROM volunteers WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
            session['name'] = row[1]
            session['phone'] = row[2]
            session['email'] = row[3]
            session['city'] = row[4]
            session['pincode'] = row[5]
            session['role'] = "volunteer"
            session['vehicle_type'] = row[6]
            cursor.close()
            return redirect('/volunteerhome')
        else:
            cursor.close()
            return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

                                                     #regulardonors table
    if reg_no:
        cursor.execute("SELECT password, name, phone, email, city, pincode FROM regulardonors WHERE email = %s AND registration_number = %s", (email, reg_no))
        row = cursor.fetchone()
        if row:
            hashed_password = row[0]
            if check_password_hash(hashed_password, password):
                session['name'] = row[1]
                session['phone'] = row[2]
                session['email'] = row[3]
                session['city'] = row[4]
                session['pincode'] = row[5]
                session['role'] = "regulardonor"
                cursor.close()
                return redirect('/regulardonorhome')
            else:
                cursor.close()
                return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

                                                         #ngo_receivers table
    if reg_no:
        cursor.execute("SELECT password, name, phone, email, city, pincode FROM ngo_receivers WHERE email = %s AND registration_no = %s", (email, reg_no))
        row = cursor.fetchone()
        if row:
            hashed_password = row[0]
            if check_password_hash(hashed_password, password):
                session['name'] = row[1]
                session['phone'] = row[2]
                session['email'] = row[3]
                session['city'] = row[4]
                session['pincode'] = row[5]
                session['role'] = "ngo"
                cursor.close()
                return redirect('/ngohome')
            else:
                cursor.close()
                return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

    cursor.close()
    return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")






                                                    # admin add partners


@app.route('/adminadd_partner', methods=['POST'])
def admin_add_partner_post():
    partner_type = request.form.get('partner_Type') or request.form.get('partner_type')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    city = request.form.get('city')
    pincode = request.form.get('pincode')
    registration_number = request.form.get('registration_number')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return render_template('admin_Script_html/add_partner.html', message="Passwords do not match")

    hashed_password = generate_password_hash(password)

    try:
        cursor = db.cursor()

        if partner_type == "donor" or partner_type == "Regular donor":
            organization_type = request.form.get('organization_type')
            cursor.execute("""
                INSERT INTO regulardonors (partner_type, name, organization_type, phone, email, city, pincode, registration_number, password, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Approved')
            """, ("Regular donor", name, organization_type, phone, email, city, pincode, registration_number, hashed_password))

        elif partner_type == "ngo" or partner_type == "NGO/Receiver":
            cursor.execute("""
                INSERT INTO ngo_receivers (partner_type, name, phone, email, city, pincode, registration_no, password, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Approved')
            """, ("NGO/Receiver", name, phone, email, city, pincode, registration_number, hashed_password))

        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return render_template('admin_Script_html/add_partner.html', message="Email or phone number already registered")
        return render_template('admin_Script_html/add_partner.html', message=f"Database error: {err.msg}")
    except Exception as e:
        print("General Exception in admin_add_partner_post:", e)
        return render_template('admin_Script_html/add_partner.html', message=f"Error: {e}")

    return render_template('admin_Script_html/add_partner.html', message="Partner Added Successfully")


@app.route('/adminview_partners')
def admin_view_partners():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, 'donor' as type, 'regulardonor' as type_raw, organization_type as orgType, phone as contact, email, city, pincode as area, registration_number as regNum, status FROM regulardonors")
        regulardonors_data = cursor.fetchall()
        
        cursor.execute("SELECT id, name, 'ngo' as type, 'ngo' as type_raw, '' as orgType, phone as contact, email, city, pincode as area, registration_no as regNum, status FROM ngo_receivers")
        ngo_receivers_data = cursor.fetchall()
        
        partners = regulardonors_data + ngo_receivers_data
        cursor.close()
    except Exception as e:
        partners = []
        print("Database error in view partners:", e)
        
    return render_template('admin_Script_html/view_partners.html', db_partners=partners)




























@app.route('/api/user-info')
def get_user_info():
    if 'name' in session:
        return {
            'logged_in': True,
            'name': session.get('name'),
            'email': session.get('email'),
            'phone': session.get('phone', ''),
            'city': session.get('city', ''),
            'pincode': session.get('pincode', ''),
            'role': session.get('role', '')
        }
    return {'logged_in': False}


if __name__ == '__main__':
    app.run(debug=True)