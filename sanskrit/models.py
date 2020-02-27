from django.db import models
from django.contrib.auth.models import User

class SanskritLessons(models.Model):
    lesson_name = models.CharField(max_length=20,primary_key=True)       
    q_number = models.IntegerField(default=0)
    # question = models.CharField(max_length=20)

    def __str__(self):
        return self.lesson_name
    

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_key = models.ForeignKey(SanskritLessons,default=0,on_delete=models.CASCADE)     
    completed = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.user.username)



class SanskritQuestions(models.Model):
    Q_TYPE_CHOICES=(
        ('t','typing'),
        ('s','select'),
        ('j','jump'),
    )
    
    key_question = models.ForeignKey(SanskritLessons,on_delete=models.CASCADE)
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=50,default="",null=False)
    q_type = models.CharField(choices=Q_TYPE_CHOICES,null=False,max_length=10)
    # q_select = models.BooleanField(default=False,null=False)
    # q_jump = models.BooleanField(default=False,null=False)
    

    def __str__(self):
        return self.question

class SanskritAnswers(models.Model):
    key_answer = models.ForeignKey(SanskritQuestions,on_delete=models.CASCADE)    
    ans_choice = models.CharField(max_length=50,null=False)
    ans_image = models.ImageField(upload_to='pics/',default='design.png')

    def __str__(self):
        return self.ans_choice

# class SanskritJumpAnswers(models.Model):
#     key_answer = models.ForeignKey(SanskritQuestions,on_delete=models.CASCADE)    
#     ans_ = models.CharField(max_length=50,null=False)
   

#     def __str__(self):
#         return self.ans_choice