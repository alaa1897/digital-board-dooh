from django.db import models
from user.models import User
from django.core.exceptions import ValidationError


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,help_text='board name')
    location = models.CharField(max_length=100,help_text='physical location of the board')
    
    width = models.FloatField(help_text='board width in cm',blank=False,null=False)
    height = models.FloatField(help_text='board height in cm',blank=False,null=False)
    def verify_width_height(self):
        if self.width<=0:
            raise ValidationError('width must be positive')
        if self.height<=0:
            raise ValidationError('height must be positive')

    size = models.CharField(max_length=10,editable=False,null=True)
    def detect_size(self):
        if (self.width * self.height)<5000:
            self.size= 'small'
        elif 120000>=self.width *self.height>=5000:
            self.size ='medium'
        elif self.width * self.height>120000:
            self.size = 'big'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner_boards'
                              ,null=False,blank=False,)

    def save(self,*args,**kwargs):
        self.verify_width_height()
        self.detect_size()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    def active_ads_on_this_board(self):
        return self.ads.filter(statues = 'active')
        
    def pending_ads_on_this_board(self):
        return self.ads.filter(statues = 'pending')
    
    def approved_ads_on_this_board(self):
        return self.ads.filter(statues = 'approved')
    
    def rejected_ads_on_this_board(self):
        return self.ads.filter(statues ='rejected')

    def board_owner(self):
        return self.owner
    
    