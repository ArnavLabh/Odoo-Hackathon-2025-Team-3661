// Skill Swap - Main JavaScript File

// Language translations
const translations = {
    en: {
    // Navigation and Common
    'skill-swap': 'Skill Swap',
    'tagline': 'Swap skills. Grow together.',
    'hero-title': 'Connect, Learn, and Grow with Skill Swap',
    'hero-subtitle': 'Join our community of learners and share your skills with others. Learn new abilities while teaching what you know best.',
    'get-started': 'Get Started',
    'learn-more': 'Learn More',
    'login': 'Login',
    'register': 'Register',
    'browse-users': 'Browse Users',
    'dashboard': 'Dashboard',
    'profile': 'Profile',
    'logout': 'Logout',
    'features': 'Features',
    'how-it-works': 'How It Works',
    'testimonials': 'Testimonials',
    'footer-text': '© 2025 Skill Swap Platform. Connect, Learn, Grow Together.',
    'name': 'Name',
    'email': 'Email',
    'password': 'Password',
    'location': 'Location',
    'availability': 'Availability',
    'submit': 'Submit',
    'or': 'or',
    'already-have-account': 'Already have an account?',
    'dont-have-account': 'Don\'t have an account?',
            'sign-up': 'Sign Up',
        'sign-in': 'Sign In',
        
        // Additional translations for HTML elements
        'platform': 'Platform',
        'home': 'Home',
        'join-now': 'Join Now',
        'support': 'Support',
        'help-center': 'Help Center',
        'community-guidelines': 'Community Guidelines',
        'safety-tips': 'Safety Tips',
        'contact-us': 'Contact Us',
        'legal': 'Legal',
        'privacy-policy': 'Privacy Policy',
        'terms-of-service': 'Terms of Service',
        'cookie-policy': 'Cookie Policy',
        'dmca': 'DMCA',
        'company': 'Company',
        'about-us': 'About Us',
        'careers': 'Careers',
        'press': 'Press',
        'blog': 'Blog',
        'secure': 'Secure',
        'community-driven': 'Community Driven',
        'global': 'Global',
        'my-account': 'My Account',
        'welcome-back': 'Welcome back! Please sign in to your account',
        'continue-with-google': 'Continue with Google',
        'forgot-password': 'Forgot your password?',
        'reset-password': 'Reset Password',
        'new-password': 'New password',
        'confirm-password': 'Confirm password',
        'send-reset-link': 'Send Reset Link',
        'back-to-login': 'Back to login',
        'remember-password': 'Remember your password?',
        'forgot-password-title': 'Forgot Password?',
        'forgot-password-subtitle': 'No worries! Enter your email address and we\'ll send you a link to reset your password.',
        'enter-email-help': 'Enter the email address associated with your Skill Swap account below.',
        'email-sent': 'Email Sent!',
        'reset-link-sent': 'If an account with that email exists, we\'ve sent password reset instructions.',
        'security-tips': 'Security Tips',
        'check-spam-folder': 'Check your spam/junk folder if you don\'t see the email',
        'reset-link-expires': 'The reset link will expire in 1 hour for security',
        'verify-email-address': 'If you don\'t receive an email, verify your email address',
        'contact-support': 'Contact support if you continue having issues',
        'create-account': 'Create one',
        'enter-new-password': 'Enter your new password below',
    // Authentication
    'welcome-back': 'Welcome back! Please sign in to your account',
    'continue-with-google': 'Continue with Google',
    'continue-with-github': 'Continue with GitHub',
    'forgot-password': 'Forgot your password?',
    'reset-password': 'Reset Password',
    'new-password': 'New password',
    'confirm-password': 'Confirm password',
    'send-reset-link': 'Send Reset Link',
    'password-reset-success': 'Your password has been reset successfully. You can now login with your new password.',
    'password-reset-instructions': 'Password reset instructions have been sent to your email.',
    'invalid-reset-token': 'Invalid or expired reset token. Please request a new password reset.',
    'passwords-dont-match': 'Passwords do not match.',
    'password-too-short': 'Password must be at least 6 characters long.',
    'registration-successful': 'Registration successful! Welcome to Skill Swap!',
    'invalid-credentials': 'Invalid email or password.',
    'account-banned': 'Your account has been banned. Please contact support.',
    'oauth-login-required': 'This account was created with Google. Please use "Continue with Google" to login.',
    'logged-out': 'You have been logged out successfully.',
    // Dashboard
    'welcome': 'Welcome',
    'recent-activity': 'Recent Activity',
    'sent-requests': 'Sent Requests',
    'received-requests': 'Received Requests',
    'my-skills': 'My Skills',
    'offered-skills': 'Offered Skills',
    'wanted-skills': 'Wanted Skills',
    'recent-feedback': 'Recent Feedback',
    'no-activity': 'No recent activity',
    'view-all': 'View All',
    'pending': 'Pending',
    'accepted': 'Accepted',
    'rejected': 'Rejected',
    'cancelled': 'Cancelled',
    'completed': 'Completed',
    // Profile
    'edit-profile': 'Edit Profile',
    'profile-updated': 'Profile updated successfully!',
    'public-profile': 'Public Profile',
    'private-profile': 'Private Profile',
    'profile-privacy': 'Profile Privacy',
    'make-public': 'Make Public',
    'make-private': 'Make Private',
    'upload-photo': 'Upload Photo',
    'change-photo': 'Change Photo',
    'remove-photo': 'Remove Photo',
    'about-me': 'About Me',
    'contact-info': 'Contact Information',
    'account-settings': 'Account Settings',
    // Skills
    'manage-skills': 'Manage Skills',
    'add-skill': 'Add Skill',
    'remove-skill': 'Remove Skill',
    'skill-name': 'Skill Name',
    'skill-type': 'Skill Type',
    'offered': 'Offered',
    'wanted': 'Wanted',
    'skill-added': 'Skill added successfully!',
    'skill-removed': 'Skill removed successfully!',
    'no-skills': 'No skills added yet',
    'search-skills': 'Search skills...',
    // Swap Requests
    'swap-request': 'Swap Request',
    'request-swap': 'Request Swap',
    'swap-requests': 'Swap Requests',
    'swap-list': 'Swap List',
    'create-swap': 'Create Swap',
    'accept-swap': 'Accept Swap',
    'reject-swap': 'Reject Swap',
    'cancel-swap': 'Cancel Swap',
    'complete-swap': 'Complete Swap',
    'swap-details': 'Swap Details',
    'swap-created': 'Swap request created successfully!',
    'swap-accepted': 'Swap request accepted!',
    'swap-rejected': 'Swap request rejected.',
    'swap-cancelled': 'Swap request cancelled.',
    'swap-completed': 'Swap completed successfully!',
    'no-swaps': 'No swap requests found',
    // Feedback
    'feedback': 'Feedback',
    'leave-feedback': 'Leave Feedback',
    'submit-feedback': 'Submit Feedback',
    'feedback-submitted': 'Thank you for your feedback!',
    'rating': 'Rating',
    'comment': 'Comment',
    'overall-rating': 'Overall Rating',
    'no-feedback': 'No feedback yet',
    'feedback-already-given': 'You have already left feedback for this swap.',
    // Browse and Search
    'browse': 'Browse',
    'search': 'Search',
    'search-users': 'Search Users',
    'search-results': 'Search Results',
    'filter-by': 'Filter by',
    'filter-by-skill': 'Filter by Skill',
    'filter-by-location': 'Filter by Location',
    'filter-by-availability': 'Filter by Availability',
    'clear-filters': 'Clear Filters',
    'no-results': 'No results found',
    'view-profile': 'View Profile',
    'contact-user': 'Contact User',
    // Notifications
    'notifications': 'Notifications',
    'no-notifications': 'No notifications',
    'mark-all-read': 'Mark all as read',
    'new-request': 'New swap request',
    'request-updated': 'Swap request updated',
    'new-feedback': 'New feedback received',
    // Messages
    'success': 'Success',
    'error': 'Error',
    'warning': 'Warning',
    'info': 'Information',
    'loading': 'Loading...',
    'saving': 'Saving...',
    'deleting': 'Deleting...',
    'please-wait': 'Please wait...',
    'operation-successful': 'Operation completed successfully!',
    'operation-failed': 'Operation failed. Please try again.',
    'confirm-delete': 'Are you sure you want to delete this?',
    'confirm-cancel': 'Are you sure you want to cancel this?',
    'yes': 'Yes',
    'no': 'No',
    'cancel': 'Cancel',
    'confirm': 'Confirm',
    'back': 'Back',
    'next': 'Next',
    'previous': 'Previous',
    'close': 'Close',
    'save': 'Save',
    'delete': 'Delete',
    'edit': 'Edit',
    'update': 'Update',
    'create': 'Create',
    'add': 'Add',
    'remove': 'Remove',
    // Form Validation
    'field-required': 'This field is required',
    'invalid-email': 'Please enter a valid email address',
    'password-too-short': 'Password must be at least 6 characters',
    'passwords-must-match': 'Passwords must match',
    'invalid-format': 'Invalid format',
    // Time and Dates
    'today': 'Today',
    'yesterday': 'Yesterday',
    'this-week': 'This Week',
    'this-month': 'This Month',
    'ago': 'ago',
    'minutes': 'minutes',
    'hours': 'hours',
    'days': 'days',
    'weeks': 'weeks',
    'months': 'months',
    'years': 'years',
    // Admin
    'admin-panel': 'Admin Panel',
    'user-management': 'User Management',
    'ban-user': 'Ban User',
    'unban-user': 'Unban User',
    'delete-user': 'Delete User',
    'make-admin': 'Make Admin',
    'remove-admin': 'Remove Admin',
    'admin-actions': 'Admin Actions',
    'admin-required': 'Admin access required.',
    // Errors
    'page-not-found': 'Page Not Found',
    'page-not-found-message': 'The page you are looking for does not exist.',
    'server-error': 'Server Error',
    'server-error-message': 'Something went wrong on our end. Please try again later.',
    'access-denied': 'Access Denied',
    'access-denied-message': 'You do not have permission to access this page.',
    'login-required': 'Please login to access this page.',
    'profile-private': 'This profile is private.',
    'user-not-available': 'This user is not available.',
    'not-part-of-swap': 'You are not part of this swap.',
    'swap-not-completed': 'You can only leave feedback for completed swaps.',
    'already-left-feedback': 'You have already left feedback for this swap.',
    // Forgot Password
    'forgot-password-title': 'Forgot Password',
    'forgot-password-subtitle': 'Enter your email address and we\'ll send you a link to reset your password',
    'remember-password': 'Remember your password?',
    'back-to-login': 'Back to login',
    'reset-link-sent': 'If an account with that email exists, password reset instructions have been sent.',
    'email-send-error': 'Error sending email. Please try again later.'
    },
    hi: {
    // Navigation and Common
    'skill-swap': 'स्किल स्वैप',
    'tagline': 'कौशल बदलें। एक साथ बढ़ें।',
    'hero-title': 'स्किल स्वैप के साथ जुड़ें, सीखें और बढ़ें',
    'hero-subtitle': 'हमारे सीखने वाले समुदाय में शामिल हों और दूसरों के साथ अपने कौशल साझा करें। नई क्षमताएं सीखें जबकि आप जो सबसे अच्छा जानते हैं उसे सिखाएं।',
    'get-started': 'शुरू करें',
    'learn-more': 'और जानें',
    'login': 'लॉगिन',
    'register': 'रजिस्टर करें',
    'browse-users': 'उपयोगकर्ता ब्राउज़ करें',
    'dashboard': 'डैशबोर्ड',
    'profile': 'प्रोफ़ाइल',
    'logout': 'लॉगआउट',
    'features': 'विशेषताएं',
    'how-it-works': 'यह कैसे काम करता है',
    'testimonials': 'प्रशंसापत्र',
    'footer-text': '© 2025 स्किल स्वैप प्लेटफॉर्म। जुड़ें, सीखें, एक साथ बढ़ें।',
    'name': 'नाम',
    'email': 'ईमेल',
    'password': 'पासवर्ड',
    'location': 'स्थान',
    'availability': 'उपलब्धता',
    'submit': 'सबमिट करें',
    'or': 'या',
    'already-have-account': 'पहले से खाता है?',
    'dont-have-account': 'खाता नहीं है?',
            'sign-up': 'साइन अप करें',
        'sign-in': 'साइन इन करें',
        
        // Additional translations for HTML elements
        'platform': 'प्लेटफॉर्म',
        'home': 'होम',
        'join-now': 'अभी जुड़ें',
        'support': 'सहायता',
        'help-center': 'सहायता केंद्र',
        'community-guidelines': 'समुदाय दिशानिर्देश',
        'safety-tips': 'सुरक्षा युक्तियां',
        'contact-us': 'हमसे संपर्क करें',
        'legal': 'कानूनी',
        'privacy-policy': 'गोपनीयता नीति',
        'terms-of-service': 'सेवा की शर्तें',
        'cookie-policy': 'कुकी नीति',
        'dmca': 'डीएमसीए',
        'company': 'कंपनी',
        'about-us': 'हमारे बारे में',
        'careers': 'करियर',
        'press': 'प्रेस',
        'blog': 'ब्लॉग',
        'secure': 'सुरक्षित',
        'community-driven': 'समुदाय संचालित',
        'global': 'वैश्विक',
        'my-account': 'मेरा खाता',
        'welcome-back': 'वापसी पर स्वागत है! कृपया अपने खाते में साइन इन करें',
        'continue-with-google': 'Google के साथ जारी रखें',
        'forgot-password': 'पासवर्ड भूल गए?',
        'reset-password': 'पासवर्ड रीसेट करें',
        'new-password': 'नया पासवर्ड',
        'confirm-password': 'पासवर्ड की पुष्टि करें',
        'send-reset-link': 'रीसेट लिंक भेजें',
        'back-to-login': 'लॉगिन पर वापस जाएं',
        'remember-password': 'पासवर्ड याद है?',
        'forgot-password-title': 'पासवर्ड भूल गए?',
        'forgot-password-subtitle': 'कोई चिंता नहीं! अपना ईमेल पता दर्ज करें और हम आपको पासवर्ड रीसेट करने का लिंक भेजेंगे।',
        'enter-email-help': 'नीचे अपने स्किल स्वैप खाते से जुड़ा ईमेल पता दर्ज करें।',
        'email-sent': 'ईमेल भेज दिया गया!',
        'reset-link-sent': 'यदि उस ईमेल के साथ कोई खाता मौजूद है, तो हमने पासवर्ड रीसेट निर्देश भेज दिए हैं।',
        'security-tips': 'सुरक्षा युक्तियां',
        'check-spam-folder': 'यदि आपको ईमेल नहीं दिखाई देता तो अपना स्पैम/जंक फोल्डर जांचें',
        'reset-link-expires': 'सुरक्षा के लिए रीसेट लिंक 1 घंटे में समाप्त हो जाएगा',
        'verify-email-address': 'यदि आपको ईमेल नहीं मिलता, तो अपना ईमेल पता सत्यापित करें',
        'contact-support': 'यदि आपको लगातार समस्याएं आ रही हैं तो सहायता से संपर्क करें',
        'create-account': 'एक बनाएं',
        'enter-new-password': 'नीचे अपना नया पासवर्ड दर्ज करें',
    // Authentication
    'welcome-back': 'वापसी पर स्वागत है! कृपया अपने खाते में साइन इन करें',
    'continue-with-google': 'Google के साथ जारी रखें',
    'continue-with-github': 'GitHub के साथ जारी रखें',
    'forgot-password': 'पासवर्ड भूल गए?',
    'reset-password': 'पासवर्ड रीसेट करें',
    'new-password': 'नया पासवर्ड',
    'confirm-password': 'पासवर्ड की पुष्टि करें',
    'send-reset-link': 'रीसेट लिंक भेजें',
    'password-reset-success': 'आपका पासवर्ड सफलतापूर्वक रीसेट हो गया है। अब आप अपने नए पासवर्ड से लॉगिन कर सकते हैं।',
    'password-reset-instructions': 'पासवर्ड रीसेट निर्देश आपके ईमेल पर भेज दिए गए हैं।',
    'invalid-reset-token': 'अमान्य या समाप्त रीसेट टोकन। कृपया नया पासवर्ड रीसेट अनुरोध करें।',
    'passwords-dont-match': 'पासवर्ड मेल नहीं खाते।',
    'password-too-short': 'पासवर्ड कम से कम 6 अक्षर का होना चाहिए।',
    'registration-successful': 'पंजीकरण सफल! स्किल स्वैप में आपका स्वागत है!',
    'invalid-credentials': 'अमान्य ईमेल या पासवर्ड।',
    'account-banned': 'आपका खाता प्रतिबंधित कर दिया गया है। कृपया सहायता से संपर्क करें।',
    'oauth-login-required': 'यह खाता Google के साथ बनाया गया था। लॉगिन के लिए कृपया "Google के साथ जारी रखें" का उपयोग करें।',
    'logged-out': 'आप सफलतापूर्वक लॉगआउट हो गए हैं।',
    // Dashboard
    'welcome': 'स्वागत है',
    'recent-activity': 'हाल की गतिविधि',
    'sent-requests': 'भेजे गए अनुरोध',
    'received-requests': 'प्राप्त अनुरोध',
    'my-skills': 'मेरे कौशल',
    'offered-skills': 'प्रदान किए गए कौशल',
    'wanted-skills': 'वांछित कौशल',
    'recent-feedback': 'हाल का प्रतिक्रिया',
    'no-activity': 'कोई हाल की गतिविधि नहीं',
    'view-all': 'सभी देखें',
    'pending': 'लंबित',
    'accepted': 'स्वीकृत',
    'rejected': 'अस्वीकृत',
    'cancelled': 'रद्द',
    'completed': 'पूर्ण',
    // Profile
    'edit-profile': 'प्रोफ़ाइल संपादित करें',
    'profile-updated': 'प्रोफ़ाइल सफलतापूर्वक अपडेट हो गया!',
    'public-profile': 'सार्वजनिक प्रोफ़ाइल',
    'private-profile': 'निजी प्रोफ़ाइल',
    'profile-privacy': 'प्रोफ़ाइल गोपनीयता',
    'make-public': 'सार्वजनिक बनाएं',
    'make-private': 'निजी बनाएं',
    'upload-photo': 'फोटो अपलोड करें',
    'change-photo': 'फोटो बदलें',
    'remove-photo': 'फोटो हटाएं',
    'about-me': 'मेरे बारे में',
    'contact-info': 'संपर्क जानकारी',
    'account-settings': 'खाता सेटिंग्स',
    // Skills
    'manage-skills': 'कौशल प्रबंधित करें',
    'add-skill': 'कौशल जोड़ें',
    'remove-skill': 'कौशल हटाएं',
    'skill-name': 'कौशल का नाम',
    'skill-type': 'कौशल का प्रकार',
    'offered': 'प्रदान किया गया',
    'wanted': 'वांछित',
    'skill-added': 'कौशल सफलतापूर्वक जोड़ा गया!',
    'skill-removed': 'कौशल सफलतापूर्वक हटा दिया गया!',
    'no-skills': 'अभी तक कोई कौशल नहीं जोड़ा गया',
    'search-skills': 'कौशल खोजें...',
    // Swap Requests
    'swap-request': 'स्वैप अनुरोध',
    'request-swap': 'स्वैप अनुरोध करें',
    'swap-requests': 'स्वैप अनुरोध',
    'swap-list': 'स्वैप सूची',
    'create-swap': 'स्वैप बनाएं',
    'accept-swap': 'स्वैप स्वीकार करें',
    'reject-swap': 'स्वैप अस्वीकार करें',
    'cancel-swap': 'स्वैप रद्द करें',
    'complete-swap': 'स्वैप पूर्ण करें',
    'swap-details': 'स्वैप विवरण',
    'swap-created': 'स्वैप अनुरोध सफलतापूर्वक बनाया गया!',
    'swap-accepted': 'स्वैप अनुरोध स्वीकार किया गया!',
    'swap-rejected': 'स्वैप अनुरोध अस्वीकार किया गया।',
    'swap-cancelled': 'स्वैप अनुरोध रद्द किया गया।',
    'swap-completed': 'स्वैप सफलतापूर्वक पूर्ण हुआ!',
    'no-swaps': 'कोई स्वैप अनुरोध नहीं मिला',
    // Feedback
    'feedback': 'प्रतिक्रिया',
    'leave-feedback': 'प्रतिक्रिया दें',
    'submit-feedback': 'प्रतिक्रिया सबमिट करें',
    'feedback-submitted': 'आपकी प्रतिक्रिया के लिए धन्यवाद!',
    'rating': 'रेटिंग',
    'comment': 'टिप्पणी',
    'overall-rating': 'कुल रेटिंग',
    'no-feedback': 'अभी तक कोई प्रतिक्रिया नहीं',
    'feedback-already-given': 'आपने पहले ही इस स्वैप के लिए प्रतिक्रिया दे दी है।',
    // Browse and Search
    'browse': 'ब्राउज़ करें',
    'search': 'खोजें',
    'search-users': 'उपयोगकर्ता खोजें',
    'search-results': 'खोज परिणाम',
    'filter-by': 'फ़िल्टर करें',
    'filter-by-skill': 'कौशल द्वारा फ़िल्टर करें',
    'filter-by-location': 'स्थान द्वारा फ़िल्टर करें',
    'filter-by-availability': 'उपलब्धता द्वारा फ़िल्टर करें',
    'clear-filters': 'फ़िल्टर साफ़ करें',
    'no-results': 'कोई परिणाम नहीं मिला',
    'view-profile': 'प्रोफ़ाइल देखें',
    'contact-user': 'उपयोगकर्ता से संपर्क करें',
    // Notifications
    'notifications': 'सूचनाएं',
    'no-notifications': 'कोई सूचना नहीं',
    'mark-all-read': 'सभी को पढ़ा हुआ चिह्नित करें',
    'new-request': 'नया स्वैप अनुरोध',
    'request-updated': 'स्वैप अनुरोध अपडेट किया गया',
    'new-feedback': 'नई प्रतिक्रिया प्राप्त हुई',
    // Messages
    'success': 'सफलता',
    'error': 'त्रुटि',
    'warning': 'चेतावनी',
    'info': 'जानकारी',
    'loading': 'लोड हो रहा है...',
    'saving': 'सहेज रहा है...',
    'deleting': 'हटा रहा है...',
    'please-wait': 'कृपया प्रतीक्षा करें...',
    'operation-successful': 'कार्य सफलतापूर्वक पूर्ण हुआ!',
    'operation-failed': 'कार्य विफल हुआ। कृपया पुनः प्रयास करें।',
    'confirm-delete': 'क्या आप वाकई इसे हटाना चाहते हैं?',
    'confirm-cancel': 'क्या आप वाकई इसे रद्द करना चाहते हैं?',
    'yes': 'हाँ',
    'no': 'नहीं',
    'cancel': 'रद्द करें',
    'confirm': 'पुष्टि करें',
    'back': 'वापस',
    'next': 'अगला',
    'previous': 'पिछला',
    'close': 'बंद करें',
    'save': 'सहेजें',
    'delete': 'हटाएं',
    'edit': 'संपादित करें',
    'update': 'अपडेट करें',
    'create': 'बनाएं',
    'add': 'जोड़ें',
    'remove': 'हटाएं',
    // Form Validation
    'field-required': 'यह फ़ील्ड आवश्यक है',
    'invalid-email': 'कृपया एक मान्य ईमेल पता दर्ज करें',
    'password-too-short': 'पासवर्ड कम से कम 6 अक्षर का होना चाहिए',
    'passwords-must-match': 'पासवर्ड मेल खाने चाहिए',
    'invalid-format': 'अमान्य प्रारूप',
    // Time and Dates
    'today': 'आज',
    'yesterday': 'कल',
    'this-week': 'इस सप्ताह',
    'this-month': 'इस महीने',
    'ago': 'पहले',
    'minutes': 'मिनट',
    'hours': 'घंटे',
    'days': 'दिन',
    'weeks': 'सप्ताह',
    'months': 'महीने',
    'years': 'वर्ष',
    // Admin
    'admin-panel': 'एडमिन पैनल',
    'user-management': 'उपयोगकर्ता प्रबंधन',
    'ban-user': 'उपयोगकर्ता प्रतिबंधित करें',
    'unban-user': 'उपयोगकर्ता प्रतिबंध हटाएं',
    'delete-user': 'उपयोगकर्ता हटाएं',
    'make-admin': 'एडमिन बनाएं',
    'remove-admin': 'एडमिन हटाएं',
    'admin-actions': 'एडमिन कार्य',
    'admin-required': 'एडमिन पहुंच आवश्यक है।',
    // Errors
    'page-not-found': 'पृष्ठ नहीं मिला',
    'page-not-found-message': 'आप जिस पृष्ठ की खोज कर रहे हैं वह मौजूद नहीं है।',
    'server-error': 'सर्वर त्रुटि',
    'server-error-message': 'हमारी तरफ से कुछ गलत हो गया। कृपया बाद में पुनः प्रयास करें।',
    'access-denied': 'पहुंच अस्वीकृत',
    'access-denied-message': 'आपको इस पृष्ठ तक पहुंचने की अनुमति नहीं है।',
    'login-required': 'कृपया इस पृष्ठ तक पहुंचने के लिए लॉगिन करें।',
    'profile-private': 'यह प्रोफ़ाइल निजी है।',
    'user-not-available': 'यह उपयोगकर्ता उपलब्ध नहीं है।',
    'not-part-of-swap': 'आप इस स्वैप का हिस्सा नहीं हैं।',
    'swap-not-completed': 'आप केवल पूर्ण स्वैप के लिए प्रतिक्रिया दे सकते हैं।',
    'already-left-feedback': 'आपने पहले ही इस स्वैप के लिए प्रतिक्रिया दे दी है।',
    // Forgot Password
    'forgot-password-title': 'पासवर्ड भूल गए',
    'forgot-password-subtitle': 'अपना ईमेल पता दर्ज करें और हम आपको पासवर्ड रीसेट करने का लिंक भेजेंगे',
    'remember-password': 'पासवर्ड याद है?',
    'back-to-login': 'लॉगिन पर वापस जाएं',
    'reset-link-sent': 'यदि उस ईमेल के साथ कोई खाता मौजूद है, तो पासवर्ड रीसेट निर्देश भेज दिए गए हैं।',
    'email-send-error': 'ईमेल भेजने में त्रुटि। कृपया बाद में पुनः प्रयास करें।'
    },
    gu: {
    // Navigation and Common
    'skill-swap': 'સ્કિલ સ્વેપ',
    'tagline': 'કૌશલ્ય બદલો. સાથે વૃદ્ધિ કરો.',
    'hero-title': 'સ્કિલ સ્વેપ સાથે જોડાઓ, શીખો અને વધો',
    'hero-subtitle': 'અમારા શીખનારાઓના સમુદાયમાં જોડાઓ અને અન્ય લોકો સાથે તમારા કૌશલ્ય શેર કરો. નવી ક્ષમતાઓ શીખો જ્યારે તમે જે શ્રેષ્ઠ જાણો છો તે શીખવો.',
    'get-started': 'શરૂ કરો',
    'learn-more': 'વધુ જાણો',
    'login': 'લોગિન',
    'register': 'નોંધણી કરો',
    'browse-users': 'યુઝર્સ બ્રાઉઝ કરો',
    'dashboard': 'ડેશબોર્ડ',
    'profile': 'પ્રોફાઇલ',
    'logout': 'લોગઆઉટ',
    'features': 'લક્ષણો',
    'how-it-works': 'તે કેવી રીતે કામ કરે છે',
    'testimonials': 'પ્રશંસાપત્રો',
    'footer-text': '© 2025 સ્કિલ સ્વેપ પ્લેટફોર્મ. જોડાઓ, શીખો, સાથે વૃદ્ધિ કરો.',
    'name': 'નામ',
    'email': 'ઇમેઇલ',
    'password': 'પાસવર્ડ',
    'location': 'સ્થાન',
    'availability': 'ઉપલબ્ધતા',
    'submit': 'સબમિટ કરો',
    'or': 'અથવા',
    'already-have-account': 'પહેલેથી ખાતું છે?',
    'dont-have-account': 'ખાતું નથી?',
            'sign-up': 'સાઇન અપ',
        'sign-in': 'સાઇન ઇન',
        
        // Additional translations for HTML elements
        'platform': 'પ્લેટફોર્મ',
        'home': 'હોમ',
        'join-now': 'હવે જોડાઓ',
        'support': 'સહાય',
        'help-center': 'સહાય કેન્દ્ર',
        'community-guidelines': 'સમુદાય માર્ગદર્શિકા',
        'safety-tips': 'સલામતી ટિપ્સ',
        'contact-us': 'અમારો સંપર્ક કરો',
        'legal': 'કાનૂની',
        'privacy-policy': 'ગોપનીયતા નીતિ',
        'terms-of-service': 'સેવાની શરતો',
        'cookie-policy': 'કુકી નીતિ',
        'dmca': 'ડીએમસીએ',
        'company': 'કંપની',
        'about-us': 'અમારા વિશે',
        'careers': 'કારકિર્દી',
        'press': 'પ્રેસ',
        'blog': 'બ્લોગ',
        'secure': 'સુરક્ષિત',
        'community-driven': 'સમુદાય સંચાલિત',
        'global': 'વૈશ્વિક',
        'my-account': 'મારું ખાતું',
        'welcome-back': 'પાછા આવવા માટે સ્વાગત છે! કૃપા કરીને તમારા ખાતામાં સાઇન ઇન કરો',
        'continue-with-google': 'Google સાથે ચાલુ રાખો',
        'forgot-password': 'પાસવર્ડ ભૂલી ગયા?',
        'reset-password': 'પાસવર્ડ રીસેટ કરો',
        'new-password': 'નવો પાસવર્ડ',
        'confirm-password': 'પાસવર્ડની પુષ્ટિ કરો',
        'send-reset-link': 'રીસેટ લિંક મોકલો',
        'back-to-login': 'લોગિન પર પાછા જાઓ',
        'remember-password': 'પાસવર્ડ યાદ છે?',
        'forgot-password-title': 'પાસવર્ડ ભૂલી ગયા?',
        'forgot-password-subtitle': 'કોઈ ચિંતા નહીં! તમારો ઇમેઇલ સરનામું દાખલ કરો અને અમે તમને પાસવર્ડ રીસેટ કરવાની લિંક મોકલીશું.',
        'enter-email-help': 'નીચે તમારા સ્કિલ સ્વેપ ખાતા સાથે સંકળાયેલો ઇમેઇલ સરનામું દાખલ કરો.',
        'email-sent': 'ઇમેઇલ મોકલ્યો!',
        'reset-link-sent': 'જો તે ઇમેઇલ સાથે કોઈ ખાતું અસ્તિત્વમાં છે, તો અમે પાસવર્ડ રીસેટ સૂચનાઓ મોકલી છે.',
        'security-tips': 'સલામતી ટિપ્સ',
        'check-spam-folder': 'જો તમને ઇમેઇલ દેખાતો નથી તો તમારો સ્પામ/જંક ફોલ્ડર તપાસો',
        'reset-link-expires': 'સલામતી માટે રીસેટ લિંક 1 કલાકમાં સમાપ્ત થશે',
        'verify-email-address': 'જો તમને ઇમેઇલ મળતો નથી, તો તમારો ઇમેઇલ સરનામો ચકાસો',
        'contact-support': 'જો તમને સતત સમસ્યાઓ આવતી રહે છે તો સહાય સાથે સંપર્ક કરો',
        'create-account': 'એક બનાવો',
        'enter-new-password': 'નીચે તમારો નવો પાસવર્ડ દાખલ કરો',
    // Authentication
    'welcome-back': 'પાછા આવવા માટે સ્વાગત છે! કૃપા કરીને તમારા ખાતામાં સાઇન ઇન કરો',
    'continue-with-google': 'Google સાથે ચાલુ રાખો',
    'continue-with-github': 'GitHub સાથે ચાલુ રાખો',
    'forgot-password': 'પાસવર્ડ ભૂલી ગયા?',
    'reset-password': 'પાસવર્ડ રીસેટ કરો',
    'new-password': 'નવો પાસવર્ડ',
    'confirm-password': 'પાસવર્ડની પુષ્ટિ કરો',
    'send-reset-link': 'રીસેટ લિંક મોકલો',
    'password-reset-success': 'તમારો પાસવર્ડ સફળતાપૂર્વક રીસેટ થયો છે. હવે તમે તમારા નવા પાસવર્ડથી લોગિન કરી શકો છો.',
    'password-reset-instructions': 'પાસવર્ડ રીસેટ સૂચનાઓ તમારા ઇમેઇલ પર મોકલી દેવામાં આવી છે.',
    'invalid-reset-token': 'અમાન્ય અથવા સમાપ્ત રીસેટ ટોકન. કૃપા કરીને નવો પાસવર્ડ રીસેટ વિનંતી કરો.',
    'passwords-dont-match': 'પાસવર્ડ મેળ ખાતા નથી.',
    'password-too-short': 'પાસવર્ડ ઓછામાં ઓછા 6 અક્ષરોનો હોવો જોઈએ.',
    'registration-successful': 'નોંધણી સફળ! સ્કિલ સ્વેપમાં તમારું સ્વાગત છે!',
    'invalid-credentials': 'અમાન્ય ઇમેઇલ અથવા પાસવર્ડ.',
    'account-banned': 'તમારું ખાતું પ્રતિબંધિત કરવામાં આવ્યું છે. કૃપા કરીને સહાય સાથે સંપર્ક કરો.',
    'oauth-login-required': 'આ ખાતું Google સાથે બનાવવામાં આવ્યું હતું. લોગિન માટે કૃપા કરીને "Google સાથે ચાલુ રાખો" નો ઉપયોગ કરો.',
    'logged-out': 'તમે સફળતાપૂર્વક લોગઆઉટ થયા છો.',
    // Dashboard
    'welcome': 'સ્વાગત છે',
    'recent-activity': 'તાજી પ્રવૃત્તિ',
    'sent-requests': 'મોકલેલી વિનંતીઓ',
    'received-requests': 'પ્રાપ્ત વિનંતીઓ',
    'my-skills': 'મારા કૌશલ્યો',
    'offered-skills': 'ઓફર કરેલા કૌશલ્યો',
    'wanted-skills': 'ઇચ્છિત કૌશલ્યો',
    'recent-feedback': 'તાજી પ્રતિભાવ',
    'no-activity': 'કોઈ તાજી પ્રવૃત્તિ નથી',
    'view-all': 'બધું જુઓ',
    'pending': 'પેન્ડિંગ',
    'accepted': 'સ્વીકૃત',
    'rejected': 'અસ્વીકૃત',
    'cancelled': 'રદ',
    'completed': 'પૂર્ણ',
    // Profile
    'edit-profile': 'પ્રોફાઇલ એડિટ કરો',
    'profile-updated': 'પ્રોફાઇલ સફળતાપૂર્વક અપડેટ થયું!',
    'public-profile': 'જાહેર પ્રોફાઇલ',
    'private-profile': 'ખાનગી પ્રોફાઇલ',
    'profile-privacy': 'પ્રોફાઇલ ગોપનીયતા',
    'make-public': 'જાહેર બનાવો',
    'make-private': 'ખાનગી બનાવો',
    'upload-photo': 'ફોટો અપલોડ કરો',
    'change-photo': 'ફોટો બદલો',
    'remove-photo': 'ફોટો દૂર કરો',
    'about-me': 'મારા વિશે',
    'contact-info': 'સંપર્ક માહિતી',
    'account-settings': 'ખાતા સેટિંગ્સ',
    // Skills
    'manage-skills': 'કૌશલ્યો મેનેજ કરો',
    'add-skill': 'કૌશલ્ય ઉમેરો',
    'remove-skill': 'કૌશલ્ય દૂર કરો',
    'skill-name': 'કૌશલ્યનું નામ',
    'skill-type': 'કૌશલ્યનો પ્રકાર',
    'offered': 'ઓફર કરેલું',
    'wanted': 'ઇચ્છિત',
    'skill-added': 'કૌશલ્ય સફળતાપૂર્વક ઉમેરાયું!',
    'skill-removed': 'કૌશલ્ય સફળતાપૂર્વક દૂર કરાયું!',
    'no-skills': 'હજુ કોઈ કૌશલ્ય ઉમેરાયું નથી',
    'search-skills': 'કૌશલ્યો શોધો...',
    // Swap Requests
    'swap-request': 'સ્વેપ વિનંતી',
    'request-swap': 'સ્વેપ વિનંતી કરો',
    'swap-requests': 'સ્વેપ વિનંતીઓ',
    'swap-list': 'સ્વેપ યાદી',
    'create-swap': 'સ્વેપ બનાવો',
    'accept-swap': 'સ્વેપ સ્વીકારો',
    'reject-swap': 'સ્વેપ અસ્વીકારો',
    'cancel-swap': 'સ્વેપ રદ કરો',
    'complete-swap': 'સ્વેપ પૂર્ણ કરો',
    'swap-details': 'સ્વેપ વિગતો',
    'swap-created': 'સ્વેપ વિનંતી સફળતાપૂર્વક બનાવી!',
    'swap-accepted': 'સ્વેપ વિનંતી સ્વીકારી!',
    'swap-rejected': 'સ્વેપ વિનંતી અસ્વીકારી.',
    'swap-cancelled': 'સ્વેપ વિનંતી રદ કરી.',
    'swap-completed': 'સ્વેપ સફળતાપૂર્વક પૂર્ણ થયું!',
    'no-swaps': 'કોઈ સ્વેપ વિનંતી મળી નથી',
    // Feedback
    'feedback': 'પ્રતિભાવ',
    'leave-feedback': 'પ્રતિભાવ આપો',
    'submit-feedback': 'પ્રતિભાવ સબમિટ કરો',
    'feedback-submitted': 'તમારા પ્રતિભાવ માટે આભાર!',
    'rating': 'રેટિંગ',
    'comment': 'ટિપ્પણી',
    'overall-rating': 'કુલ રેટિંગ',
    'no-feedback': 'હજુ કોઈ પ્રતિભાવ નથી',
    'feedback-already-given': 'તમે પહેલેથી જ આ સ્વેપ માટે પ્રતિભાવ આપી દીધું છે.',
    // Browse and Search
    'browse': 'બ્રાઉઝ કરો',
    'search': 'શોધો',
    'search-users': 'યુઝર્સ શોધો',
    'search-results': 'શોધ પરિણામો',
    'filter-by': 'ફિલ્ટર કરો',
    'filter-by-skill': 'કૌશલ્ય દ્વારા ફિલ્ટર કરો',
    'filter-by-location': 'સ્થાન દ્વારા ફિલ્ટર કરો',
    'filter-by-availability': 'ઉપલબ્ધતા દ્વારા ફિલ્ટર કરો',
    'clear-filters': 'ફિલ્ટર સાફ કરો',
    'no-results': 'કોઈ પરિણામ મળ્યું નથી',
    'view-profile': 'પ્રોફાઇલ જુઓ',
    'contact-user': 'યુઝર સાથે સંપર્ક કરો',
    // Notifications
    'notifications': 'સૂચનાઓ',
    'no-notifications': 'કોઈ સૂચના નથી',
    'mark-all-read': 'બધી વાંચી લીધી તરીકે ચિહ્નિત કરો',
    'new-request': 'નવી સ્વેપ વિનંતી',
    'request-updated': 'સ્વેપ વિનંતી અપડેટ કરી',
    'new-feedback': 'નવો પ્રતિભાવ મળ્યો',
    // Messages
    'success': 'સફળતા',
    'error': 'ભૂલ',
    'warning': 'ચેતવણી',
    'info': 'માહિતી',
    'loading': 'લોડ થઈ રહ્યું છે...',
    'saving': 'સેવ કરી રહ્યું છે...',
    'deleting': 'કાઢી રહ્યું છે...',
    'please-wait': 'કૃપા કરીને રાહ જુઓ...',
    'operation-successful': 'કામ સફળતાપૂર્વક પૂર્ણ થયું!',
    'operation-failed': 'કામ નિષ્ફળ થયું. કૃપા કરીને ફરીથી પ્રયાસ કરો.',
    'confirm-delete': 'શું તમે ખરેખર આ કાઢી નાખવા માંગો છો?',
    'confirm-cancel': 'શું તમે ખરેખર આ રદ કરવા માંગો છો?',
    'yes': 'હા',
    'no': 'ના',
    'cancel': 'રદ કરો',
    'confirm': 'પુષ્ટિ કરો',
    'back': 'પાછળ',
    'next': 'આગળ',
    'previous': 'પહેલું',
    'close': 'બંધ કરો',
    'save': 'સેવ કરો',
    'delete': 'કાઢી નાખો',
    'edit': 'એડિટ કરો',
    'update': 'અપડેટ કરો',
    'create': 'બનાવો',
    'add': 'ઉમેરો',
    'remove': 'દૂર કરો',
    // Form Validation
    'field-required': 'આ ફીલ્ડ જરૂરી છે',
    'invalid-email': 'કૃપા કરી'
    }
};

