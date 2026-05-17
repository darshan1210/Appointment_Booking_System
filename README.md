**PROJECT DOCUMENTATION**

**Multi-Tenant Appointment Booking Platform**

Enterprise SaaS Solution with Super Admin, Firm & User Management

| **Version** | 1.1.0                             |
| ----------- | --------------------------------- |
| **Date**    | May 2026                          |
| **Status**  | Planning & Design Phase           |
| **Type**    | Multi-Tenant SaaS Web Application |

# **1\. Project Overview**

## **1.1 Introduction**

This document provides comprehensive technical and functional documentation for the Multi-Tenant Appointment Booking Platform, a SaaS (Software as a Service) web application that enables businesses (firms) to manage their internal user scheduling, appointments, availability policies, and communication campaigns - all under a single unified platform.

## **1.2 Purpose & Goals**

- Provide a scalable, multi-tenant appointment scheduling platform for multiple firms.
- Enable a Super Admin to create, manage, and monitor all firms and their users.
- Allow firms to manage their own users, groups, and campaigns.
- Let individual users book appointments with each other with smart conflict prevention.
- Support timezone-aware scheduling, buffer times, and availability policies.
- Deliver automated notifications and a cancellation management system.

## **1.3 System Architecture Overview**

The platform follows a three-tier multi-tenant architecture:

| **Tier** | **Role**    | **Scope**                                |
| -------- | ----------- | ---------------------------------------- |
| Tier 1   | Super Admin | Platform-wide: manages all firms         |
| Tier 2   | Firm Admin  | Firm-wide: manages firm users & settings |
| Tier 3   | End User    | User-level: books & manages appointments |

# **2\. User Roles & Permissions**

## **2.1 Super Admin**

The Super Admin is the highest-authority user in the system. There is only one Super Admin account, which has full access to all firms and their data. Super Admin registration requires a special secret code - without it, the registration request is rejected.

### **Super Admin Capabilities:**

- Create, Read, Update, Delete (CRUD) firms on the platform.
- View complete list of all registered firms.
- View detailed data for each individual firm, including:
  - Total number of users per firm.
  - List of all users with individual user details.
  - Appointment statistics per user.
  - CRUD operations on firm users (add, edit, activate/deactivate, delete).
- Activate or deactivate any user account across any firm.
- View each user's complete appointment history with details such as who they booked with, time, and location.
- Launch campaigns targeting all users of a specific firm.
- NOTE: Group management (CRUD) is handled exclusively by Firm Admins. Super Admin does not create or manage groups.

## **2.2 Firm Admin (Firm-Level)**

Each firm may designate admin users who manage the firm's internal operations. Firm Admin capabilities are scoped to their own firm.

### **Firm Admin Capabilities:**

- Manage users within their firm (CRUD).
- Activate or deactivate users.
- View user appointment details within their firm.
- Create and manage groups within their firm.
- Launch campaigns for all firm users or specific groups.

## **2.3 End User**

End users are the primary consumers of the appointment booking service. Each end user belongs to exactly one firm.

### **End User Capabilities:**

- Book appointments with other users within the same firm only - cross-firm communication is not permitted.
- View and manage incoming appointment requests.
- Cancel appointments (own or incoming) with a mandatory cancellation reason.
- View a list of all cancelled appointments and associated reasons.
- Set personal availability policies (daily, weekly, weekends, holidays).
- Configure pre- and post-meeting buffer times.
- View all appointments in a timezone-aware calendar.

## **2.4 Firm Communication Boundary Rules**

The platform enforces strict firm-level isolation. All communication and appointment booking is restricted within the same firm:

