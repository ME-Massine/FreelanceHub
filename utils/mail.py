from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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


def send_project_deadline_alert(project):
    """
    Send alert when project is approaching deadline
    Triggered when project deadline is within alert threshold (e.g., 2 days)
    """
    if hasattr(project, 'is_approaching_deadline') and project.is_approaching_deadline():
        # Send to both client and assigned freelancer
        recipients = []
        if project.client.email:
            recipients.append(project.client.email)
        if hasattr(project,
                   'assigned_freelancer') and project.assigned_freelancer and project.assigned_freelancer.email:
            recipients.append(project.assigned_freelancer.email)

        if recipients:
            subject = f'Deadline Alert: "{project.title}"'
            message = (f"Your project is approaching its deadline.\n\n"
                       f"Project: {project.title}\n"
                       f"Deadline: {project.deadline.strftime('%Y-%m-%d %H:%M')}\n"
                       f"Current Status: {project.get_status_display()}\n\n"
                       f"Please ensure all deliverables are completed on time.")

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=True,
            )
            return True
    return False


def send_payment_due_notification(project):
    """
    Send notification when payment is due for completed project
    Triggered when project is marked as completed but payment is pending
    """
    if project.status == 'completed' and not project.is_paid:
        if project.client.email:
            subject = f'Payment Due: "{project.title}"'
            message = (f"Payment is due for your completed project.\n\n"
                       f"Project: {project.title}\n"
                       f"Freelancer: {project.assigned_freelancer.get_full_name()}\n"
                       f"Amount Due: ${project.budget}\n"
                       f"Completed Date: {project.completion_date.strftime('%Y-%m-%d')}\n\n"
                       f"Please process the payment through your dashboard.")

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [project.client.email],
                fail_silently=True,
            )
            return True
    return False


def send_freelancer_application_status(application, status):
    """
    Send notification to freelancer about their application status
    Triggered when client accepts/rejects a proposal
    """
    if application.freelancer.email:
        if status == 'accepted':
            subject = f'Congratulations! Your proposal was accepted for "{application.project.title}"'
            message = (f"Great news! Your proposal has been accepted.\n\n"
                       f"Project: {application.project.title}\n"
                       f"Client: {application.project.client.get_full_name()}\n"
                       f"Budget: ${application.budget}\n"
                       f"Deadline: {application.project.deadline.strftime('%Y-%m-%d')}\n\n"
                       f"Login to your dashboard to start working on the project.")
        else:
            subject = f'Update on your proposal for "{application.project.title}"'
            message = (f"Thank you for your interest in the project.\n\n"
                       f"Project: {application.project.title}\n"
                       f"Unfortunately, your proposal was not selected this time.\n\n"
                       f"Don't worry! Keep applying to other projects that match your skills.")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.freelancer.email],
            fail_silently=True,
        )
        return True
    return False


def send_low_rating_alert(user):
    """
    Send alert when user's rating drops below threshold
    Triggered when average rating falls below acceptable level (e.g., 3.0)
    """
    if hasattr(user, 'get_average_rating') and user.get_average_rating() < 3.0:
        if user.email:
            subject = 'Account Performance Alert'
            message = (f"Your account rating needs attention.\n\n"
                       f"Current Rating: {user.get_average_rating():.1f}/5.0\n"
                       f"This may affect your visibility to potential clients.\n\n"
                       f"Tips to improve:\n"
                       f"- Communicate clearly with clients\n"
                       f"- Deliver work on time\n"
                       f"- Follow project requirements carefully\n\n"
                       f"Contact support if you need assistance.")

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            return True
    return False


def send_milestone_completion_notification(milestone):
    """
    Send notification when a project milestone is completed
    Triggered when freelancer marks a milestone as complete
    """
    if milestone.project.client.email:
        subject = f'Milestone Completed: "{milestone.project.title}"'
        message = (f"A milestone has been completed for your project.\n\n"
                   f"Project: {milestone.project.title}\n"
                   f"Milestone: {milestone.title}\n"
                   f"Freelancer: {milestone.project.assigned_freelancer.get_full_name()}\n"
                   f"Completion Date: {milestone.completion_date.strftime('%Y-%m-%d')}\n\n"
                   f"Please review the deliverable and provide feedback.")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [milestone.project.client.email],
            fail_silently=True,
        )
        return True
    return False


def send_profile_completion_reminder(user):
    """
    Send reminder to complete profile for better visibility
    Triggered when profile completion is below threshold (e.g., 70%)
    """
    if hasattr(user, 'get_profile_completion') and user.get_profile_completion() < 70:
        if user.email:
            subject = 'Complete Your Profile for Better Opportunities'
            message = (f"Your profile is {user.get_profile_completion()}% complete.\n\n"
                       f"Complete your profile to:\n"
                       f"- Increase visibility to clients\n"
                       f"- Build trust and credibility\n"
                       f"- Showcase your skills and experience\n\n"
                       f"Missing sections may include:\n"
                       f"- Profile photo\n"
                       f"- Skills and expertise\n"
                       f"- Portfolio samples\n"
                       f"- Professional description\n\n"
                       f"Complete your profile now to start getting more projects!")

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            return True
    return False