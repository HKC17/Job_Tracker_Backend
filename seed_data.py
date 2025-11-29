"""
Data seeding script for Job Application Tracker.
Creates realistic sample applications for testing and ML training.
"""

from config.mongodb import get_collection
from django.contrib.auth import get_user_model
import os
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


User = get_user_model()

# Sample data
COMPANIES = [
    {'name': 'Google', 'website': 'https://google.com', 'industry': 'Technology',
        'size': '10000+', 'location': 'Mountain View, CA'},
    {'name': 'Microsoft', 'website': 'https://microsoft.com',
        'industry': 'Technology', 'size': '10000+', 'location': 'Redmond, WA'},
    {'name': 'Amazon', 'website': 'https://amazon.com',
        'industry': 'E-commerce', 'size': '10000+', 'location': 'Seattle, WA'},
    {'name': 'Meta', 'website': 'https://meta.com', 'industry': 'Technology',
        'size': '10000+', 'location': 'Menlo Park, CA'},
    {'name': 'Apple', 'website': 'https://apple.com',
        'industry': 'Technology', 'size': '10000+', 'location': 'Cupertino, CA'},
    {'name': 'Netflix', 'website': 'https://netflix.com',
        'industry': 'Entertainment', 'size': '5000-10000', 'location': 'Los Gatos, CA'},
    {'name': 'Tesla', 'website': 'https://tesla.com',
        'industry': 'Automotive', 'size': '10000+', 'location': 'Palo Alto, CA'},
    {'name': 'Airbnb', 'website': 'https://airbnb.com', 'industry': 'Travel',
        'size': '5000-10000', 'location': 'San Francisco, CA'},
    {'name': 'Uber', 'website': 'https://uber.com', 'industry': 'Transportation',
        'size': '10000+', 'location': 'San Francisco, CA'},
    {'name': 'Spotify', 'website': 'https://spotify.com', 'industry': 'Music',
        'size': '5000-10000', 'location': 'Stockholm, Sweden'},
    {'name': 'LinkedIn', 'website': 'https://linkedin.com',
        'industry': 'Technology', 'size': '10000+', 'location': 'Sunnyvale, CA'},
    {'name': 'Twitter', 'website': 'https://twitter.com', 'industry': 'Social Media',
        'size': '5000-10000', 'location': 'San Francisco, CA'},
    {'name': 'Salesforce', 'website': 'https://salesforce.com',
        'industry': 'Software', 'size': '10000+', 'location': 'San Francisco, CA'},
    {'name': 'Adobe', 'website': 'https://adobe.com', 'industry': 'Software',
        'size': '10000+', 'location': 'San Jose, CA'},
    {'name': 'Oracle', 'website': 'https://oracle.com',
        'industry': 'Software', 'size': '10000+', 'location': 'Austin, TX'},
    {'name': 'IBM', 'website': 'https://ibm.com', 'industry': 'Technology',
        'size': '10000+', 'location': 'Armonk, NY'},
    {'name': 'Intel', 'website': 'https://intel.com', 'industry': 'Hardware',
        'size': '10000+', 'location': 'Santa Clara, CA'},
    {'name': 'Nvidia', 'website': 'https://nvidia.com',
        'industry': 'Hardware', 'size': '10000+', 'location': 'Santa Clara, CA'},
    {'name': 'Stripe', 'website': 'https://stripe.com', 'industry': 'Fintech',
        'size': '1000-5000', 'location': 'San Francisco, CA'},
    {'name': 'Shopify', 'website': 'https://shopify.com', 'industry': 'E-commerce',
        'size': '5000-10000', 'location': 'Ottawa, Canada'},
]

JOB_TITLES = [
    'Backend Developer',
    'Frontend Developer',
    'Full Stack Developer',
    'Software Engineer',
    'Senior Software Engineer',
    'DevOps Engineer',
    'Data Engineer',
    'Machine Learning Engineer',
    'Python Developer',
    'Django Developer',
    'React Developer',
    'Cloud Engineer',
    'Solutions Architect',
    'Technical Lead',
    'Engineering Manager',
]

SKILLS = [
    'Python', 'Django', 'Flask', 'FastAPI',
    'JavaScript', 'React', 'Vue.js', 'Angular',
    'Node.js', 'Express.js', 'MongoDB', 'PostgreSQL',
    'MySQL', 'Redis', 'Docker', 'Kubernetes',
    'AWS', 'Azure', 'GCP', 'Git',
    'CI/CD', 'REST API', 'GraphQL', 'Microservices',
    'Agile', 'Scrum', 'TDD', 'Machine Learning',
]

