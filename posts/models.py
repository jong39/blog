from django.db import models
#from django.core.urlresolvers import reverse
# Create your models here.
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

# Below are Type of model Manager
#Post.objects.all()
#Post.objects.create(user=user, title='test')
class PostManager(models.Manager): #override models itself
    def active(self, *args, **kwargs):
        # Post.objects.all() is same as #super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length = 120)
    # slug = models.SlugField(unique=True) #Required field
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, 
        width_field="width_field", 
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    publish = models.DateField(auto_now=False, auto_now_add=False)
    draft = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:mydetail", kwargs={"id": self.id})
        #return "%s/" %(self.id)

    class Meta: #anything to do with not fields
        ordering = ["-timestamp", "-updated"]

    def get_lower(self):
        content = self.content
        lower_content = content.lower()
        return lower_content
        

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

# pre_save.connect(pre_save_post_receiver, sender=Post)