| **Rule**                                          | **Applies To** | **Behavior**                                           |
| ------------------------------------------------- | -------------- | ------------------------------------------------------ |
| Users can only book with users of the same firm   | End Users      | Cross-firm booking requests are blocked at API level   |
| Users can only search/see users of their own firm | End Users      | User search results are filtered by firm_id            |
| Campaigns reach only users of the sending firm    | Firm Admin     | Campaign target list is always scoped to firm_id       |
| Groups contain only users from the same firm      | Firm Admin     | Group member selection is restricted to own firm users |
| Notifications are delivered only within same firm | System         | Notification dispatch always validates firm_id match   |

This boundary is enforced at both the API middleware level (JWT claim includes firm_id) and database query level (all queries are filtered by firm_id). No frontend restriction alone is considered sufficient.

# **3\. Super Admin Dashboard**

## **3.1 Dashboard Overview**

Upon logging in, the Super Admin lands on a dashboard that provides a bird's-eye view of the entire platform. The dashboard displays:

- Total number of firms registered.
- Total number of users across all firms.
- Total number of appointments booked platform-wide.
- Recent activity feed.

## **3.2 Firm Management (CRUD)**

The Super Admin can perform full CRUD operations on firms:

| **Operation** | **Action**       | **Details**                                |
| ------------- | ---------------- | ------------------------------------------ |
| Create        | Add New Firm     | Name, address, contact email, plan, status |
| Read          | View Firm List   | Paginated list with search and filters     |
| Read          | View Firm Detail | All firm data + users + appointment stats  |
| Update        | Edit Firm        | Update any firm field                      |
| Delete        | Remove Firm      | Soft delete with data retention policy     |

## **3.3 Firm Detail View**

When the Super Admin clicks on a firm, they see the full firm detail page including:

- Firm profile: name, creation date, status (active/inactive), subscription plan.
- User list with individual user cards showing:
  - User name, email, role.
  - Account status (active/inactive).
  - Total appointments booked.
  - Last active date.
  - Quick action buttons: activate/deactivate, view profile.
- Firm-wide appointment statistics.
- Campaign history for the firm.
- Group list for the firm.

## **3.4 User Management (Super Admin Level)**

The Super Admin has complete control over all users across all firms:

- Add new users to any firm.
- Edit user profile and permissions.
- Activate or deactivate user accounts.
- View a user's full appointment list including:
  - Who the appointment was booked with.
  - Date, time, and timezone.
  - Location (physical or virtual link).
  - Status (upcoming, completed, cancelled).
  - Cancellation reason (if cancelled).
- Delete a user (soft delete with data preservation).

# **4\. Campaigns & Group Management**

## **4.1 Group Management (CRUD)**

Super Admins (and Firm Admins) can organize firm users into groups for targeted communication:

- Create groups with name, description, and list of members.
- Read: view all groups and their members.
- Update: add/remove members, rename group.
- Delete: remove a group (users remain unaffected).

## **4.2 Campaign Management**

Campaigns are bulk communications sent to users. They can be targeted at:

- All users in a firm.
- Specific groups within a firm.

### **Campaign Fields:**

- Campaign name and description.
- Target audience: entire firm or specific group.
- Channel: Email / Push Notification.
- Message subject and body.
- Schedule: send immediately or at a future date/time.
- Status: Draft, Scheduled, Sent, Failed.

# **5\. Appointment Booking System**

## **5.1 Booking an Appointment**

Users can book appointments with other users on the platform through the following workflow:

- User searches for another user they want to meet with.
- System displays the recipient's available time slots based on their availability policy.
- Booking user selects a date and time slot.
- Booking user fills in appointment details: title, location, agenda/notes.
- System validates the selected slot (no double booking, no conflicts, within policy hours).
- System sends a booking request to the recipient.
- Recipient accepts or declines the request.
- Both parties receive confirmation notifications.

## **5.2 Appointment Request Management**

Every user has an Appointment Requests inbox that shows:

- Incoming appointment requests from other users.
- Request details: requester name, proposed time, location, notes.
- Actions available: Accept, Decline, Propose New Time.
- Outgoing requests they have sent and their current status.

## **5.3 Cancellation Management System**