EMPLOYMENT_TYPES = ['full-time', 'part-time', 'contract', 'internship']
WORK_MODES = ['remote', 'hybrid', 'onsite']
EXPERIENCE_LEVELS = ['entry', 'mid', 'senior', 'lead']
SOURCES = ['LinkedIn', 'Indeed', 'Company Website',
           'Referral', 'Recruiter', 'AngelList', 'Glassdoor']
STATUSES = ['applied', 'screening', 'interview', 'technical_test',
            'offer', 'rejected', 'accepted', 'withdrawn']

EVENT_TYPES = [
    'phone_screen', 'technical_interview', 'behavioral_interview',
    'system_design', 'coding_challenge', 'onsite_interview',
    'final_round', 'offer_received', 'offer_negotiation'
]


def create_sample_user():
    """Create a sample user if not exists."""
    email = 'demo@example.com'

    try:
        user = User.objects.get(email=email)
        print(f'✅ Using existing user: {email}')
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            password='DemoPass123!',
            first_name='Demo',
            last_name='User'
        )
        user.skills = ['Python', 'Django', 'React', 'MongoDB', 'AWS', 'Docker']
        user.years_of_experience = 1.5
        user.current_role = 'Backend Developer'
        user.save()
        print(f'✅ Created new user: {email}')

    return user


def generate_timeline_events(applied_date, status, num_events):
    """Generate realistic timeline events."""
    timeline = []
    current_date = applied_date

    # First event: Application submitted
    timeline.append({
        'date': current_date,
        'event_type': 'applied',
        'title': 'Application submitted',
        'notes': 'Applied through job portal'
    })

    # Generate intermediate events based on status
    if status in ['screening', 'interview', 'technical_test', 'offer', 'rejected', 'accepted']:
        # Phone screen (1-7 days after application)
        current_date += timedelta(days=random.randint(1, 7))
        timeline.append({
            'date': current_date,
            'event_type': 'phone_screen',
            'title': 'Phone screening with recruiter',
            'notes': 'Discussed role, experience, and compensation',
            'interviewer_name': random.choice(['Sarah Johnson', 'Mike Chen', 'Emily Davis', 'John Smith'])
        })

    if status in ['interview', 'technical_test', 'offer', 'rejected', 'accepted']:
        # Technical interview (3-5 days after phone screen)
        current_date += timedelta(days=random.randint(3, 5))
        timeline.append({
            'date': current_date,
            'event_type': 'technical_interview',
            'title': 'Technical interview',
            'notes': 'Coding problems and system design discussion',
            'interviewer_name': random.choice(['Alex Kumar', 'Rachel Lee', 'David Brown', 'Lisa Wang']),
            'interview_type': 'video'
        })

    if status in ['offer', 'accepted']:
        # Final round (5-7 days after technical)
        current_date += timedelta(days=random.randint(5, 7))
        timeline.append({
            'date': current_date,
            'event_type': 'final_round',
            'title': 'Final round with hiring manager',
            'notes': 'Team fit and culture discussion',
            'interviewer_name': random.choice(['Robert Taylor', 'Jennifer Martinez', 'James Wilson', 'Maria Garcia'])
        })

        # Offer received (2-4 days after final)
        current_date += timedelta(days=random.randint(2, 4))
        timeline.append({
            'date': current_date,
            'event_type': 'offer_received',
            'title': 'Offer received',
            'notes': 'Competitive offer with good benefits package'
        })

    if status == 'rejected':
        # Rejection (1-3 days after last interview)
        current_date += timedelta(days=random.randint(1, 3))
        timeline.append({
            'date': current_date,
            'event_type': 'rejection',
            'title': 'Application rejected',
            'notes': 'Moving forward with other candidates'
        })

    return timeline[:num_events]


