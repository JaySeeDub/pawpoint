from Imports import *

#initialize app
app = Flask(__name__)
CORS(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.cache = {}
# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database/set a secret key
app.config['SECRET_KEY'] = '00123801989349857773048209842893048'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import *
from User_DB import *

#For hashing passwords
bcrypt = Bcrypt(app)

#reload user id from database
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})  # SQLite needs this argument

# Create a sessionmaker instance to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

#reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        #db.drop_all()
        #app.jinja_env.cache = {}
        db.create_all()
    app.run(debug=True)