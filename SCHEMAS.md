# MongoDB Collections Schema Documentation

This document describes the structure of all MongoDB collections used in the Job Application Tracker.

## Collections Overview

- **applications** - Job application tracking
- **companies** - Company information

---

## 1. Applications Collection

**Collection Name:** `applications`

### Schema Structure

```javascript
{
  _id: ObjectId,                    // Auto-generated MongoDB ID
  user_id: Integer,                 // Reference to Django User.id

  // Company Information (Embedded Document)
  company: {
    name: String,                   // Required - Company name
    website: String,                // Optional - Company website URL
    industry: String,               // Optional - Industry (e.g., "Technology")
    size: String,                   // Optional - Company size (e.g., "1000-5000")
    location: String,               // Optional - Location (e.g., "San Francisco, CA")
    logo_url: String                // Optional - Company logo URL
  },

  // Job Information (Embedded Document)
  job: {
    title: String,                  // Required - Job title
    description: String,            // Optional - Job description
    job_url: String,                // Optional - Job posting URL
    employment_type: String,        // Optional - "full-time", "part-time", "contract", "internship"
    work_mode: String,              // Optional - "remote", "hybrid", "onsite"
    experience_level: String,       // Optional - "entry", "mid", "senior", "lead"
    salary_min: Number,             // Optional - Minimum salary
    salary_max: Number,             // Optional - Maximum salary
    currency: String                // Optional - Default "USD"
  },

  // Application Status (Embedded Document)
  application: {
    applied_date: Date,             // Date when applied (default: now)
    source: String,                 // Optional - "LinkedIn", "Indeed", "Company Website", etc.
    status: String,                 // Required - "applied", "screening", "interview", "offer", "rejected", "accepted", "withdrawn"
    resume_version: String,         // Optional - Resume filename used
    cover_letter: String,           // Optional - Cover letter text
    referral_name: String           // Optional - Name of referrer
  },

  // Job Requirements (Embedded Document)
  requirements: {
    skills_required: [String],      // Array - Required skills
    skills_preferred: [String],     // Array - Preferred skills
    years_experience: Number,       // Optional - Years of experience required
    education: String               // Optional - Education requirement
  },

  // Timeline Events (Array of Embedded Documents)
  timeline: [
    {
      date: Date,                   // Event date
      event_type: String,           // "applied", "phone_screen", "interview", "offer", "rejection", etc.
      title: String,                // Event title
      notes: String,                // Optional - Event notes
      interviewer_name: String,     // Optional - Interviewer name
      interview_type: String        // Optional - "phone", "video", "onsite", etc.
    }
  ],

  // File Attachments (Array of Embedded Documents)
  attachments: [
    {
      filename: String,             // Original filename
      original_name: String,        // Original name before upload
      file_path: String,            // Path in storage
      file_url: String,             // Public URL
      file_size: Number,            // File size in bytes
      file_type: String,            // File extension (without dot)
      uploaded_at: Date             // Upload timestamp
    }
  ],

  // Additional Fields
  notes: String,                    // Optional - Personal notes
  is_favorite: Boolean,             // Default false

  // Timestamps
  created_at: Date,                 // Auto - Creation timestamp
  updated_at: Date                  // Auto - Last update timestamp
}
```

### Example Document

