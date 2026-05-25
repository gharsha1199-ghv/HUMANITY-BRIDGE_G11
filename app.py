from flask import Flask, render_template,request, redirect
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

db=mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Sharjina@74802',
    database='humanity_bridge'
)



app = Flask(__name__)







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

@app.route('/donordonatecloths')
def donorlogin_donatecloths():
    return render_template('donorlogin_Script_html/donatecloths_pg.html')

@app.route('/donordonatefood')
def donorlogin_donatefood():
    return render_template('donorlogin_Script_html/donatefood_pg.html')

@app.route('/donordonatemoney')
def donorlogin_donatemoney():
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
    return render_template('regulardonar_Script_html/donatecloths_pg.html')

@app.route('/regulardonordonatefood')
def regulardonar_donatefood():
    return render_template('regulardonar_Script_html/donatefood_pg.html')

@app.route('/regulardonordonatemoney')
def regulardonar_donatemoney():
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

@app.route('/ngogethelp_clothes')
def ngo_gethelp_clothes():
    return render_template('ngo_Script_html/gethelp_clothes.html')

@app.route('/ngogethelp_food')
def ngo_gethelp_food():
    return render_template('ngo_Script_html/gethelp_food.html')

@app.route('/ngogethelp_money')
def ngo_gethelp_money():
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
    return render_template('admin_Script_html/donations.html')

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
    return render_template('admin_Script_html/index.html')

@app.route('/adminmyaccount')
def admin_myaccount():
    return render_template('admin_Script_html/myaccount_pg.html')

@app.route('/adminourwork')
def admin_ourwork():
    return render_template('admin_Script_html/ourwork_pg.html')

@app.route('/adminrequestpage')
def admin_requestpage():
    return render_template('admin_Script_html/requestpage.html')

@app.route('/admintracking')
def admin_tracking():
    return render_template('admin_Script_html/tracking.html')

@app.route('/adminverification')
def admin_verification():
    return render_template('admin_Script_html/verification.html')

@app.route('/adminview')
def admin_view():
    return render_template('admin_Script_html/view_pg.html')







# sending data to database
# from flask import request, redirect, render_template
# signup donor & volunteer

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

# static values for testing
    if email == "admin@gmail.com" and password == "humanitybridge":
        return redirect('/adminhome')
    elif email == "ngo@gmail.com" and password == "humanitybridge":
        return redirect('/ngohome')
    elif email == "donar@gmail.com" and password == "humanitybridge":
        return redirect('/donorhome')
    elif email == "regulardonar@gmail.com" and password == "humanitybridge":
        return redirect('/regulardonorhome')
    elif email == "volunteer@gmail.com" and password == "humanitybridge":
        return redirect('/volunteerhome')
    elif email == "b4login@gmail.com" and password == "humanitybridge":
        return redirect('/')

    #database tables
    cursor = db.cursor()

    #donors table
    cursor.execute("SELECT password FROM donors WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
            cursor.close()
            return redirect('/donorhome')
        else:
            cursor.close()
            return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

    #volunteers table
    cursor.execute("SELECT password FROM volunteers WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
            cursor.close()
            return redirect('/volunteerhome')
        else:
            cursor.close()
            return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

    #regulardonors table
    cursor.execute("SELECT password FROM regulardonors WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
            cursor.close()
            return redirect('/regulardonorhome')
        else:
            cursor.close()
            return render_template('beforelogin_Script_html/login_pg.html', error="Invalid Email or Password!")

    #ngo_receivers table
    cursor.execute("SELECT password FROM ngo_receivers WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if check_password_hash(hashed_password, password):
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
        # Fetch from regulardonors table
        cursor.execute("SELECT name, 'donor' as type, organization_type as orgType, phone as contact, email, city, pincode as area, registration_number as regNum, 'Approved' as status FROM regulardonors")
        regulardonors_data = cursor.fetchall()
        
        # Fetch from ngo_receivers table
        cursor.execute("SELECT name, 'ngo' as type, '' as orgType, phone as contact, email, city, pincode as area, registration_no as regNum, 'Approved' as status FROM ngo_receivers")
        ngo_receivers_data = cursor.fetchall()
        
        partners = regulardonors_data + ngo_receivers_data
        cursor.close()
    except Exception as e:
        partners = []
        print("Database error in view partners:", e)
        
    return render_template('admin_Script_html/view_partners.html', db_partners=partners)








































if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)