The platform supports a transparent and structured cancellation system:

### **Cancellation Rules:**

- Any party (booker or recipient) can cancel a confirmed appointment.
- A cancellation reason is mandatory - the system will not process a cancellation without a reason.
- Upon cancellation, both parties are notified with the cancellation reason.

### **Cancellation Views:**

- "Cancelled by Me" tab: lists appointments the user themselves cancelled, along with the reason they provided.
- "Cancelled on Me" tab: lists appointments cancelled by other parties, with their provided reason.

# **6\. Availability & Policy Settings**

## **6.1 Overview**

Each user can configure their personal availability policy, which the system uses to calculate bookable time slots. Policies are respected across all bookings.

## **6.2 Availability Policy Options**

| **Policy Type**     | **Description**                                                |
| ------------------- | -------------------------------------------------------------- |
| Daily Availability  | Set working hours for each day (e.g., 9:00 AM to 6:00 PM)      |
| Weekly Recurring    | Set which days of the week are available (e.g., Mon-Fri only)  |
| Weekend/Weekday     | Toggle availability for weekends vs weekdays separately        |
| Holiday Blocking    | Mark specific dates as unavailable (holidays, personal leaves) |
| Pre-Meeting Buffer  | Block time before each meeting (e.g., 15 minutes prior)        |
| Post-Meeting Buffer | Block time after each meeting (e.g., 10 minutes after)         |

## **6.3 Buffer Time Example**

Example scenario with buffer settings:

- Meeting scheduled at 10:00 AM.
- Pre-meeting buffer: 15 minutes.
- Post-meeting buffer: 10 minutes.
- System automatically blocks 9:45 AM to 10:00 AM and 11:00 AM to 11:10 AM (assuming 1-hour meeting).
- No back-to-back bookings are allowed within this protected window.

# **7\. Timezone Management & Conflict Prevention**

## **7.1 Automatic Timezone Conversion**

The system is timezone-aware and automatically converts appointment times for each participant:

- Every user account stores the user's local timezone.
- When User A (IST - India) books a slot, User B (EST - USA) sees the appointment in their own local time.
- Calendar views always display times in the viewing user's timezone.
- Notification times are also converted to local timezone before sending.

Example:

- User A in India books a slot at 7:00 PM IST.
- User B in New York sees the appointment as 8:30 AM EST.
- Both receive a confirmation email displaying their respective local times.

## **7.2 Automatic Conflict Prevention**

The system automatically prevents the following scenarios at the point of booking:

| **Conflict Type**     | **System Behavior**                                                       |
| --------------------- | ------------------------------------------------------------------------- |
| Double Booking        | Rejects booking if the user already has an appointment at that time       |
| Overlapping Meetings  | Checks all active appointments including buffer windows before confirming |
| Invalid Time Range    | Rejects slots that fall outside the user's availability policy hours      |
| Back-to-Back Meetings | Enforces pre/post buffer times to prevent consecutive bookings            |
| Holiday Conflicts     | Prevents booking on dates marked as holidays by the recipient             |

# **8\. Notification System**

## **8.1 Notification Channels**

The platform uses two communication channels for all system notifications:

### **Email Notifications (Development: Free Tier)**

- Provider: SendGrid Free Tier or Resend Free Tier (for development).
- Used for: appointment confirmations, cancellations, reminders, campaign messages.
- Templates: HTML email templates for each notification type.

### **Push Notifications (Development: Free Tier)**

- Provider: Firebase Cloud Messaging (FCM) - free tier.
- Used for: real-time in-app alerts, appointment reminders.
- Web Push support for browser-based notifications.

## **8.2 Automated Reminder Notifications**

The system automatically triggers reminders before every confirmed appointment:

- 10 minutes before the appointment: a reminder notification is sent to both parties.
- 1 minute before the appointment: a final alert notification is sent to both parties.
- Reminders are sent via both Email and Push Notification.
- Reminder jobs are managed by the background job scheduler (APScheduler / Celery).

