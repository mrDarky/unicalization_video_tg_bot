# Admin Panel Features Documentation

This document describes the new admin panel features implemented for the Video Bot.

## Overview

Three major features have been added to enhance the admin panel:
1. **Authentication** - Secure login system for admin access
2. **Tariff Plans** - Configurable pricing tiers with video limits
3. **Video Limitations** - Enforcement of daily and per-order video processing limits

## 1. Authentication System

### Features
- Secure JWT-based authentication
- Session management using secure HTTP-only cookies
- Login page with username/password authentication
- Protected admin routes
- Logout functionality

### Configuration
Set the following environment variables in your `.env` file:

```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here
SECRET_KEY=your_secret_key_for_jwt_signing
```

⚠️ **Security Note**: Always change the default credentials in production!

### Usage
1. Navigate to the admin panel: `http://localhost:8000/login`
2. Enter your admin credentials
3. You'll be redirected to the dashboard upon successful login
4. Click "Logout" in the sidebar to end your session

## 2. Tariff Plans Management

### Features
- Create, read, update, and delete tariff plans
- Configure limits per plan:
  - **Videos per Day**: Maximum videos a user can process daily
  - **Videos per Order**: Maximum videos a user can process in a single batch
  - **Price**: Cost of the plan (informational)
  - **Status**: Active/Inactive toggle
- Assign tariff plans to individual users
- View assigned tariff plans in the users list

### Accessing Tariff Plans
Navigate to: **Admin Panel → Tariff Plans**

### Creating a Tariff Plan
1. Click "Add Tariff Plan"
2. Fill in the details:
   - **Name**: Plan identifier (e.g., "Basic", "Premium", "Enterprise")
   - **Description**: Brief description of the plan
   - **Videos per Day**: Daily processing limit (e.g., 10)
   - **Videos per Order**: Per-batch limit (e.g., 3)
   - **Price**: Cost in dollars (e.g., 9.99)
   - **Active**: Check to make the plan available
3. Click "Save"

### Assigning Plans to Users
1. Navigate to **Admin Panel → Users**
2. Find the user you want to assign a plan to
3. Click the card icon (📋) button next to the user
4. Select a tariff plan from the dropdown
5. Click "Assign"

### Default Behavior
Users without an assigned tariff plan receive default limits:
- **Daily Limit**: 5 videos per day
- **Per-Order Limit**: 3 videos per batch

## 3. Video Limitations

### How It Works
The system enforces limits at the beginning of video processing:

1. **Order Check**: When a user submits videos for processing, the system checks if the batch size exceeds their per-order limit
2. **Daily Check**: The system checks if processing the batch would exceed their daily limit
3. **Rejection**: If either limit is exceeded, processing is rejected with a clear error message
4. **Tracking**: After successful processing, the daily counter is incremented

### User Experience
When limits are exceeded, users see clear messages:

```
❌ Order limit exceeded. Maximum 3 videos per order.
Please try again later or upgrade your plan.
```

or

```
❌ Daily limit exceeded. You have 0 videos remaining today (limit: 10).
Please try again later or upgrade your plan.
```

### Supported Modes
All video processing modes respect tariff limits:
- **Mode 1**: Single video processing with filters
- **Mode 2**: Two-group video merging
- **Mode N**: Multi-group video combining

### Daily Reset
Daily usage counters are tracked per calendar day. The system automatically starts fresh counts each day based on the date field in the `daily_video_usage` table.

## Database Schema

### New Tables

#### `tariff_plans`
- `id`: Primary key
- `name`: Plan name (unique)
- `description`: Plan description
- `videos_per_day`: Daily video limit
- `videos_per_order`: Per-order video limit
- `price`: Plan price
- `is_active`: Active status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

#### `daily_video_usage`
- `id`: Primary key
- `user_id`: Foreign key to users table
- `date`: Date of usage
- `video_count`: Number of videos processed

### Modified Tables

#### `users`
- Added `tariff_plan_id`: Foreign key to tariff_plans table (nullable)

## API Endpoints

### Tariff Plans
- `GET /api/tariff-plans/`: List all tariff plans
- `GET /api/tariff-plans/{id}`: Get specific tariff plan
- `POST /api/tariff-plans/`: Create new tariff plan
- `PUT /api/tariff-plans/{id}`: Update tariff plan
- `DELETE /api/tariff-plans/{id}`: Delete tariff plan
- `POST /api/tariff-plans/assign`: Assign plan to user

### Authentication
- `GET /login`: Login page
- `POST /login`: Login submission
- `GET /logout`: Logout

### Protected Routes
All `/admin/*` routes now require authentication via session cookie.

## Testing

Run the test suite to verify all features:

```bash
python test_admin_features.py
```

This tests:
- Database models
- CRUD operations
- Limit checking logic
- Authentication functions

## Troubleshooting

### Users not seeing tariff plan
- Ensure the relationship is eagerly loaded with `selectinload(User.tariff_plan)`
- Check that the tariff plan is active

### Limits not enforced
- Verify the user has a tariff plan assigned
- Check the database for `daily_video_usage` records
- Ensure the date comparison is working correctly

### Authentication issues
- Verify `SECRET_KEY` is set in environment variables
- Check cookie settings if running behind a proxy
- Ensure browser accepts cookies

## Future Enhancements

Possible improvements:
- Payment integration for tariff plans
- Usage analytics and reporting
- Automatic plan upgrades/downgrades
- Email notifications for limit warnings
- Multi-admin support with roles
- API keys for programmatic access
