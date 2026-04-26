# CUET Campus Medical Center

A comprehensive medical management system for the CUET (Chittagong University of Engineering & Technology) campus community.

## **Project Team**

- **Pulak Bhowmik** - ID: 2204092
- **Ananta Debnath** - ID: 2204093
- **Mahfuzur Rahman** - ID: 2204097

---

## **Project Overview**

CUET Campus Medical Center is a modern, full-stack web application designed to streamline healthcare services and communication at the CUET campus. It provides an integrated platform for students, doctors, and administrative staff to manage health records, appointments, pharmacy services, blood bank operations, and emergency notifications.

---

## **Key Features**

### **👤 User Authentication & Management**
- **Multi-role Authentication System**: Separate login/signup flows for Students, Doctors, and Admins
- **OTP-based Email Verification**: Secure registration with one-time passwords
- **JWT Token Authentication**: Secure API authentication with refresh tokens
- **User Profile Management**: Complete profile editing with role-specific fields
- **Account Deletion**: Users can permanently delete their accounts with database synchronization
- **Password Management**: Secure password handling with plaintext storage for demo purposes

### **📋 Medical Records**
- **Electronic Medical Records (EMR)**: Students can maintain their medical history
- **Doctor Access Control**: Only authorized doctors can view/update patient records
- **Appointment Tracking**: Record of medical consultations and visits
- **Secure Data Storage**: Encrypted and role-based access to sensitive health information

### **🩺 Doctor Portal**
- **Doctor Dashboard**: Centralized view of all patients and appointments
- **Patient Management**: View and manage student medical records
- **Appointment Scheduling**: Schedule and manage patient consultations
- **Roster Management**: Doctor availability and shift scheduling
- **Patient History**: Complete medical history and visit records

### **🏥 Hospital Management**
- **Bed Availability Tracking**: Real-time bed status and occupancy management
- **Emergency Response**: Fast-track emergency alert system
- **Resource Management**: Track available resources and equipment
- **System Status Monitoring**: Hospital alerts and notifications

### **💉 Pharmacy Management**
- **Prescription Processing**: Digital prescription management
- **Medicine Inventory**: Track medicine availability and stock
- **Patient Prescriptions**: Students can view their active prescriptions
- **Pharmacy Dashboard**: Admin view of all medications and inventory

### **🩸 Blood Bank Services**
- **Blood Donor Registry**: Database of blood donors with blood group information
- **Blood Stock Management**: Track blood availability by type
- **Donation History**: Record of blood donations and recipients
- **Emergency Blood Request**: Fast request system for urgent blood needs

### **📢 Notices & Announcements**
- **Notice Publishing**: Admins and doctors can publish important notices
- **PDF Upload & Download**: Attach PDF files to notices for easy distribution
- **Public Access**: All users can view and download published notices
- **Role-Based Publishing**: Only authorized personnel can create notices

### **🔔 Alerts & Notifications**
- **System Alerts**: Real-time alerts for important medical center updates
- **Emergency Notifications**: Instant alerts for medical emergencies
- **User Notifications**: Personal notifications for appointments and updates
- **Alert Management**: Dashboard to manage and view all notifications

### **🤖 AI Health Assistant**
- **Groq AI Integration**: AI-powered health assistant for medical queries
- **Natural Language Processing**: Ask health-related questions in plain English
- **Medical Information**: Get reliable health information and guidance
- **24/7 Availability**: Always available assistant for quick health questions

### **🎯 Additional Features**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Theme UI**: Modern dark-themed interface for better UX
- **Role-Based Access Control**: Different features and views for each user role
- **Real-time Data Sync**: Instant updates across all components
- **Admin Dashboard**: Comprehensive admin panel for system management
- **Search & Filter**: Quick search and filtering across all modules

---

## **Technology Stack**

### **Backend**
- **Django 5.2.13** - Python web framework
- **Django REST Framework** - REST API development
- **SQLite** - Database
- **JWT Authentication** - Secure token-based auth
- **Groq API** - AI health assistant integration

### **Frontend**
- **Vanilla JavaScript** - No framework dependencies
- **HTML5 & CSS3** - Modern markup and styling
- **LocalStorage** - Client-side token management
- **Responsive Design** - Mobile-first approach

### **Development Tools**
- **Git** - Version control
- **Virtual Environment** - Python dependency isolation
- **Django ORM** - Database management