## **8.3 Notification Triggers Summary**

| **Event**                        | **Recipients** | **Channel**  |
| -------------------------------- | -------------- | ------------ |
| New appointment request received | Recipient      | Email + Push |
| Appointment request accepted     | Requester      | Email + Push |
| Appointment request declined     | Requester      | Email + Push |
| Appointment cancelled            | Both parties   | Email + Push |
| Reminder: 10 mins before         | Both parties   | Email + Push |
| Reminder: 1 min before           | Both parties   | Email + Push |
| Campaign broadcast               | Group / Firm   | Email + Push |

# **9\. In-App Internal Notification System**

## **9.1 Overview**

In addition to external Email and Push Notifications, the platform includes a dedicated internal notification system - a live notification center visible inside the application for every logged-in user. This is a real-time, in-app notification feed that does not rely on any external service.

## **9.2 How It Works**

- Every system event (appointment request, acceptance, cancellation, reminder, campaign) generates an internal notification record in the database for the affected user.
- When the user is logged into the application, a notification bell icon in the header displays the count of unread notifications.
- Clicking the bell opens a notification panel/drawer that lists all recent notifications in reverse chronological order.
- Each notification shows: title, message body, timestamp, and a read/unread status indicator.
- Clicking a notification marks it as read and can deep-link the user to the relevant appointment or event.
- Real-time delivery is handled via WebSocket or Server-Sent Events (SSE) - the notification count updates live without requiring a page refresh.

## **9.3 Internal Notification Data Model**

| **Field**      | **Type**           | **Description**                                                        |
| -------------- | ------------------ | ---------------------------------------------------------------------- |
| id             | UUID               | Unique notification identifier                                         |
| user_id        | UUID (FK)          | The user who receives this notification                                |
| type           | ENUM               | appointment_request, accepted, declined, cancelled, reminder, campaign |
| title          | String             | Short notification heading (e.g. 'New Appointment Request')            |
| body           | Text               | Full notification message with context details                         |
| is_read        | Boolean            | False by default; set to True when user views it                       |
| appointment_id | UUID (nullable FK) | Reference to related appointment, if applicable                        |
| firm_id        | UUID (FK)          | Ensures notifications are scoped within firm boundary                  |
| created_at     | Timestamp          | When the notification was generated                                    |

## **9.4 Notification Triggers (Internal)**

| **System Event**             | **Recipient(s)** | **Internal Notification Message**                 |
| ---------------------------- | ---------------- | ------------------------------------------------- |
| Appointment request received | Recipient user   | '\[Name\] has requested an appointment with you'  |
| Appointment accepted         | Requester user   | '\[Name\] accepted your appointment request'      |
| Appointment declined         | Requester user   | '\[Name\] declined your appointment request'      |
| Appointment cancelled        | Both parties     | 'Appointment cancelled: \[Reason\]'               |
| Reminder: 10 mins before     | Both parties     | 'Your appointment starts in 10 minutes'           |
| Reminder: 1 min before       | Both parties     | 'Your appointment is starting now'                |
| Campaign received            | Targeted users   | '\[Firm\] sent you a message: \[Campaign Title\]' |

## **9.5 Real-Time Delivery Architecture**

- Backend: FastAPI WebSocket endpoint or Server-Sent Events (SSE) endpoint per user session.
- When a new notification is written to the database, the backend pushes it to the active WebSocket/SSE connection of the recipient.
- If the user is offline, notifications remain in the database and are fetched on next login via REST API (GET /api/v1/notifications).
- Unread count badge on the notification bell icon updates in real-time.
- Users can mark individual notifications as read or mark all as read.

## **9.6 Notification API Endpoints (Internal)**

