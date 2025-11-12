from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    phone_number = models.IntegerField(blank=True,help_text='add your mobile phone',null=True)
    company_name = models.CharField(max_length=100,blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ROLE_CHOICES = [
        ('client','Client'),
        ('admin','Admin'),
        ('super_admin','super_admin')
     ]
    role = models.CharField(max_length=20,null=False,blank=False,choices=ROLE_CHOICES,default='client')
    
    def __str__(self):
         return f'{self.username} {self.email}'

    def contact_info(self):
         return f'{self.username} {self.email} {self.phone_number}'
    
    def is_admin(self):
         if self.role == 'admin':
              return True
         else:
              return False
    
    def is_client(self):
         if self.role == 'client':
              return True
         else:
              return False
         
    def is_super_admin(self):
         if self.role == 'super_admin':
              return True
         else:
              return False
         
    def ads_count(self):
         return self.client_ads.count()
    
    def ads_belonging_for_this_client(self):
         return self.client_ads.all()
    
    def active_ads_for_this_client(self):
         return self.client_ads.filter(statue='active')

    def pending_ads_for_this_client(self):
         return self.client_ads.filter(statue='pending')
    
    def approved_ads_for_this_client(self):
         return self.client_ads.filter(statue='approved')
    
    def rejected_ads_for_this_client(self):
         return self.client_ads.filter(statue='rejected')
    

    def boards_belonging_to_this_owner(self):
         if self.is_admin()==True or self.is_super_admin()==True:
               return self.client_boards.all()

    def add_board(self,username,location,width,height):
         from boards.models import Board
         if self.is_admin() == False:
              raise ValueError('Only admins can create boards')
         else:
              return Board.objects.create(
                    username = username,
                    location = location,
                    width = width,
                    height = height,
                    admin = self
          )
    
    def ownership_management(self,board,user):
         from boards.models import Board
         if self.is_super_admin():
               if user.is_admin():
                    board.admin = user
                    board.save()
                    return('ownership submitted successfully')
               else:
                    raise ValueError(f'this user{user.username} is not admin')


    def transfer_ownership_between_admins(self,board,user):
         from boards.models import Board        
         if self.is_super_admin():
              if user.is_admin():
                   board.admin = user
                   board.save()
                   return('ownership has been transferred correctly')
              else:
                   raise ValueError(f'this user {user.username}is not an admin')     
     
   
    def create_ad(self, content, title):
          from ads.models import Ad
          import os

          if not self.is_client():
               raise PermissionError("Only clients can create ads.")

          if not content:
               raise ValidationError("No file uploaded.")

          max_size = 50 * 1024 * 1024  # bytes
          if content.size > max_size:
               raise ValidationError("File should not surpass 50MB.")
          
          ad = Ad(content=content,title=title,client=self)
          ad.detect_type()
          ad.save()




    def _link_ad_to_boards(self,ad,board):
           from ads.models import Ad
           from boards.models import Board
           if not isinstance(board,(list)):
               boards = [board]
           else :
               boards = board
           for  b in boards :
                    ad.boards.add(b)
                    print (f'{ad} added successfully to the board {b}')            
   
   
    def add_ad(self,ad,board):
          if self.is_client() and self == ad.client:
               self._link_ad_to_boards(ad,board)
                   


    def assign_ad(self,ad,board):
          if self.is_admin() or self.is_super_admin():
                self._link_ad_to_boards(ad,board)        
                              
    
    
    def filter_ads(self,statue=None,media_type=None,board=None):
          if statue == None:
                         statuses=[]
          elif not isinstance(statue,(list)):
                    statuses=[statue]
          else:
                    statuses=statue
          if media_type == None:
                    media_types=[]
          elif not isinstance(media_type,(list)):
                    media_types=[media_type]
          else:
                    media_types = media_type
         
          if self.role=='client':
                 if len(statuses)==0 and len(media_types)==0:
                    return self.client_ads.all()
                 elif len(statuses)!=0 and len(media_types)==0:
                    return self.client_ads.filter(statue__in=statuses)
                 elif len(media_types)!=0 and len (statuses)==0:
                    return self.client_ads.filter(media_type__in=media_types)     
                 else:   
                    return self.client_ads.filter(media_type__in=media_types,statue__in=statuses )
                 
          elif self.role =='admin':
              if board == None:
                   raise ValidationError('select a board first')
              elif board !=None:
                   if board.admin != self:
                        raise ValidationError('you can not select a board you don´t own')
                   else:
                         if len(statuses)==0 and len(media_types)==0:
                              return board.board_ads.all()
                         elif len(statuses)!=0 and len(media_types)==0:
                              return board.bord_ads.filter(statue__in=statuses)
                         elif len(media_types)!=0 and len (statuses)==0:
                              return board.board_ads.filter(media_type__in=media_types)
                         else:
                              return board.board_ads.filter(statue__in=statuses,media_type__in=media_types)
                             
          else:
               from ads.models import Ad
               if len(statuses)==0 and len(media_types)==0:
                         return  Ad.objects.all()
               elif len(statuses)!=0 and len(media_types)==0:
                         return Ad.objects.filter(statue__in=statuses)
               elif len(media_types)!=0 and len (statuses)==0:
                         return Ad.objects.filter(media_type__in=media_types)
               else:
                         return Ad.objects.filter(statue__in=statuses,media_type__in=media_types)
    
    
    def filter_boards(self,location=None,size=None):
     if location==None:
          locations=[]
     elif not isinstance(location,(list)):
          locations=[location]
     else:
          locations=location
     if size == None:
          sizes =[]
     elif not isinstance(size,(list)):
          sizes = [size]
     else:
          sizes = size

     if self.role == 'client' or self.role=='super_admin':
               from boards.models import Board
               boards = Board.objects.all()
               if len (locations)==0 and len (sizes)==0:
                    return boards
               elif len (locations) !=0 and len(sizes)==0:
                    return boards.filter(location__in=locations)
               elif len(sizes)!=0 and len(locations)==0:
                    return boards.filter(size__in=sizes)
               else:
                         return boards.filter(location__in=locations,size__in=sizes)
     else:
               if len(locations)==0 and len(sizes)==0:
                     return self.owner_boards.all()
               elif len(locations)!=0 and len(sizes)==0:
                     return self.owner_boards.filter(location__in=locations)
               elif len(sizes)!=0 and len(locations)==0:
                     return self.owner_boards.filter(size__in=sizes)
               else:
                     return self.owner_boards.filter(size__in=sizes,location__in=location)
               

                   
    
     