---

## **Installation & Setup**

### **Prerequisites**
- Python 3.8+
- pip (Python package manager)
- Git
- Virtual Environment

### **Steps**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mahfuz-byte/CUET-Medical-Center.git
   cd CUET-Medical-Center
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Open browser and go to `http://127.0.0.1:8000`
   - Default login page: `http://127.0.0.1:8000/login.html`

---

## **Project Structure**

```
CUET-Medical-Center/
├── accounts/              # User authentication and profiles
├── bloodbank/            # Blood bank management
├── notifications/        # Notices and alerts system
├── records/             # Medical records management
├── roster/              # Doctor roster/scheduling
├── cuet_medical/        # Main Django project settings
├── frontend-temp/       # Frontend HTML/CSS/JS files
│   ├── student/         # Student-specific pages
│   └── assets/          # CSS, JS, images
├── media/               # User uploads (notices, files)
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── README.md           # This file
```

---

## **API Endpoints**

### **Authentication**
- `POST /api/auth/send-otp/` - Send OTP to email
- `POST /api/auth/verify-otp/` - Verify OTP code
- `POST /api/auth/signup/` - Register new user
- `POST /api/auth/login/` - Login user
- `GET /api/auth/me/` - Get current user profile
- `DELETE /api/auth/me/` - Delete user account

### **Notices**
- `GET /api/notifications/notices/` - List all notices
- `POST /api/notifications/notices/` - Create new notice (admin/doctor only)
- `DELETE /api/notifications/notices/{id}/` - Delete notice

### **Medical Records**
- `GET /api/records/` - View medical records
- `POST /api/records/` - Create medical record

### **AI Assistant**
- `POST /api/assistant/ask/` - Ask health questions to AI

### **Roster & Blood Bank**
- `GET /api/roster/` - Doctor roster information
- `GET /api/notifications/blood/` - Blood donor information

---

## **Usage Examples**

### **Student User**
1. Sign up with CUET student email (u[StudentID]@student.cuet.ac.bd)
2. View medical records and appointments
3. Check prescriptions from pharmacy
4. Download notices and announcements
5. Ask health questions to AI assistant

### **Doctor User**
1. Sign up as a doctor
2. View and manage patient records
3. Create medical prescriptions
4. Publish important notices
5. Manage doctor schedule/roster

### **Admin User**
1. Sign up as administrator
2. Manage all users and accounts
3. Monitor system resources (beds, blood, etc.)
4. Publish notices and alerts
5. Access comprehensive admin dashboard

---

## **Features Implemented**

✅ Multi-role user authentication  
✅ Electronic medical records system  
✅ Doctor portal with patient management  
✅ Pharmacy and prescription management  
✅ Blood bank services and donor registry  
✅ Notice publishing system with PDF uploads  
✅ Alerts and notifications  
✅ AI health assistant (Groq API)  
✅ Responsive dark-themed UI  
✅ Role-based access control  
✅ User profile management  
✅ Account deletion with database sync  
✅ Real-time bed availability tracking  
✅ Emergency response system  

---

## **Known Limitations**

- Development server only (not production-ready)
- SQLite database (single-user concurrent access)
- Email sending requires SMTP configuration
- AI assistant rate limits depend on Groq API plan

---

## **Future Enhancements**

- Video consultation between doctors and patients
- SMS notifications for emergencies
- Mobile app (iOS/Android)
- Advanced analytics and reporting
- Integration with hospital management systems
- Appointment booking system
- Payment gateway integration
- Prescription fulfillment tracking

---

## **Security Note**

This is a demonstration project for educational purposes. For production use:
- Use a production-grade database (PostgreSQL)
- Implement HTTPS/SSL
- Use a professional email service
- Add rate limiting and DDoS protection
- Implement comprehensive logging
- Use environment variables for sensitive data
- Deploy on a production server

---

## **Contributing**

This is a university project by the team members listed above. For questions or suggestions, please contact:
- Email: medical@cuet.edu
- Phone: +880-31-714946

---

## **License**

© 2026 CUET Campus Medical Center. All rights reserved.

---

## **Contact & Support**

**CUET Campus Medical Center**  
Pahartoli, Raozan, Chattogram - 4349, Bangladesh  
Phone: +880-31-714946  
Email: medical@cuet.edu

---

**Last Updated:** April 19, 2026  
**Version:** 1.0.0
