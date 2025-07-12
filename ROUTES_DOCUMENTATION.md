# Skill Swap Platform - Backend Routes Documentation

## 🔐 Authentication Routes (Main Blueprint)
- `GET /` - Landing page (index.html)
- `GET|POST /register` - User registration (register.html)
- `GET|POST /login` - User login (login.html)
- `GET /logout` - User logout (redirect)

## 👤 User Profile Routes (Main Blueprint)
- `GET /profile` - View own profile (profile.html)
- `GET|POST /edit_profile` - Edit profile (edit_profile.html)
- `GET /public_profile/<user_id>` - View another user's profile (public_profile.html)

## 🔧 Skills Management Routes (Main Blueprint)
- `GET /manage_skills` - Manage user skills (manage_skills.html)
- `POST /add_skill` - Add skill to user profile
- `GET /remove_skill/<skill_id>/<skill_type>` - Remove skill from profile

## 🔍 Browse & Search Routes (Main Blueprint)
- `GET /browse` - Browse users (browse.html)
- `GET /user/<user_id>` - View user profile (view_user.html)
- `GET /search_results` - Advanced search with filters (search_results.html)

## 📊 Dashboard & Core Features (Main Blueprint)
- `GET /dashboard` - User dashboard (dashboard.html)
- `GET /swap_request/<to_user_id>` - Show swap request form (swap_request.html)
- `GET /swap_list` - View all swap requests (swap_list.html)
- `GET /feedback_form/<swap_id>` - Feedback form (feedback_form.html)
- `POST /submit_feedback` - Submit feedback (redirect)

## 🔄 Swap Management Routes (Swaps Blueprint - /swaps prefix)
- `GET|POST /swaps/request_swap/<to_user_id>` - Create swap request
- `GET /swaps/accept_swap/<request_id>` - Accept swap request
- `GET /swaps/reject_swap/<request_id>` - Reject swap request
- `GET /swaps/cancel_swap/<request_id>` - Cancel swap request
- `GET /swaps/complete_swap/<request_id>` - Mark swap as complete
- `GET|POST /swaps/feedback/<request_id>` - Leave feedback
- `GET /swaps/swap/<request_id>` - View swap details

## ⚙️ Settings & Privacy Routes (Main Blueprint)
- `GET|POST /privacy_toggle` - Toggle profile privacy (privacy_toggle.html)
- `GET /notifications` - View notifications (notifications.html)

## 🔧 Admin Routes (Admin Blueprint - /admin prefix)
### Dashboard & Overview
- `GET /admin/admin_dashboard` - Admin overview (admin_dashboard.html)

### User Management
- `GET /admin/user_list` - View/moderate users (user_list.html)
- `GET /admin/ban_user/<user_id>` - Ban user
- `GET /admin/unban_user/<user_id>` - Unban user
- `GET /admin/delete_user/<user_id>` - Delete user

### Swap Management
- `GET /admin/swap_moderation` - View all swaps (swap_moderation.html)
- `GET /admin/force_complete_swap/<swap_id>` - Force complete swap
- `GET /admin/cancel_swap_admin/<swap_id>` - Admin cancel swap

### Skill Management
- `GET /admin/skill_moderation` - Moderate skills (skill_moderation.html)
- `GET /admin/delete_skill/<skill_id>` - Delete skill

### Broadcasting & Reports
- `GET|POST /admin/broadcast` - Send platform messages (broadcast.html)
- `GET /admin/download_user_report` - Download user report (CSV)
- `GET /admin/download_swap_report` - Download swap report (CSV)
- `GET /admin/download_feedback_report` - Download feedback report (CSV)

## 🔌 API Routes (API Blueprint)
### Search APIs
- `GET /api/skills/search?q=<query>` - Search skills for autocomplete
- `GET /api/users/search?q=<query>` - Search users by name
- `GET /api/user/<user_id>/skills` - Get user's skills

### Data APIs
- `POST /api/swap/<swap_id>/status` - Update swap status via JSON
- `GET /api/stats/dashboard` - Get dashboard statistics
- `GET /api/notifications/unread` - Get unread notification count

## 🚫 Error Handling
- `404` - Custom 404 page (404.html)

## 🔒 Security Features
- **Password Hashing**: Uses bcrypt for secure password storage
- **Google OAuth**: Secure authentication with Google accounts
- **Session Management**: Flask sessions for authentication
- **Admin Protection**: Admin-only decorator for sensitive routes
- **Privacy Controls**: Public/private profile toggle
- **Input Validation**: Custom secure filename handling
- **Clean Dependencies**: No werkzeug or babel dependencies

## 📁 Template Files Required
### Authentication
- `login.html` - User login form
- `register.html` - User registration form

### User Account & Profile
- `profile.html` - User's own profile view
- `edit_profile.html` - Edit profile form
- `public_profile.html` - View another user's profile

### Skill Swap Core
- `dashboard.html` - Main user dashboard
- `swap_request.html` - Send swap request form
- `swap_list.html` - View all swap requests
- `feedback_form.html` - Leave rating/comment
- `search_results.html` - Search and filter results

### Admin Panel
- `admin_dashboard.html` - Admin overview
- `user_list.html` - User moderation
- `swap_moderation.html` - Swap management
- `broadcast.html` - Send system messages

### Misc
- `base.html` - Common layout template
- `404.html` - Error page
- `index.html` - Landing page
- `notifications.html` - Notifications list
- `privacy_toggle.html` - Privacy settings

## 🏗️ Database Models
- **User** - Profile, authentication, settings
- **Skill** - Available skills
- **UserSkill** - User-skill relationships (offered/wanted)
- **SwapRequest** - Skill exchange requests
- **Feedback** - Ratings and comments

## 🚀 Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python run.py`
3. Access at: `http://127.0.0.1:5000`

## 🔧 Configuration
- SQLite database with bcrypt password hashing
- Google OAuth integration for seamless authentication
- Environment variables for configuration
- Session-based authentication
- Custom secure file upload handling
- Minimal dependencies (no werkzeug, no babel)