- GET /api/v1/notifications - Fetch paginated list of own notifications (newest first)
- GET /api/v1/notifications/unread-count - Get count of unread notifications
- PATCH /api/v1/notifications/{id}/read - Mark a single notification as read
- PATCH /api/v1/notifications/read-all - Mark all notifications as read
- DELETE /api/v1/notifications/{id} - Delete a specific notification

# **10\. Technology Stack**

## **9.1 Frontend**

| **Technology** | **Version / Library** | **Purpose**                                         |
| -------------- | --------------------- | --------------------------------------------------- |
| Next.js        | Latest (App Router)   | React-based full-stack framework; SSR/SSG support   |
| Tailwind CSS   | v3.x                  | Utility-first CSS for responsive, modern UI design  |
| Axios          | v1.x                  | HTTP client for API communication with backend      |
| React Query    | v5.x (TanStack)       | Data fetching, caching, and server state management |

## **9.2 Backend**

| **Technology**     | **Library / Tool**  | **Purpose**                                      |
| ------------------ | ------------------- | ------------------------------------------------ |
| FastAPI            | v0.111+             | High-performance Python REST API framework       |
| SQLAlchemy         | v2.x (async)        | ORM for database models and query building       |
| Pydantic           | v2.x                | Data validation and serialization of API schemas |
| Alembic            | v1.x                | Database migration management tool               |
| JWT Authentication | python-jose / PyJWT | Secure token-based user authentication           |

## **9.3 Database**

| **Technology** | **Provider**                | **Purpose**                                       |
| -------------- | --------------------------- | ------------------------------------------------- |
| PostgreSQL     | Supabase (hosted)           | Primary relational database for all platform data |
| Supabase       | Cloud (free tier available) | Managed Postgres + Auth + Realtime + Storage      |

## **9.4 Background Jobs & Scheduling**

| **Technology** | **Library**                | **Purpose**                                                  |
| -------------- | -------------------------- | ------------------------------------------------------------ |
| APScheduler    | v3.x                       | In-process scheduler for reminder notifications              |
| Celery         | v5.x                       | Distributed task queue for heavy background jobs             |
| Redis          | redis-py                   | Message broker for Celery task queue                         |
| Cron Jobs      | system-level / Celery beat | Scheduled periodic tasks (daily cleanups, report generation) |

## **9.5 Notification Services (Free Development Tier)**

| **Channel**       | **Provider**                   | **Free Tier Limit**             |
| ----------------- | ------------------------------ | ------------------------------- |
| Email             | Resend / SendGrid              | 100-300 emails/day free         |
| Push Notification | Firebase Cloud Messaging (FCM) | Completely free, no daily limit |

# **11\. Authentication Module**

## **11.1 Overview**

The authentication module secures all platform entry points and manages user identity throughout the system lifecycle.

## **11.2 Auth Features**

| **Feature**              | **Implementation Details**                                                                                                                                                                     |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Super Admin Registration | Requires email, password AND a secret registration code stored in environment variable (e.g. SUPER_ADMIN_SECRET=dev-secret). Without the correct code, registration is rejected with HTTP 403. |
| User Registration        | Email + password, role assignment, firm assignment on creation. No secret code required for regular users.                                                                                     |
| User Login               | Email/password login, returns JWT access + refresh tokens                                                                                                                                      |
| JWT Tokens               | Access token (short-lived: 15 min), Refresh token (long-lived: 7 days)                                                                                                                         |
| Password Hashing         | bcrypt hashing via passlib - passwords never stored in plaintext                                                                                                                               |
| Token Refresh            | Endpoint to issue a new access token using the refresh token                                                                                                                                   |
| Role-Based Auth          | Super Admin, Firm Admin, User roles enforced at API middleware level                                                                                                                           |
| Password Reset           | Email-based OTP or reset link for forgotten password flow                                                                                                                                      |

### **Super Admin Secret Registration Code - Details:**

To prevent unauthorized Super Admin account creation, the Super Admin registration endpoint requires an additional mandatory field: registration_secret. This secret is defined in the server's environment variables only and is never exposed in any frontend code, API docs, or client response.