```javascript
{
  "_id": ObjectId("674a1b2c3d4e5f6789012345"),
  "user_id": 1,
  "company": {
    "name": "Google",
    "website": "https://google.com",
    "industry": "Technology",
    "size": "10000+",
    "location": "Mountain View, CA",
    "logo_url": "https://logo.clearbit.com/google.com"
  },
  "job": {
    "title": "Backend Developer",
    "description": "Work on scalable backend systems",
    "job_url": "https://careers.google.com/jobs/123",
    "employment_type": "full-time",
    "work_mode": "remote",
    "experience_level": "mid",
    "salary_min": 100000,
    "salary_max": 150000,
    "currency": "USD"
  },
  "application": {
    "applied_date": ISODate("2025-01-15T10:00:00Z"),
    "source": "LinkedIn",
    "status": "interview",
    "resume_version": "Resume_v3.pdf",
    "cover_letter": "I am excited to apply...",
    "referral_name": "John Doe"
  },
  "requirements": {
    "skills_required": ["Python", "Django", "PostgreSQL"],
    "skills_preferred": ["AWS", "Docker", "Kubernetes"],
    "years_experience": 2,
    "education": "Bachelor's in Computer Science"
  },
  "timeline": [
    {
      "date": ISODate("2025-01-15T10:00:00Z"),
      "event_type": "applied",
      "title": "Application submitted",
      "notes": "Applied through LinkedIn"
    },
    {
      "date": ISODate("2025-01-20T14:00:00Z"),
      "event_type": "phone_screen",
      "title": "Phone screening with recruiter",
      "notes": "Discussed role and compensation",
      "interviewer_name": "Sarah Johnson",
      "interview_type": "phone"
    }
  ],
  "attachments": [
    {
      "filename": "offer_letter.pdf",
      "original_name": "Google_Offer_Letter.pdf",
      "file_path": "uploads/1/document/abc123.pdf",
      "file_url": "/media/uploads/1/document/abc123.pdf",
      "file_size": 245678,
      "file_type": "pdf",
      "uploaded_at": ISODate("2025-01-25T09:00:00Z")
    }
  ],
  "notes": "Very interested in this position. Great team culture.",
  "is_favorite": true,
  "created_at": ISODate("2025-01-15T10:00:00Z"),
  "updated_at": ISODate("2025-01-25T10:00:00Z")
}
```

### Indexes

```javascript
// Primary indexes
db.applications.createIndex({ user_id: 1, created_at: -1 });
db.applications.createIndex({ "company.name": 1 });
db.applications.createIndex({ "job.title": 1 });
db.applications.createIndex({ "application.status": 1 });

// Text search index
db.applications.createIndex({
  "company.name": "text",
  "job.title": "text",
  notes: "text",
});
```

---

## 2. Companies Collection

**Collection Name:** `companies`

### Schema Structure

```javascript
{
  _id: ObjectId,                    // Auto-generated MongoDB ID
  user_id: Integer,                 // Reference to Django User.id

  // Basic Information
  name: String,                     // Required - Company name
  website: String,                  // Optional - Company website
  industry: String,                 // Optional - Industry
  size: String,                     // Optional - Company size
  location: String,                 // Optional - Location
  logo_url: String,                 // Optional - Logo URL
  description: String,              // Optional - Company description
  glassdoor_rating: Number,         // Optional - Rating (0-5)

  // User-specific fields
  notes: String,                    // Optional - Personal notes
  is_favorite: Boolean,             // Default false
  tags: [String],                   // Array - Custom tags

  // Contact Information (Embedded Document)
  contact_info: {
    recruiter_name: String,         // Optional
    recruiter_email: String,        // Optional
    recruiter_phone: String,        // Optional
    hr_contact: String              // Optional
  },

  // Timestamps
  created_at: Date,                 // Auto - Creation timestamp
  updated_at: Date                  // Auto - Last update timestamp
}
```

### Example Document

```javascript
{
  "_id": ObjectId("674b2c3d4e5f6789012346"),
  "user_id": 1,
  "name": "Google",
  "website": "https://google.com",
  "industry": "Technology",
  "size": "10000+",
  "location": "Mountain View, CA",
  "logo_url": "https://logo.clearbit.com/google.com",
  "description": "Multinational technology company",
  "glassdoor_rating": 4.5,
  "notes": "Great company culture, good benefits",
  "is_favorite": true,
  "tags": ["FAANG", "Remote-friendly", "Tech"],
  "contact_info": {
    "recruiter_name": "Jane Smith",
    "recruiter_email": "jane.smith@google.com",
    "recruiter_phone": "+1-650-555-0100",
    "hr_contact": "hr-tech@google.com"
  },
  "created_at": ISODate("2025-01-10T10:00:00Z"),
  "updated_at": ISODate("2025-01-20T15:00:00Z")
}
```