def generate_application(user_id, days_ago):
    """Generate a single realistic application."""
    company = random.choice(COMPANIES)
    job_title = random.choice(JOB_TITLES)

    # Applied date (X days ago)
    applied_date = datetime.utcnow() - timedelta(days=days_ago)

    # Status based on how long ago (newer = more likely to be in progress)
    if days_ago < 7:
        status = random.choice(['applied', 'screening', 'interview'])
    elif days_ago < 30:
        status = random.choice(
            ['applied', 'screening', 'interview', 'technical_test', 'rejected', 'withdrawn'])
    else:
        status = random.choice(['rejected', 'withdrawn', 'offer', 'accepted'])

    # Random skills (5-10 skills)
    num_skills = random.randint(5, 10)
    required_skills = random.sample(SKILLS, num_skills)

    # Salary range based on experience level
    experience_level = random.choice(EXPERIENCE_LEVELS)
    if experience_level == 'entry':
        salary_min = random.randint(60000, 80000)
        salary_max = salary_min + random.randint(15000, 25000)
    elif experience_level == 'mid':
        salary_min = random.randint(80000, 120000)
        salary_max = salary_min + random.randint(20000, 40000)
    elif experience_level == 'senior':
        salary_min = random.randint(120000, 160000)
        salary_max = salary_min + random.randint(30000, 60000)
    else:  # lead
        salary_min = random.randint(150000, 200000)
        salary_max = salary_min + random.randint(40000, 80000)

    # Timeline events
    num_events = random.randint(1, 5)
    timeline = generate_timeline_events(applied_date, status, num_events)

    application = {
        'user_id': user_id,
        'company': company,
        'job': {
            'title': job_title,
            'description': f'Looking for a {job_title} to join our team.',
            'job_url': f'{company["website"]}/careers/{job_title.lower().replace(" ", "-")}',
            'employment_type': random.choice(EMPLOYMENT_TYPES),
            'work_mode': random.choice(WORK_MODES),
            'experience_level': experience_level,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'currency': 'USD'
        },
        'application': {
            'applied_date': applied_date,
            'source': random.choice(SOURCES),
            'status': status,
            'resume_version': f'Resume_v{random.randint(1, 5)}.pdf',
            'cover_letter': 'Customized cover letter for this position',
            # 60% no referral
            'referral_name': random.choice(['', '', '', 'John Doe', 'Jane Smith'])
        },
        'requirements': {
            'skills_required': required_skills,
            'skills_preferred': random.sample(SKILLS, random.randint(2, 5)),
            'years_experience': random.choice([1, 1.5, 2, 3, 4, 5]),
            'education': random.choice(['Bachelor\'s', 'Master\'s', 'Bachelor\'s or equivalent experience'])
        },
        'timeline': timeline,
        'attachments': [],
        'notes': random.choice([
            'Really excited about this role!',
            'Good company culture from what I heard',
            'Matches my career goals',
            'Referral from a friend',
            'Challenging position with growth opportunities',
            ''
        ]),
        # 25% favorites
        'is_favorite': random.choice([True, False, False, False]),
        'created_at': applied_date,
        'updated_at': datetime.utcnow(),
    }

    return application


def seed_applications(user, num_applications=50):
    """Seed applications for a user."""
    collection = get_collection('applications')

    print(f'\n🌱 Seeding {num_applications} applications...')

    applications = []

    # Generate applications spread over last 90 days
    for i in range(num_applications):
        days_ago = random.randint(1, 90)
        app = generate_application(user.id, days_ago)
        applications.append(app)

    # Insert all applications
    result = collection.insert_many(applications)

    print(f'✅ Created {len(result.inserted_ids)} applications')

    # Print summary
    statuses = {}
    for app in applications:
        status = app['application']['status']
        statuses[status] = statuses.get(status, 0) + 1

    print('\n📊 Status Summary:')
    for status, count in sorted(statuses.items()):
        print(f'   {status}: {count}')


def main():
    """Main seeding function."""
    print('=' * 60)
    print('JOB APPLICATION TRACKER - DATA SEEDING')
    print('=' * 60)

    # Create/get user
    user = create_sample_user()

    # Check existing applications
    collection = get_collection('applications')
    existing = collection.count_documents({'user_id': user.id})

    if existing > 0:
        print(f'\n⚠️  Found {existing} existing applications')
        response = input('Delete existing and reseed? (yes/no): ')
        if response.lower() == 'yes':
            collection.delete_many({'user_id': user.id})
            print('✅ Deleted existing applications')
        else:
            print('❌ Seeding cancelled')
            return

    # Seed applications
    num_apps = int(
        input('\nHow many applications to create? (default 50): ') or 50)
    seed_applications(user, num_apps)

    print('\n' + '=' * 60)
    print('✅ SEEDING COMPLETED!')
    print('=' * 60)
    print(f'\nUser credentials:')
    print(f'  Email: demo@example.com')
    print(f'  Password: DemoPass123!')
    print(f'\nYou can now:')
    print(f'  1. Login with these credentials')
    print(f'  2. View applications: GET /api/applications/')
    print(f'  3. View analytics: GET /api/analytics/dashboard/')
    print('=' * 60)


if __name__ == '__main__':
    main()
