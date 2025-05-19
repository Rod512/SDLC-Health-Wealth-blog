from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from account.models import User
from blog_app.models import Blog


@receiver(post_save, sender=User)
def permission_of_user_creation(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "admin":
            perms = ['can_edit_blog', 'can_view_blog', 'can_edit_category']
        elif instance.user_type == "user":
            perms = ['can_view_blog']
        else:
            perms = []

        for codename in perms:
            try:
                permission = Permission.objects.get(codename=codename)
                instance.user_permissions.add(permission)
            except Permission.DoesNotExist:
                continue


