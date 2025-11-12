from django.db import models
from user.models import User
from django.core.exceptions import ValidationError


class Ad(models.Model):
    ad_id = models.AutoField(primary_key=True)
    content = models.FileField(upload_to='ads/',blank=False,null=False)
    client = models.ForeignKey(User,on_delete=models.CASCADE,related_name='client_ads',
                               null=False,blank=False)
    boards = models.ManyToManyField('boards.Board',related_name='board_ads')
    title = models.CharField(blank=True,null=True,help_text="Ad description",max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    Statue_choices = [
                    ('pending','Pending'),
                     ('approved','Approved'),
                     ('rejected','Rejected'),
                     ('active','Active'),
                    ]
    statue = models.CharField(choices=Statue_choices,null=False,blank=False,
                                default='pending')
    
    media_type = models.CharField(max_length=10,editable=False,blank=True)                          

    def detect_type (self):
        import os
        file_type = os.path.splitext(self.content.name)[1].lower()
        allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        allowed_video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
        if file_type  in allowed_image_extensions:
            self.media_type = 'image'
            return
        elif file_type in allowed_video_extensions:
            self.media_type = 'video'
            return  
        else :
            raise ValidationError('unsupported media type')
            
    def save(self, *args, **kwargs):
            self.detect_type()
            super().save(*args, **kwargs)
        
   
    def ad_board(self):
        return self.boards
    
    def client_who_has_this_ad(self):
        return self.client

    def board_displaying_this_ad(self):
        return self.boards
    
    def ad_content(self):
        return self.content()
    
    def ad_type(self):
        return self.type()







class schedule(models.Model):
    start_time = models.DateTimeField(help_text="the time when the ad starts displaying")
    end_time = models.DateTimeField(help_text="the time when the ad stops displaying")
    ad = models.ForeignKey(Ad,on_delete=models.CASCADE)

    def ad_schedule():
        return 