### Indexes

```javascript
db.companies.createIndex({ user_id: 1, name: 1 }, { unique: true });
db.companies.createIndex({ industry: 1 });
db.companies.createIndex({ name: "text", industry: "text", location: "text" });
```

---

## Status Values Reference

### Application Statuses

- `applied` - Application submitted
- `screening` - Initial screening in progress
- `interview` - Interview scheduled/in progress
- `technical_test` - Technical assessment phase
- `offer` - Offer received
- `rejected` - Application rejected
- `accepted` - Offer accepted
- `withdrawn` - Application withdrawn

### Event Types

- `applied` - Application submitted
- `phone_screen` - Phone screening
- `technical_interview` - Technical interview
- `behavioral_interview` - Behavioral interview
- `system_design` - System design interview
- `coding_challenge` - Coding challenge
- `onsite_interview` - Onsite interview
- `final_round` - Final round interview
- `offer_received` - Offer received
- `offer_negotiation` - Offer negotiation
- `rejection` - Rejection received
- `status_change` - Status changed

---

## Query Examples

### Common Queries

```javascript
// Get all applications for a user
db.applications.find({ user_id: 1 });

// Get applications by status
db.applications.find({
  user_id: 1,
  "application.status": "interview",
});

// Get applications by company
db.applications.find({
  user_id: 1,
  "company.name": "Google",
});

// Get favorite applications
db.applications.find({
  user_id: 1,
  is_favorite: true,
});

// Search applications
db.applications.find({
  user_id: 1,
  $text: { $search: "backend developer" },
});

// Get applications in date range
db.applications.find({
  user_id: 1,
  "application.applied_date": {
    $gte: ISODate("2025-01-01"),
    $lte: ISODate("2025-12-31"),
  },
});
```

### Aggregation Queries

```javascript
// Count applications by status
db.applications.aggregate([
  { $match: { user_id: 1 } },
  {
    $group: {
      _id: "$application.status",
      count: { $sum: 1 },
    },
  },
]);

// Get top companies by application count
db.applications.aggregate([
  { $match: { user_id: 1 } },
  {
    $group: {
      _id: "$company.name",
      count: { $sum: 1 },
    },
  },
  { $sort: { count: -1 } },
  { $limit: 10 },
]);

// Get skills demand
db.applications.aggregate([
  { $match: { user_id: 1 } },
  { $unwind: "$requirements.skills_required" },
  {
    $group: {
      _id: "$requirements.skills_required",
      count: { $sum: 1 },
    },
  },
  { $sort: { count: -1 } },
]);
```

---

## Migration & Setup

### Create Indexes

Run this in MongoDB shell or add to setup script:

```javascript
// Applications indexes
db.applications.createIndex({ user_id: 1, created_at: -1 });
db.applications.createIndex({ "company.name": 1 });
db.applications.createIndex({ "application.status": 1 });
db.applications.createIndex({
  "company.name": "text",
  "job.title": "text",
  notes: "text",
});

// Companies indexes
db.companies.createIndex({ user_id: 1, name: 1 }, { unique: true });
db.companies.createIndex({ name: "text", industry: "text" });
```

---

## Notes for Developers

1. **No Migrations**: MongoDB is schemaless. You can add new fields anytime without migrations.
2. **Validation**: Validation happens at the application level (Django serializers), not in MongoDB.

3. **References**: `user_id` is a reference to Django's User model (stored in SQLite).

4. **Embedded vs Referenced**:

   - Company/Job data is embedded (denormalized) for performance
   - User data is referenced (normalized) for security

5. **Flexible Schema**: Different applications can have different fields. This is intentional.

6. **Services**: Use service classes (`ApplicationService`, `CompanyService`) to interact with MongoDB, not Django models.

---

## See Also

- Service implementations: `apps/applications/services.py`
- Serializers: `apps/applications/serializers.py`
- API Documentation: http://localhost:8000/api/docs/
