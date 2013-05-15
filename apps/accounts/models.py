from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def save_image(instance, filename):
    import os
    from django.conf import settings
    extn = os.path.splitext(filename)[1]
    path = os.path.join(settings.MEDIA_ROOT, 'user_image', 'user_%x%s' % ((random.randrange(256**15) % 1000000), extn))



class UserProfile(models.Model):
    user = models.ForeignKey(User)
    follows = models.ManyToManyField(User, related_name='u+')
    # image = models.ImageField(upload_to='/user/', max_length=255, height_field='height', width_field='width')
    # width   = models.IntegerField()
    # height  = models.IntegerField()
    date_of_birth = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "<UserProfile for {name}>".format(name=self.user.username)

    def get_image_url(self):
        return self.image.url

    def get_image_size(self):
        return (self.width, self.height)

    def add_following(self, user):
        self.follows.add(user)
        self.save()
        return

    def get_user_details(self):
        result = {
            'username': self.user.username,
            'email': self.user.email,
            'date_of_birth': self.date_of_birth,
            # 'image_url': self.image.url,
            'following_count': self.follows.count(),
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        }
        return result
