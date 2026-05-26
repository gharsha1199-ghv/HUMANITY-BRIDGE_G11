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
    return render_template('donorlogin_Script_html/donardashboard_pg.html')

@app.route('/donarmyaccount')
def donorlogin_myaccount():
    return render_template('donorlogin_Script_html/myaccount_pg.html')



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
                    prepared_time, pickup_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'food', donor_name, phone, city, pincode, full_address,
                food_category, expiry_date, expiry_time, description, is_hygienic,
                prepared_time, pickup_time
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
                    amount, purpose, payment_method, upi_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'money', donor_name, phone, city, pincode, full_address,
                amount, purpose, payment_method, upi_id
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
    return render_template('donorlogin_Script_html/donation_history_pg.html')

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
    return render_template('regulardonar_Script_html/donardashboard_pg.html')

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
                    amount, purpose, payment_method, upi_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'money', donor_name, phone, city, pincode, full_address,
                amount, purpose, payment_method, upi_id
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
    return render_template('regulardonar_Script_html/donation_history_pg.html')

@app.route('/regulardonorformsubmit')
def regulardonar_formsubmit():
    return render_template('regulardonar_Script_html/formsubmit.html')

@app.route('/regulardonorgallery')
def regulardonar_gallery():
    return render_template('regulardonar_Script_html/gallery_pg.html')

@app.route('/regulardonorhome')
def regulardonar_index():
    return render_template('regulardonar_Script_html/index.html')

@app.route('/regulardonormyaccount')
def regulardonar_myaccount():
    return render_template('regulardonar_Script_html/myaccount_pg.html')

@app.route('/regulardonorourwork')
def regulardonar_ourwork():
    return render_template('regulardonar_Script_html/ourwork_pg.html')

@app.route('/regulardonorregulardonarverification')
def regulardonar_regulardonarverification():
    return render_template('regulardonar_Script_html/regulardonarverification.html')










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

@app.route('/ngomyaccount')
def ngo_myaccount():
    return render_template('ngo_Script_html/myaccount_pg.html')

@app.route('/ngongo_history')
def ngo_ngo_history():
    return render_template('ngo_Script_html/ngo_history_pg.html')

@app.route('/ngongoverification')
def ngo_ngoverification():
    return render_template('ngo_Script_html/ngoverification.html')

@app.route('/ngoourwork')
def ngo_ourwork():
    return render_template('ngo_Script_html/ourwork_pg.html')

@app.route('/ngorecieverdash')
def ngo_recieverdash():
    return render_template('ngo_Script_html/recieverdash.html')








                                                        # volunteer login pages


@app.route('/volunteerhome')
def volunteer_index():
    return render_template('volunteer_Script_html/index.html')

@app.route('/volunteermyaccount')
def volunteer_myaccount():
    return render_template('volunteer_Script_html/myaccount_pg.html')

@app.route('/volunteerorders')
def volunteer_orders():
    return render_template('volunteer_Script_html/orders.html')

@app.route('/volunteertracking')
def volunteer_tracking():
    return render_template('volunteer_Script_html/tracking.html')

@app.route('/volunteervolunteer_history')
def volunteer_volunteer_history():
    return render_template('volunteer_Script_html/volunteer_history_pg.html')





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
        cursor.execute("SELECT COUNT(*) as c FROM donor_donations WHERE status = 'Pending'")
        pd1 = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM regular_donor_donations WHERE status = 'Pending'")
        pd2 = cursor.fetchone()['c']
        pending_donations_count = pd1 + pd2
        
        cursor.execute("SELECT COUNT(*) as c FROM ngo_requests WHERE status = 'Pending'")
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
        cursor.close()
    except Exception as e:
        requests_list = []
        print("Error fetching NGO requests:", e)
        
    return render_template('admin_Script_html/requestpage.html', requests=requests_list)

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
    status_val = 'Approved' if action == 'approve' else 'Rejected'
    
    if table_name:
        try:
            cursor = db.cursor()
            cursor.execute(f"UPDATE {table_name} SET status = %s WHERE id = %s", (status_val, user_id))
            db.commit()
            cursor.close()
        except Exception as e:
            print("Error verifying user:", e)
            
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
        cursor = db.cursor()
        cursor.execute(f"UPDATE {table_name} SET status = %s WHERE id = %s", (status_val, donation_id))
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
        cursor = db.cursor()
        cursor.execute("UPDATE ngo_requests SET status = %s WHERE id = %s", (status_val, request_id))
        db.commit()
        cursor.close()
    except Exception as e:
        print("Error updating request status:", e)
        
    return redirect('/adminrequestpage')







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
            vehicle_type = request.form.get('vehicle_type')

            cursor.execute("""
                INSERT INTO volunteers (name, phone, email, city, pincode, vehicle_type, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, phone, email, city, pincode, vehicle_type, hashed_password))

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

                                              # static values for testing
    if email == "admin@gmail.com" and password == "humanitybridge":
        session['name'] = "Admin"
        session['email'] = email
        session['role'] = "admin"
        return redirect('/adminhome')
    elif email == "ngo@gmail.com" and reg_no == "123456" and password == "humanitybridge":
        session['name'] = "Sunshine Orphanage"
        session['email'] = "ngo@gmail.com"
        session['phone'] = "+91 90123 45678"
        session['city'] = "Hyderabad"
        session['pincode'] = "500001"
        session['role'] = "ngo"
        return redirect('/ngohome')
    elif email == "donar@gmail.com" and password == "humanitybridge":
        session['name'] = "Harsha Vardhan"
        session['email'] = email
        session['phone'] = "+91 98765 43210"
        session['city'] = "Hyderabad"
        session['pincode'] = "500001"
        session['role'] = "donor"
        return redirect('/donorhome')
    elif email == "regulardonar@gmail.com" and reg_no == "123456" and password == "humanitybridge":
        session['name'] = "Santhosh Dhaba"
        session['email'] = "regulardonar@gmail.com"
        session['phone'] = "+91 99999 88888"
        session['city'] = "Hyderabad"
        session['pincode'] = "500001"
        session['role'] = "regulardonor"
        return redirect('/regulardonorhome')
    elif email == "volunteer@gmail.com" and password == "humanitybridge":
        session['name'] = "Volunteer User"
        session['email'] = email
        session['phone'] = "+91 88888 77777"
        session['city'] = "Hyderabad"
        session['pincode'] = "500001"
        session['role'] = "volunteer"
        return redirect('/volunteerhome')
    elif email == "b4login@gmail.com" and password == "humanitybridge":
        session['name'] = "Before Login"
        session['email'] = email
        session['role'] = "beforelogin"
        return redirect('/')

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
    cursor.execute("SELECT password, name, phone, email, city, pincode FROM volunteers WHERE email = %s", (email,))
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
                INSERT INTO regulardonors (partner_type, name, organization_type, phone, email, city, pincode, registration_number, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ("Regular donor", name, organization_type, phone, email, city, pincode, registration_number, hashed_password))

        elif partner_type == "ngo" or partner_type == "NGO/Receiver":
            cursor.execute("""
                INSERT INTO ngo_receivers (partner_type, name, phone, email, city, pincode, registration_no, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        cursor.execute("SELECT name, 'donor' as type, organization_type as orgType, phone as contact, email, city, pincode as area, registration_number as regNum, status FROM regulardonors")
        regulardonors_data = cursor.fetchall()
        
        cursor.execute("SELECT name, 'ngo' as type, '' as orgType, phone as contact, email, city, pincode as area, registration_no as regNum, status FROM ngo_receivers")
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