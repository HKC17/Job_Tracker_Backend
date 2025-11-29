"""
Companies service layer for MongoDB operations.
"""

from bson import ObjectId
from datetime import datetime
from config.mongodb import get_collection


class CompanyService:
    """Service class for company operations."""

    def __init__(self):
        self.collection = get_collection('companies')
        self.applications_collection = get_collection('applications')

    def create_company(self, user_id, data):
        """Create a new company."""
        company = {
            'user_id': user_id,
            'name': data.get('name'),
            'website': data.get('website', ''),
            'industry': data.get('industry', ''),
            'size': data.get('size', ''),
            'location': data.get('location', ''),
            'logo_url': data.get('logo_url', ''),
            'description': data.get('description', ''),
            'glassdoor_rating': data.get('glassdoor_rating'),
            'notes': data.get('notes', ''),
            'is_favorite': data.get('is_favorite', False),
            'tags': data.get('tags', []),
            'contact_info': data.get('contact_info', {}),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }

        result = self.collection.insert_one(company)
        company['_id'] = result.inserted_id
        return company

    def get_company(self, company_id, user_id):
        """Get a single company by ID."""
        return self.collection.find_one({
            '_id': ObjectId(company_id),
            'user_id': user_id
        })

    def get_company_by_name(self, name, user_id):
        """Get company by name."""
        return self.collection.find_one({
            'name': {'$regex': f'^{name}$', '$options': 'i'},
            'user_id': user_id
        })

    def get_companies(self, user_id, filters=None, skip=0, limit=20):
        """Get all companies for a user with optional filters."""
        query = {'user_id': user_id}

        if filters:
            if filters.get('industry'):
                query['industry'] = {
                    '$regex': filters['industry'], '$options': 'i'}
            if filters.get('location'):
                query['location'] = {
                    '$regex': filters['location'], '$options': 'i'}
            if filters.get('is_favorite') is not None:
                query['is_favorite'] = filters['is_favorite']
            if filters.get('tags'):
                query['tags'] = {'$in': filters['tags']}

        total = self.collection.count_documents(query)
        companies = list(
            self.collection.find(query)
            .sort('name', 1)
            .skip(skip)
            .limit(limit)
        )

        # Add application count for each company
        for company in companies:
            app_count = self.applications_collection.count_documents({
                'user_id': user_id,
                'company.name': company['name']
            })
            company['application_count'] = app_count

        return {
            'total': total,
            'companies': companies
        }

    def update_company(self, company_id, user_id, data):
        """Update a company."""
        data['updated_at'] = datetime.utcnow()

        result = self.collection.update_one(
            {'_id': ObjectId(company_id), 'user_id': user_id},
            {'$set': data}
        )

        if result.modified_count > 0:
            return self.get_company(company_id, user_id)
        return None

    def delete_company(self, company_id, user_id):
        """Delete a company."""
        result = self.collection.delete_one({
            '_id': ObjectId(company_id),
            'user_id': user_id
        })
        return result.deleted_count > 0

    def search_companies(self, user_id, search_term):
        """Search companies by name, industry, or location."""
        query = {
            'user_id': user_id,
            '$or': [
                {'name': {'$regex': search_term, '$options': 'i'}},
                {'industry': {'$regex': search_term, '$options': 'i'}},
                {'location': {'$regex': search_term, '$options': 'i'}},
            ]
        }

        companies = list(self.collection.find(query).sort('name', 1))

        # Add application count
        for company in companies:
            app_count = self.applications_collection.count_documents({
                'user_id': user_id,
                'company.name': company['name']
            })
            company['application_count'] = app_count

        return companies

    def autocomplete(self, user_id, prefix, limit=10):
        """Autocomplete company names."""
        query = {
            'user_id': user_id,
            'name': {'$regex': f'^{prefix}', '$options': 'i'}
        }

        companies = list(
            self.collection.find(
                query, {'name': 1, 'industry': 1, 'location': 1})
            .sort('name', 1)
            .limit(limit)
        )

        return companies

    def get_company_applications(self, company_id, user_id):
        """Get all applications for a specific company."""
        company = self.get_company(company_id, user_id)
        if not company:
            return None

        applications = list(
            self.applications_collection.find({
                'user_id': user_id,
                'company.name': company['name']
            }).sort('created_at', -1)
        )

        return {
            'company': company,
            'applications': applications
        }

    def get_company_stats(self, company_id, user_id):
        """Get statistics for a specific company."""
        company = self.get_company(company_id, user_id)
        if not company:
            return None

        # Total applications
        total = self.applications_collection.count_documents({
            'user_id': user_id,
            'company.name': company['name']
        })

        # Status breakdown
        pipeline = [
            {'$match': {
                'user_id': user_id,
                'company.name': company['name']
            }},
            {'$group': {
                '_id': '$application.status',
                'count': {'$sum': 1}
            }}
        ]

        status_breakdown = {}
        for result in self.applications_collection.aggregate(pipeline):
            status_breakdown[result['_id']] = result['count']

        # Average response time
        applications = list(self.applications_collection.find({
            'user_id': user_id,
            'company.name': company['name']
        }, {'application.applied_date': 1, 'timeline': 1}))

        response_times = []
        for app in applications:
            applied_date = app.get('application', {}).get('applied_date')
            timeline = app.get('timeline', [])

            if applied_date and timeline:
                for event in sorted(timeline, key=lambda x: x.get('date', datetime.min)):
                    event_date = event.get('date')
                    if event_date and event_date > applied_date:
                        days = (event_date - applied_date).days
                        response_times.append(days)
                        break

        avg_response_time = sum(response_times) / \
            len(response_times) if response_times else 0

        return {
            'company': company,
            'total_applications': total,
            'status_breakdown': status_breakdown,
            'average_response_time': round(avg_response_time, 1)
        }

    def sync_companies_from_applications(self, user_id):
        """Extract and create company entries from existing applications."""
        # Get unique companies from applications
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$company.name',
                'company': {'$first': '$company'}
            }}
        ]

        unique_companies = list(
            self.applications_collection.aggregate(pipeline))

        created_count = 0
        for item in unique_companies:
            company_name = item['_id']
            company_data = item['company']

            # Check if company already exists
            existing = self.get_company_by_name(company_name, user_id)

            if not existing:
                # Create new company
                self.create_company(user_id, company_data)
                created_count += 1

        return created_count

    def get_industry_breakdown(self, user_id):
        """Get breakdown of companies by industry."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$industry',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]

        results = list(self.collection.aggregate(pipeline))

        return [
            {'industry': result['_id'] or 'Unknown', 'count': result['count']}
            for result in results
        ]

    def get_top_companies_by_applications(self, user_id, limit=10):
        """Get companies with most applications."""
        # Get all companies
        companies = list(self.collection.find({'user_id': user_id}))

        # Count applications for each
        company_stats = []
        for company in companies:
            app_count = self.applications_collection.count_documents({
                'user_id': user_id,
                'company.name': company['name']
            })

            if app_count > 0:
                company_stats.append({
                    'company': company,
                    'application_count': app_count
                })

        # Sort by application count
        company_stats.sort(key=lambda x: x['application_count'], reverse=True)

        return company_stats[:limit]
