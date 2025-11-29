"""
Analytics service for generating insights from application data.
"""

from datetime import datetime, timedelta
from collections import defaultdict
from config.mongodb import get_collection


class AnalyticsService:
    """Service class for analytics operations."""

    def __init__(self):
        self.collection = get_collection('applications')

    def get_dashboard_stats(self, user_id):
        """Get comprehensive dashboard statistics."""
        # Total applications
        total = self.collection.count_documents({'user_id': user_id})

        # Status breakdown
        status_pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$application.status',
                'count': {'$sum': 1}
            }}
        ]
        status_breakdown = {}
        for result in self.collection.aggregate(status_pipeline):
            status_breakdown[result['_id']] = result['count']

        # Calculate success rate (offers / total)
        offers = status_breakdown.get(
            'offer', 0) + status_breakdown.get('accepted', 0)
        success_rate = (offers / total * 100) if total > 0 else 0

        # Response rate (not rejected / total)
        rejected = status_breakdown.get('rejected', 0)
        withdrawn = status_breakdown.get('withdrawn', 0)
        response_rate = ((total - rejected - withdrawn) /
                         total * 100) if total > 0 else 0

        # Applications in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent = self.collection.count_documents({
            'user_id': user_id,
            'created_at': {'$gte': thirty_days_ago}
        })

        # Average days in pipeline
        avg_days = self._calculate_average_days(user_id)

        # Top companies
        top_companies = self._get_top_companies(user_id, limit=5)

        # Top sources
        top_sources = self._get_top_sources(user_id)

        return {
            'total_applications': total,
            'status_breakdown': status_breakdown,
            'success_rate': round(success_rate, 2),
            'response_rate': round(response_rate, 2),
            'applications_last_30_days': recent,
            'average_days_in_pipeline': avg_days,
            'top_companies': top_companies,
            'top_sources': top_sources
        }

    def get_applications_over_time(self, user_id, period='month'):
        """Get application counts over time."""
        if period == 'month':
            group_by = {
                'year': {'$year': '$created_at'},
                'month': {'$month': '$created_at'}
            }
            sort_by = [('_id.year', 1), ('_id.month', 1)]
        elif period == 'week':
            group_by = {
                'year': {'$year': '$created_at'},
                'week': {'$week': '$created_at'}
            }
            sort_by = [('_id.year', 1), ('_id.week', 1)]
        else:  # day
            group_by = {
                'year': {'$year': '$created_at'},
                'month': {'$month': '$created_at'},
                'day': {'$dayOfMonth': '$created_at'}
            }
            sort_by = [('_id.year', 1), ('_id.month', 1), ('_id.day', 1)]

        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': group_by,
                'count': {'$sum': 1}
            }},
            {'$sort': dict(sort_by)}
        ]

        results = list(self.collection.aggregate(pipeline))

        # Format results
        formatted = []
        for result in results:
            if period == 'month':
                label = f"{result['_id']['year']}-{result['_id']['month']:02d}"
            elif period == 'week':
                label = f"{result['_id']['year']}-W{result['_id']['week']:02d}"
            else:
                label = f"{result['_id']['year']}-{result['_id']['month']:02d}-{result['_id']['day']:02d}"

            formatted.append({
                'period': label,
                'count': result['count']
            })

        return formatted

    def get_success_rate_over_time(self, user_id):
        """Calculate success rate by month."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': {
                    'year': {'$year': '$created_at'},
                    'month': {'$month': '$created_at'},
                    'status': '$application.status'
                },
                'count': {'$sum': 1}
            }},
            {'$sort': {'_id.year': 1, '_id.month': 1}}
        ]

        results = list(self.collection.aggregate(pipeline))

        # Group by month
        monthly_data = defaultdict(lambda: {'total': 0, 'success': 0})

        for result in results:
            year = result['_id']['year']
            month = result['_id']['month']
            status = result['_id']['status']
            count = result['count']

            key = f"{year}-{month:02d}"
            monthly_data[key]['total'] += count

            if status in ['offer', 'accepted']:
                monthly_data[key]['success'] += count

        # Calculate rates
        formatted = []
        for period, data in sorted(monthly_data.items()):
            rate = (data['success'] / data['total']
                    * 100) if data['total'] > 0 else 0
            formatted.append({
                'period': period,
                'success_rate': round(rate, 2),
                'total': data['total'],
                'success': data['success']
            })

        return formatted

    def get_skills_demand(self, user_id):
        """Analyze which skills are most demanded in job postings."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$unwind': '$requirements.skills_required'},
            {'$group': {
                '_id': '$requirements.skills_required',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}},
            {'$limit': 20}
        ]

        results = list(self.collection.aggregate(pipeline))

        return [
            {'skill': result['_id'], 'count': result['count']}
            for result in results
        ]

    def get_application_timeline_analysis(self, user_id):
        """Analyze timeline and interview stages."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$unwind': '$timeline'},
            {'$group': {
                '_id': '$timeline.event_type',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]

        results = list(self.collection.aggregate(pipeline))

        return [
            {'event_type': result['_id'], 'count': result['count']}
            for result in results
        ]

    def get_salary_insights(self, user_id):
        """Get salary statistics from applications."""
        pipeline = [
            {'$match': {
                'user_id': user_id,
                'job.salary_min': {'$exists': True, '$ne': None}
            }},
            {'$group': {
                '_id': None,
                'avg_min': {'$avg': '$job.salary_min'},
                'avg_max': {'$avg': '$job.salary_max'},
                'min_salary': {'$min': '$job.salary_min'},
                'max_salary': {'$max': '$job.salary_max'},
                'count': {'$sum': 1}
            }}
        ]

        results = list(self.collection.aggregate(pipeline))

        if not results:
            return {
                'average_min': 0,
                'average_max': 0,
                'lowest': 0,
                'highest': 0,
                'total_with_salary': 0
            }

        data = results[0]
        return {
            'average_min': round(data.get('avg_min', 0)),
            'average_max': round(data.get('avg_max', 0)),
            'lowest': data.get('min_salary', 0),
            'highest': data.get('max_salary', 0),
            'total_with_salary': data.get('count', 0)
        }

    def get_response_time_analysis(self, user_id):
        """Analyze how long it takes companies to respond."""
        applications = list(self.collection.find(
            {'user_id': user_id},
            {'application.applied_date': 1, 'timeline': 1, 'company.name': 1}
        ))

        response_times = []

        for app in applications:
            applied_date = app.get('application', {}).get('applied_date')
            timeline = app.get('timeline', [])

            if not applied_date or not timeline:
                continue

            # Find first response (first timeline event after application)
            for event in sorted(timeline, key=lambda x: x.get('date', datetime.min)):
                event_date = event.get('date')
                if event_date and event_date > applied_date:
                    days = (event_date - applied_date).days
                    response_times.append({
                        'company': app.get('company', {}).get('name', 'Unknown'),
                        'days': days
                    })
                    break

        if not response_times:
            return {
                'average_days': 0,
                'fastest': 0,
                'slowest': 0,
                'total_responses': 0
            }

        days_list = [r['days'] for r in response_times]

        return {
            'average_days': round(sum(days_list) / len(days_list), 1),
            'fastest': min(days_list),
            'slowest': max(days_list),
            'total_responses': len(response_times)
        }

    def _calculate_average_days(self, user_id):
        """Calculate average days applications stay in pipeline."""
        applications = list(self.collection.find(
            {'user_id': user_id},
            {'created_at': 1, 'application.status': 1}
        ))

        if not applications:
            return 0

        total_days = 0
        count = 0

        for app in applications:
            created = app.get('created_at')
            status = app.get('application', {}).get('status')

            if created:
                # If still in pipeline, calculate days until now
                if status not in ['offer', 'accepted', 'rejected', 'withdrawn']:
                    days = (datetime.utcnow() - created).days
                    total_days += days
                    count += 1

        return round(total_days / count) if count > 0 else 0

    def _get_top_companies(self, user_id, limit=5):
        """Get companies with most applications."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$company.name',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}},
            {'$limit': limit}
        ]

        results = list(self.collection.aggregate(pipeline))

        return [
            {'company': result['_id'], 'count': result['count']}
            for result in results
        ]

    def _get_top_sources(self, user_id):
        """Get top application sources."""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$application.source',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]

        results = list(self.collection.aggregate(pipeline))

        return [
            {'source': result['_id'] or 'Unknown', 'count': result['count']}
            for result in results
        ]