// Current language
let currentLang = localStorage.getItem('skillswap-language') || 'en';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeLanguage();
    initializeScrollAnimations();
    initializeFormValidation();
    initializeNavbar();
    initializeParticles();
});

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('skillswap-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        updateThemeIcon();
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('skillswap-theme', newTheme);
    updateThemeIcon();
    
    // Add smooth transition effect
    document.body.style.transition = 'all 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}

function updateThemeIcon() {
    const themeToggle = document.querySelector('.theme-toggle i');
    const currentTheme = document.documentElement.getAttribute('data-theme');
    
    if (themeToggle) {
        themeToggle.className = currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Language Management
function initializeLanguage() {
    const languageOptions = document.querySelectorAll('.language-option');
    if (languageOptions.length > 0) {
        languageOptions.forEach(option => {
            if (option.getAttribute('data-lang') === currentLang) {
                option.classList.add('active');
            }
            option.addEventListener('click', function(e) {
                e.preventDefault();
                changeLanguage(this.getAttribute('data-lang'));
            });
        });
    }
    
    updateLanguage();
}

function changeLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('skillswap-language', currentLang);
    
    // Update active class
    document.querySelectorAll('.language-option').forEach(option => {
        if (option.getAttribute('data-lang') === currentLang) {
            option.classList.add('active');
        } else {
            option.classList.remove('active');
        }
    });
    
    updateLanguage();
}

function updateLanguage() {
    const elementsToTranslate = document.querySelectorAll('[data-translate]');
    
    elementsToTranslate.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[currentLang] && translations[currentLang][key]) {
            if (element.tagName === 'INPUT' && element.type === 'submit') {
                element.value = translations[currentLang][key];
            } else if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                element.placeholder = translations[currentLang][key];
            } else {
                element.textContent = translations[currentLang][key];
            }
        }
    });
    
    // Update document title
    if (translations[currentLang]['skill-swap']) {
        document.title = translations[currentLang]['skill-swap'];
    }
}

