from django.core.mail import send_mail
from django.conf import settings

"""
Email notification utilities for FreelanceHub platform
Adapted from stock alert system to freelance marketplace notifications
"""


def send_project_proposal_notification(project, freelancer):
    """
    Send notification to client when a freelancer submits a proposal
    Triggered when a freelancer applies to a project
    """
    if project.client.email:
        subject = f'New Proposal for "{project.title}"'
        message = (f"A freelancer has submitted a proposal for your project.\n\n"
                   f"Project: {project.title}\n"
                   f"Freelancer: {freelancer.get_full_name()}\n"
                   f"Proposed Budget: ${freelancer.applications.filter(project=project).first().budget}\n\n"
                   f"Login to your dashboard to review the proposal.")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [project.client.email],
            fail_silently=True,
        )
        return True
    return False