### **Registration Flow:**

- Request sent to POST /api/v1/auth/super-admin/register with: email, password, registration_secret.
- Backend compares the provided registration_secret against SUPER_ADMIN_SECRET from environment variables.
- If secret is missing or incorrect: API returns HTTP 403 Forbidden with message 'Invalid registration code'.
- If secret matches: Super Admin account is created and JWT tokens are returned.
- System enforces a single Super Admin rule - if one already exists, re-registration is blocked even with the correct secret.

## **11.3 Security Best Practices**

- Passwords are never stored in plaintext - only bcrypt hashes are saved.
- JWT tokens are signed with a secret key (HS256 algorithm).
- Refresh tokens are stored server-side and can be revoked on logout.
- All API endpoints are protected by dependency injection auth guards in FastAPI.
- Role checks are enforced at the route handler level for each resource.
- HTTPS is enforced in all production environments.

# **12\. Core Database Schema (Overview)**

## **12.1 Key Tables**

| **Table Name**        | **Key Fields & Purpose**                                                                |
| --------------------- | --------------------------------------------------------------------------------------- |
| firms                 | id, name, email, status, plan, created_at, deleted_at                                   |
| users                 | id, firm_id, email, password_hash, role, is_active, timezone, created_at                |
| availability_policies | id, user_id, day_of_week, start_time, end_time, is_holiday, buffer_before, buffer_after |
| appointments          | id, requester_id, recipient_id, start_time, end_time, title, location, status, notes    |
| cancellations         | id, appointment_id, cancelled_by, reason, cancelled_at                                  |
| groups                | id, firm_id, name, description, created_by, created_at                                  |
| group_members         | id, group_id, user_id, added_at                                                         |
| campaigns             | id, firm_id, group_id (nullable), title, message, channel, status, scheduled_at         |
| notifications         | id, user_id, type, title, body, is_read, sent_at, appointment_id (ref)                  |

# **13\. API Endpoint Structure**

## **13.1 Authentication Endpoints**

- POST /api/v1/auth/register - Register a new user
- POST /api/v1/auth/login - Login and receive JWT tokens
- POST /api/v1/auth/refresh - Refresh access token
- POST /api/v1/auth/logout - Revoke refresh token
- POST /api/v1/auth/forgot-password - Initiate password reset
- POST /api/v1/auth/reset-password - Complete password reset with token

## **13.2 Super Admin Endpoints**

- GET /api/v1/admin/firms - List all firms
- POST /api/v1/admin/firms - Create a firm
- GET /api/v1/admin/firms/{id} - Get firm detail with user list
- PUT /api/v1/admin/firms/{id} - Update firm
- DELETE /api/v1/admin/firms/{id} - Soft delete firm
- GET /api/v1/admin/users - List all users across all firms
- GET /api/v1/admin/users/{id} - Get user detail with appointments
- PATCH /api/v1/admin/users/{id}/status - Activate/deactivate user

## **13.3 Firm Endpoints**

- GET /api/v1/firm/users - List users in own firm
- POST /api/v1/firm/users - Add user to firm
- PUT /api/v1/firm/users/{id} - Update firm user
- DELETE /api/v1/firm/users/{id} - Remove user
- GET /api/v1/firm/groups - List groups in firm
- POST /api/v1/firm/groups - Create a group
- PUT /api/v1/firm/groups/{id} - Update group
- DELETE /api/v1/firm/groups/{id} - Delete group
- POST /api/v1/firm/campaigns - Launch a campaign

## **13.4 User Endpoints**

- GET /api/v1/appointments - List own appointments
- POST /api/v1/appointments - Create/book an appointment
- GET /api/v1/appointments/requests - View incoming requests
- PATCH /api/v1/appointments/{id}/accept - Accept a request
- PATCH /api/v1/appointments/{id}/decline - Decline a request
- POST /api/v1/appointments/{id}/cancel - Cancel with reason
- GET /api/v1/availability - Get own availability policy
- PUT /api/v1/availability - Update availability policy
- GET /api/v1/users/search - Search users to book with
- GET /api/v1/notifications - List notifications

