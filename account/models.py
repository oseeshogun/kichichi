from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profiles/user_{0}/{1}'.format(instance.user.username, filename)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    profession = models.CharField(max_length=250, null=True, blank=True)
    profil = models.ImageField(default="profiles/default/profil.png")
    actived = models.BooleanField(default=False)
    langue = models.CharField(max_length=5, default='fr')

    def __str__(self):
        return self.user.username

    @property
    def is_bithday(self):
        if self.birthday == datetime.today:
            return True
        return False

    def is_confirmed(self):
        return self.actived


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followings = models.ManyToManyField(User, related_name='is_following_me', blank=True)

    def __str__(self):
        return self.user.username


class User_groups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    members = models.ManyToManyField(User, related_name='group', blank=True)

    def __str__(self):
        name = 'user: {0}, name: {1}'.format(self.user.username, self.name)
        return name

    def vote(self):
        return self.vote_to_add


class Publication(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    launched = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='Publication/%Y/%m/%d/', null=True, blank=True)
    text = models.CharField(max_length=200, null=True, blank=True)
    likes_number = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, related_name='likers_related', blank=True)
    inappropriate = models.BooleanField(default=False)
    inappropriate_clicks = models.IntegerField(default=0)
    inappropriate_clickers = models.ManyToManyField(User, related_name='inappropriate_clikers', blank=True)
    viewers_group = models.ForeignKey(User_groups, on_delete=models.CASCADE, null=True, blank=True)
    public = models.BooleanField(default=False)
    for_followers = models.BooleanField(default=False)

    def __str__(self):
        tx = str(self.text)
        return tx

    def publishedby(self):
        return self.publisher.username

    def profil(self):
        return self.publisher.profile.profil

    def size(self):
        size_octet = self.file.size
        size_mo = (size_octet / 1050030)
        size_mo = float(size_mo)
        return '%.01f' % size_mo

    def is_file(self):
        if self.file.name.lower().endswith('jpg'):
            return False
        return True

    class Meta:
        ordering = ['-launched']


class Comments(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    posttime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posttime']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField()
    important = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sender")
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification

    class Meta:
        ordering = ['-send_time']
