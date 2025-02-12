from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from uuid import uuid4
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Folder configurations
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PATIENT_DATA_FOLDER'] = 'patient_data/'
app.config['PATIENT_IMAGES_FOLDER'] = 'patient_images/'
app.config['REPORT_IMAGES_FOLDER'] = 'report_images/'
app.config['ENCRYPTION_KEYS_FOLDER'] = 'encryption_keys/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Ensure necessary folders exist
for folder in [app.config['UPLOAD_FOLDER'], 
               app.config['PATIENT_DATA_FOLDER'], 
               app.config['PATIENT_IMAGES_FOLDER'], 
               app.config['REPORT_IMAGES_FOLDER'], 
               app.config['ENCRYPTION_KEYS_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# AES encryption key (should be securely stored)
KEY = get_random_bytes(16)

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + encrypted_data).decode()

def decrypt_data(encrypted_data, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=encrypted_data[:AES.block_size])
        decrypted = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
        return decrypted.decode('utf-8')
    except (ValueError, KeyError) as e:
        logging.error(f"Text decryption failed: {e}")
        raise

def encrypt_file(file_data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    padded_data = pad(file_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return cipher.iv + encrypted_data

def decrypt_file(encrypted_file_data, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=encrypted_file_data[:AES.block_size])
        decrypted = unpad(cipher.decrypt(encrypted_file_data[AES.block_size:]), AES.block_size)
        return decrypted
    except (ValueError, KeyError) as e:
        logging.error(f"File decryption failed: {e}")
        raise

def parse_form_data(decrypted_form_data):
    form_data = {}
    for line in decrypted_form_data.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            form_data[key.strip()] = value.strip()
    return form_data

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user_folder = os.path.join('data/users', username_hash)
    if not os.path.exists(user_folder):
        return jsonify({"error": "Invalid username or password"}), 401

    username_file = os.path.join(user_folder, 'username.txt')
    password_file = os.path.join(user_folder, 'password.txt')

    with open(username_file, 'r') as f:
        stored_username_hash = f.read().strip()
    with open(password_file, 'r') as f:
        stored_password_hash = f.read().strip()

    if stored_username_hash == username_hash and stored_password_hash == password_hash:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401
    
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/add-patient')
def add_patient():
    return render_template('patient.html')

@app.route('/search-patient')
def search_patient():
    return render_template('search.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        visit_id = request.form['visit-id']
        unique_folder_name = str(uuid4())

        patient_data_path = os.path.join(app.config['PATIENT_DATA_FOLDER'], visit_id)
        patient_images_path = os.path.join(app.config['PATIENT_IMAGES_FOLDER'], visit_id)
        report_images_path = os.path.join(app.config['REPORT_IMAGES_FOLDER'], visit_id)
        encryption_keys_path = os.path.join(app.config['ENCRYPTION_KEYS_FOLDER'], visit_id)

        os.makedirs(patient_data_path, exist_ok=True)
        os.makedirs(patient_images_path, exist_ok=True)
        os.makedirs(report_images_path, exist_ok=True)
        os.makedirs(encryption_keys_path, exist_ok=True)

        first_name = request.form['first-name']
        last_name = request.form['last-name']
        date_of_birth = request.form['date-of-birth']
        blood_group = request.form['blood-group']
        gender = request.form['gender']
        contact_info = request.form['contact-info']
        state = request.form['inputState']
        visit_date = request.form['visit-date']
        visit_time = request.form['visit-time']
        doctor = request.form['doctor']
        specialty = request.form['specialty']
        diagnosis = request.form['diagnosis']
        past_medical_conditions = request.form['past-medical-conditions']
        current_medications = request.form['current-medications']
        allergies = request.form['allergies']
        immunization_records = request.form['immunization-records']

        form_data = f"""
        Patient Information:
        First Name: {first_name}
        Last Name: {last_name}
        Date of Birth: {date_of_birth}
        Blood Group: {blood_group}
        Gender: {gender}
        Contact Info: {contact_info}
        State: {state}
        Visit Date: {visit_date}
        Visit Time: {visit_time}
        Doctor: {doctor}
        Specialty: {specialty}
        Diagnosis: {diagnosis}
        Past Medical Conditions: {past_medical_conditions}
        Current Medications: {current_medications}
        Allergies: {allergies}
        Immunization Records: {immunization_records}
        """

        encrypted_form_data = encrypt_data(form_data)
        form_data_file = os.path.join(patient_data_path, "form_data.txt")
        with open(form_data_file, 'w') as f:
            f.write(encrypted_form_data)

        if 'patient-image' in request.files:
            patient_image = request.files['patient-image']
            if patient_image and allowed_file(patient_image.filename):
                patient_image_data = patient_image.read()
                encrypted_image_data = encrypt_file(patient_image_data)
                encrypted_image_path = os.path.join(patient_images_path, 'encrypted_patient_image.enc')
                with open(encrypted_image_path, 'wb') as f:
                    f.write(encrypted_image_data)

        if 'medical-report-images' in request.files:
            medical_report_images = request.files.getlist('medical-report-images')
            for report in medical_report_images:
                if report and allowed_file(report.filename):
                    report_data = report.read()
                    encrypted_report_data = encrypt_file(report_data)
                    encrypted_report_path = os.path.join(report_images_path, f'encrypted_{report.filename}.enc')
                    with open(encrypted_report_path, 'wb') as f:
                        f.write(encrypted_report_data)

        key_file = os.path.join(encryption_keys_path, 'encryption_key.key')
        with open(key_file, 'wb') as f:
            f.write(KEY)

        return redirect(url_for('main'))
    

@app.route('/fetch_patient_data/<visit_id>', methods=['GET'])
def fetch_patient_data(visit_id):
    logging.info(f"Fetching data for visit ID: {visit_id}")
    patient_data_path = os.path.join(app.config['PATIENT_DATA_FOLDER'], visit_id)
    patient_images_path = os.path.join(app.config['PATIENT_IMAGES_FOLDER'], visit_id)
    report_images_path = os.path.join(app.config['REPORT_IMAGES_FOLDER'], visit_id)
    encryption_keys_path = os.path.join(app.config['ENCRYPTION_KEYS_FOLDER'], visit_id)

    key_file_path = os.path.join(encryption_keys_path, 'encryption_key.key')
    try:
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()
    except FileNotFoundError:
        logging.error("Encryption key not found for visit ID %s", visit_id)
        return jsonify({"error": "Encryption key not found"}), 404

    form_data_file = os.path.join(patient_data_path, 'form_data.txt')
    try:
        with open(form_data_file, 'r') as f:
            encrypted_form_data = base64.b64decode(f.read())
            decrypted_form_data = decrypt_data(encrypted_form_data, key)
            form_data = parse_form_data(decrypted_form_data)
    except FileNotFoundError:
        logging.error("Form data not found for visit ID %s", visit_id)
        return jsonify({"error": "Form data not found"}), 404
    except Exception as e:
        logging.error(f"Error decrypting form data: {e}")
        return jsonify({"error": "Failed to decrypt form data"}), 500

    encrypted_image_path = os.path.join(patient_images_path, 'encrypted_patient_image.enc')
    image_data = None
    try:
        with open(encrypted_image_path, 'rb') as f:
            encrypted_image_data = f.read()
            decrypted_image_data = decrypt_file(encrypted_image_data, key)
            image_data = base64.b64encode(decrypted_image_data).decode()
    except FileNotFoundError:
        logging.warning("Patient image not found for visit ID %s", visit_id)

    report_data = []
    if os.path.exists(report_images_path):
        for report_file in os.listdir(report_images_path):
            if report_file.endswith('.enc'):
                try:
                    with open(os.path.join(report_images_path, report_file), 'rb') as f:
                        encrypted_report_data = f.read()
                        decrypted_report_data = decrypt_file(encrypted_report_data, key)
                        report_data.append(base64.b64encode(decrypted_report_data).decode())
                except Exception as e:
                    logging.warning(f"Error decrypting report file {report_file}: {e}")

    return jsonify({
        "form_data": form_data,
        "image_data": image_data,
        "report_data": report_data,
    })


if __name__ == '__main__':
    app.run(debug=True)