// Scroll Animations
function initializeScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    showFieldError(input, 'This field is required');
                } else {
                    input.classList.remove('error');
                    hideFieldError(input);
                }
                
                // Email validation
                if (input.type === 'email' && input.value.trim()) {
                    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailPattern.test(input.value)) {
                        isValid = false;
                        input.classList.add('error');
                        showFieldError(input, 'Please enter a valid email address');
                    }
                }
                
                // Password validation
                if (input.type === 'password' && input.value.trim()) {
                    if (input.value.length < 6) {
                        isValid = false;
                        input.classList.add('error');
                        showFieldError(input, 'Password must be at least 6 characters');
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                if (input.classList.contains('error')) {
                    validateField(input);
                }
            });
        });
    });
}

function validateField(input) {
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Email validation
    if (input.type === 'email' && value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }
    
    // Password validation
    if (input.type === 'password' && value) {
        if (value.length < 6) {
            isValid = false;
            errorMessage = 'Password must be at least 6 characters';
        }
    }
    
    if (isValid) {
        input.classList.remove('error');
        hideFieldError(input);
    } else {
        input.classList.add('error');
        showFieldError(input, errorMessage);
    }
}

function showFieldError(input, message) {
    hideFieldError(input); // Remove existing error
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.cssText = `
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.25rem;
        opacity: 0;
        transform: translateY(-10px);
        transition: all 0.3s ease;
    `;
    
    input.parentNode.appendChild(errorElement);
    
    // Animate in
    setTimeout(() => {
        errorElement.style.opacity = '1';
        errorElement.style.transform = 'translateY(0)';
    }, 10);
}