# **14\. Key System Workflows**

## **14.1 Appointment Booking Flow**

- User A searches for User B by name or email.
- System fetches User B's available slots (respecting their policy, buffers, holidays, timezone).
- User A picks a slot and fills in appointment details.
- System validates: no double booking, no conflict with buffer times, within policy hours.
- If valid: system creates appointment in 'PENDING' status and sends request notification to User B.
- User B receives Email + Push notification with request details.
- User B accepts → status changes to 'CONFIRMED', both users get confirmation notification.
- User B declines → status changes to 'DECLINED', User A gets decline notification.
- 10 minutes before start → reminder sent to both.
- 1 minute before start → final reminder sent to both.

## **14.2 Cancellation Flow**

- User (either party) opens the appointment and clicks 'Cancel'.
- System shows a mandatory 'Reason for Cancellation' text field.
- User enters reason and confirms cancellation.
- System changes appointment status to 'CANCELLED'.
- System logs the cancellation in the cancellations table with reason and cancelled_by.
- Both parties receive a cancellation notification including the reason.
- Cancelled appointment appears in the 'Cancelled' section for both users.

## **14.3 Campaign Launch Flow**

- Super Admin or Firm Admin navigates to Campaigns section.
- Clicks 'Create Campaign'.
- Fills in campaign details: title, message, target (all firm users or specific group), channel.
- Selects send time: immediate or scheduled.
- Reviews and confirms launch.
- If immediate: Celery task dispatches emails/push notifications to all targeted users.
- If scheduled: APScheduler or Celery Beat triggers the task at the specified time.
- Campaign status updates to 'SENT' upon completion.

# **15\. Project Modules Summary**

| **Module**          | **Key Features**                            | **Status**  |
| ------------------- | ------------------------------------------- | ----------- |
| Auth Module         | Registration, Login, JWT, Password Reset    | To be built |
| Super Admin Module  | Firm CRUD, User oversight, Global stats     | To be built |
| Firm Module         | User CRUD, Group CRUD, Campaigns            | To be built |
| Appointment Module  | Booking, Requests, Cancellation, History    | To be built |
| Availability Module | Policy, Buffer, Holiday Blocking            | To be built |
| Timezone Module     | Auto-conversion, UTC storage, Display local | To be built |
| Conflict Prevention | Double-booking, Overlap, Buffer enforcement | To be built |
| Notification Module | Email, Push, Reminders (10 & 1 min)         | To be built |
| Campaign Module     | Bulk messaging, Scheduling, Group targeting | To be built |
| Background Jobs     | Celery, APScheduler, Redis, Cron            | To be built |

# **16\. Deployment Considerations**

## **16.1 Recommended Deployment Stack**

- Frontend: Vercel (Next.js native hosting, free tier available).
- Backend: Railway or Render (FastAPI container deployment, free tier available).
- Database: Supabase (managed PostgreSQL, generous free tier).
- Redis (for Celery): Upstash Redis - serverless, free tier available.
- Push Notifications: Firebase Cloud Messaging (completely free).
- Email: Resend.com or SendGrid free tier (100-300 emails/day).

## **16.2 Environment Variables Required**

- DATABASE_URL - Supabase PostgreSQL connection string.
- JWT_SECRET_KEY - Secret key for signing JWT tokens.
- REDIS_URL - Redis broker URL for Celery.
- EMAIL_API_KEY - API key for Resend or SendGrid.
- FCM_SERVER_KEY - Firebase Cloud Messaging server key.
- SUPABASE_URL and SUPABASE_KEY - For Supabase client calls.

**End of Document**

Multi-Tenant Appointment Booking Platform - Project Documentation v1.0
