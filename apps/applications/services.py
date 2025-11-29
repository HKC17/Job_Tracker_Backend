"""
Application service layer for MongoDB operations.
"""

from bson import ObjectId
from datetime import datetime
from config.mongodb import get_collection


class ApplicationService:
    """Service class for application CRUD operations."""

    def __init__(self):
        self.collection = get_collection('applications')

    def create_application(self, user_id, data):
        """Create a new job application."""
        application = {
            'user_id': user_id,
            'company': data.get('company', {}),
            'job': data.get('job', {}),
            'application': {
                'applied_date': data.get('application', {}).get('applied_date', datetime.utcnow()),
                'source': data.get('application', {}).get('source', ''),
                'status': data.get('application', {}).get('status', 'applied'),
                'resume_version': data.get('application', {}).get('resume_version', ''),
                'cover_letter': data.get('application', {}).get('cover_letter', ''),
                'referral_name': data.get('application', {}).get('referral_name', ''),
            },
            'requirements': data.get('requirements', {}),
            'timeline': data.get('timeline', []),
            'attachments': data.get('attachments', []),
            'notes': data.get('notes', ''),
            'is_favorite': data.get('is_favorite', False),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }

        result = self.collection.insert_one(application)
        application['_id'] = result.inserted_id
        return application

    def get_application(self, application_id, user_id):
        """Get a single application by ID."""
        return self.collection.find_one({
            '_id': ObjectId(application_id),
            'user_id': user_id
        })

    def get_applications(self, user_id, filters=None, skip=0, limit=20):
        """Get all applications for a user with optional filters."""
        query = {'user_id': user_id}

        if filters:
            if filters.get('status'):
                query['application.status'] = filters['status']
            if filters.get('company'):
                query['company.name'] = {
                    '$regex': filters['company'], '$options': 'i'}
            if filters.get('job_title'):
                query['job.title'] = {
                    '$regex': filters['job_title'], '$options': 'i'}
            if filters.get('is_favorite') is not None:
                query['is_favorite'] = filters['is_favorite']

        total = self.collection.count_documents(query)
        applications = list(
            self.collection.find(query)
            .sort('created_at', -1)
            .skip(skip)
            .limit(limit)
        )

        return {
            'total': total,
            'applications': applications
        }

    def update_application(self, application_id, user_id, data):
        """Update an application."""
        data['updated_at'] = datetime.utcnow()

        result = self.collection.update_one(
            {'_id': ObjectId(application_id), 'user_id': user_id},
            {'$set': data}
        )

        if result.modified_count > 0:
            return self.get_application(application_id, user_id)
        return None

    def delete_application(self, application_id, user_id):
        """Delete an application."""
        result = self.collection.delete_one({
            '_id': ObjectId(application_id),
            'user_id': user_id
        })
        return result.deleted_count > 0

    def add_timeline_event(self, application_id, user_id, event_data):
        """Add a timeline event to an application."""
        event = {
            'date': event_data.get('date', datetime.utcnow()),
            'event_type': event_data.get('event_type', ''),
            'title': event_data.get('title', ''),
            'notes': event_data.get('notes', ''),
            'interviewer_name': event_data.get('interviewer_name', ''),
            'interview_type': event_data.get('interview_type', ''),
        }

        result = self.collection.update_one(
            {'_id': ObjectId(application_id), 'user_id': user_id},
            {
                '$push': {'timeline': event},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )

        return result.modified_count > 0

    def update_status(self, application_id, user_id, new_status, notes=None):
        """Update application status and add timeline event."""
        # Get current application
        app = self.get_application(application_id, user_id)
        if not app:
            return None

        old_status = app.get('application', {}).get('status', 'unknown')

        # Create timeline event
        event = {
            'date': datetime.utcnow(),
            'event_type': 'status_change',
            'title': f'Status changed from {old_status} to {new_status}',
            'notes': notes or '',
        }

        # Update status and add timeline event
        result = self.collection.update_one(
            {'_id': ObjectId(application_id), 'user_id': user_id},
            {
                '$set': {
                    'application.status': new_status,
                    'updated_at': datetime.utcnow()
                },
                '$push': {'timeline': event}
            }
        )

        if result.modified_count > 0:
            return self.get_application(application_id, user_id)
        return None

    def get_statistics(self, user_id):
        """Get application statistics for a user."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$application.status',
                'count': {'$sum': 1}
            }}
        ]

        status_counts = {}
        for result in self.collection.aggregate(pipeline):
            status_counts[result['_id']] = result['count']

        total = self.collection.count_documents({'user_id': user_id})

        return {
            'total_applications': total,
            'status_breakdown': status_counts
        }

    def search_applications(self, user_id, search_term):
        """Search applications by company name, job title, or notes."""
        query = {
            'user_id': user_id,
            '$or': [
                {'company.name': {'$regex': search_term, '$options': 'i'}},
                {'job.title': {'$regex': search_term, '$options': 'i'}},
                {'notes': {'$regex': search_term, '$options': 'i'}},
            ]
        }

        return list(self.collection.find(query).sort('created_at', -1))
