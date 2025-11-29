"""
File upload service for handling application attachments.
"""

import os
import uuid
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class FileUploadService:
    """Service for handling file uploads."""

    ALLOWED_EXTENSIONS = {
        'resume': ['.pdf', '.doc', '.docx', '.txt'],
        'document': ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def validate_file(file, file_type='document'):
        """Validate uploaded file."""
        errors = []

        # Check file size
        if file.size > FileUploadService.MAX_FILE_SIZE:
            errors.append(f'File size exceeds 5MB limit')

        # Check file extension
        file_ext = os.path.splitext(file.name)[1].lower()
        allowed_exts = FileUploadService.ALLOWED_EXTENSIONS.get(file_type, [])

        if file_ext not in allowed_exts:
            errors.append(
                f'File type {file_ext} not allowed. Allowed types: {", ".join(allowed_exts)}')

        return errors

    @staticmethod
    def save_file(file, user_id, file_type='document'):
        """Save uploaded file and return file info."""
        # Validate file
        errors = FileUploadService.validate_file(file, file_type)
        if errors:
            return None, errors

        # Generate unique filename
        file_ext = os.path.splitext(file.name)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"

        # Create file path: media/uploads/{user_id}/{file_type}/filename
        file_path = os.path.join('uploads', str(
            user_id), file_type, unique_filename)

        # Save file
        try:
            saved_path = default_storage.save(
                file_path, ContentFile(file.read()))

            # Return file info
            file_info = {
                'filename': file.name,
                'original_name': file.name,
                'file_path': saved_path,
                'file_url': f'/media/{saved_path}',
                'file_size': file.size,
                'file_type': file_ext[1:],  # Remove dot
                'uploaded_at': datetime.utcnow()
            }

            return file_info, None

        except Exception as e:
            return None, [f'Error saving file: {str(e)}']

    @staticmethod
    def delete_file(file_path):
        """Delete a file from storage."""
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                return True
            return False
        except Exception as e:
            print(f'Error deleting file: {str(e)}')
            return False

    @staticmethod
    def get_file_info(file_path):
        """Get information about a stored file."""
        try:
            if default_storage.exists(file_path):
                return {
                    'exists': True,
                    'size': default_storage.size(file_path),
                    'url': default_storage.url(file_path)
                }
            return {'exists': False}
        except Exception as e:
            return {'exists': False, 'error': str(e)}
