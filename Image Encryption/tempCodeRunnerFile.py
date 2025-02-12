# # Routes
# @app.route('/')
# def index():
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({"error": "Username and password are required"}), 400

#     username_hash = hashlib.sha256(username.encode()).hexdigest()
#     password_hash = hashlib.sha256(password.encode()).hexdigest()

#     user_folder = os.path.join('data/users', username_hash)
#     if not os.path.exists(user_folder):
#         return jsonify({"error": "Invalid username or password"}), 401

#     username_file = os.path.join(user_folder, 'username.txt')
#     password_file = os.path.join(user_folder, 'password.txt')

#     with open(username_file, 'r') as f:
#         stored_username_hash = f.read().strip()
#     with open(password_file, 'r') as f:
#         stored_password_hash = f.read().strip()

#     if stored_username_hash == username_hash and stored_password_hash == password_hash:
#         return jsonify({"message": "Login successful!"})
#     else:
#         return jsonify({"error": "Invalid username or password"}), 401