function hideFieldError(input) {
    const existingError = input.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// Navbar Management
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Particle Animation (for hero section)
function initializeParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
        z-index: 1;
    `;
    
    hero.appendChild(particlesContainer);
    
    // Create particles
    for (let i = 0; i < 50; i++) {
        createParticle(particlesContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    const size = Math.random() * 4 + 2;
    const startX = Math.random() * window.innerWidth;
    const duration = Math.random() * 20 + 10;
    
    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: radial-gradient(circle, var(--primary-color), transparent);
        border-radius: 50%;
        left: ${startX}px;
        top: 100%;
        opacity: 0.6;
        animation: floatUp ${duration}s linear infinite;
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
        // Create new particle
        createParticle(container);
    }, duration * 1000);
}

// Add CSS for particle animation
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    .form-control.error {
        border-color: #ef4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }
`;
document.head.appendChild(style);

// Enhanced dropdowns
document.addEventListener('DOMContentLoaded', function() {
    // Add animation and styling to dropdowns
    const dropdowns = document.querySelectorAll('.dropdown-menu');
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('show.bs.dropdown', function() {
            this.classList.add('animate__animated', 'animate__fadeIn');
            this.style.animationDuration = '0.3s';
        });
    });
    
    // Make select elements more interactive
    const selects = document.querySelectorAll('select.form-control, .filter-select');
    
    selects.forEach(select => {
        select.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        select.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Add a subtle animation when changing options
        select.addEventListener('change', function() {
            this.classList.add('pulse');
            setTimeout(() => {
                this.classList.remove('pulse');
            }, 500);
        });
    });
});

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        opacity: 0;
        transform: translateX(100px);
        transition: all 0.3s ease;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function addLoadingState(button) {
    const originalText = button.textContent;
    button.innerHTML = '<span class="loading"></span> Loading...';
    button.disabled = true;
    
    return function removeLoadingState() {
        button.textContent = originalText;
        button.disabled = false;
    };
}

// Export functions for use in other scripts
window.SkillSwap = {
    showNotification,
    addLoadingState,
    updateLanguage,
    toggleTheme
};