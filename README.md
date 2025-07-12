# 🔄 Skill Swap Platform
*Empowering Communities Through Knowledge Exchange*

<div align="center">

[![Odoo Hackathon 2025](https://img.shields.io/badge/Odoo%20Hackathon-2025-blue.svg)](https://www.odoo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Latest-red.svg)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue.svg)](https://sqlite.org)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com)

</div>

## 🚀 Live Demo
> **[View Live App](https://skill-swap-five-mu.vercel.app/)**

## 🎬 Demo Video
> **Coming Soon!** Watch our platform in action - from user registration to successful skill swaps.

[![Demo Video Placeholder](https://via.placeholder.com/800x450/007bff/ffffff?text=🎥+Demo+Video+Coming+Soon)](https://github.com/ArnavLabh/Odoo-Hackathon-2025-Team-3661)

*Click above to view the complete demonstration once available*

---

## 💡 What is Skill Swap?

**Imagine a world where learning never stops, and everyone is both a teacher and a student.**

Skill Swap Platform transforms the way people share knowledge by creating a vibrant ecosystem where:
- 🎯 **Your expertise becomes someone else's breakthrough**
- 🌱 **Every interaction sparks mutual growth**
- 🤝 **Communities thrive through collaborative learning**
- ⚡ **Skills flow freely, barriers disappear**

Whether you're a coding wizard wanting to learn guitar, a chef eager to master photography, or a language enthusiast ready to teach conversation skills - **Skill Swap connects you with the perfect learning partner.**

## 🚀 Why Skill Swap?

### 🌍 **For Learners**
No more expensive courses or rigid schedules. Find passionate experts in your area ready to share their knowledge in exchange for yours.

### 👨‍🏫 **For Teachers**  
Transform your skills into meaningful connections. Teach what you love while learning something entirely new.

### 🏢 **For Communities**
Foster collaboration, reduce learning barriers, and create networks where knowledge multiplies exponentially.

---

## 🌟 Features

### Core Functionality
- **User Authentication** - Secure registration and login with bcrypt password hashing
- **Profile Management** - Customizable profiles with photos, location, and availability
- **Skill Management** - Add skills you offer and skills you want to learn
- **Smart Matching** - Browse and search users by skills, location, and availability
- **Swap Requests** - Send, receive, accept, and reject skill exchange requests
- **Feedback System** - Rate and review completed skill swaps
- **Privacy Controls** - Toggle between public and private profiles

### Advanced Features
- **Real-time Notifications** - Stay updated on swap requests and responses
- **Advanced Search** - Filter users by multiple criteria
- **Admin Panel** - Platform moderation and management tools
- **API Endpoints** - RESTful APIs for enhanced frontend interactions
- **Data Export** - Generate reports and analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ArnavLabh/Odoo-Hackathon-2025-Team-3661.git
   cd Odoo-Hackathon-2025-Team-3661
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or alternatively:
   ```bash
   py -m pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your preferred settings
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## 🗂️ Project Structure

```
skill-swap-platform/
├── app.py                 # Flask application factory
├── run.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── models.py              # Database models
├── routes.py              # Main application routes
├── swap_routes.py         # Swap management routes
├── admin_routes.py        # Admin panel routes
├── api_routes.py          # API endpoints
├── templates/             # HTML templates (to be created)
├── static/               # CSS, JS, images
├── instance/             # SQLite database location
└── .env                  # Environment variables
```

## 📊 Database Schema

### Core Models
- **User** - User profiles and authentication
- **Skill** - Available skills in the platform
- **UserSkill** - Links users to their offered/wanted skills
- **SwapRequest** - Skill exchange requests between users
- **Feedback** - Ratings and comments for completed swaps

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///skillswap.db
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

### Default Settings
- **Database**: SQLite (development)
- **Session Management**: Flask sessions
- **Password Hashing**: bcrypt
- **File Uploads**: Local storage in `static/uploads/`

## 🛣️ API Routes

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### User Management
- `GET /profile` - View own profile
- `GET /public_profile/<user_id>` - View public profile
- `POST /edit_profile` - Update profile

### Skill Management
- `GET /manage_skills` - Manage user skills
- `POST /add_skill` - Add new skill
- `GET /remove_skill/<skill_id>/<type>` - Remove skill

### Swap Operations
- `GET /dashboard` - User dashboard
- `POST /swaps/request_swap/<user_id>` - Create swap request
- `GET /swaps/accept_swap/<request_id>` - Accept request
- `GET /swaps/reject_swap/<request_id>` - Reject request
- `POST /submit_feedback` - Submit feedback

### Search & Browse
- `GET /browse` - Browse users
- `GET /search_results` - Advanced search
- `GET /api/skills/search` - Skill autocomplete
- `GET /api/users/search` - User search

For complete API documentation, see [ROUTES_DOCUMENTATION.md](./ROUTES_DOCUMENTATION.md)

## 👨‍💼 Admin Panel

Access admin features at `/admin/admin_dashboard` (requires admin privileges):

- **User Moderation** - Ban/unban users, view profiles
- **Swap Management** - Monitor and moderate exchanges
- **Skill Moderation** - Remove inappropriate skills
- **Broadcasting** - Send platform-wide messages
- **Analytics** - Download user and swap reports

## 🔒 Security Features

- **Password Security** - bcrypt hashing with salt
- **Session Management** - Secure Flask sessions
- **Input Validation** - Form data sanitization
- **Admin Protection** - Role-based access control
- **Privacy Controls** - User-controlled profile visibility

## 🧪 Testing

Run the test script to verify installation:

```bash
python test_app.py
```

This will test:
- App creation and initialization
- Database model imports
- Route registration
- Blueprint configuration

## 🔄 Development Workflow

1. **Start the development server**
   ```bash
   python run.py
   ```

2. **Make changes** to Python files (auto-reload enabled)

3. **Database changes**
   - Modify models in `models.py`
   - Restart the application to apply schema changes

4. **Add new routes**
   - Add to appropriate blueprint file
   - Register in `app.py` if creating new blueprint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is created for the Odoo Hackathon 2025.

## 🆘 Troubleshooting

### Common Issues

**Database not found**
```bash
# Delete existing database and restart
rm instance/skillswap.db
python run.py
```

**Module import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Permission errors**
```bash
# Check virtual environment activation
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate
```

### Getting Help

- Check the [ROUTES_DOCUMENTATION.md](./ROUTES_DOCUMENTATION.md) for detailed API info
- Review error logs in the terminal output
- Ensure all dependencies are installed correctly

## 🎯 Roadmap

- [ ] Email notifications for swap requests
- [ ] Real-time chat for matched users
- [ ] Mobile-responsive frontend
- [ ] Advanced analytics dashboard
- [ ] Integration with external skill verification
- [ ] Multi-language support

---

**Built with ❤️ for Odoo Hackathon 2025**
