
from django.db import models
from django.conf import settings 


# class Project(models.Model):
#     class Meta:
#         constraints=[
#             models.UniqueConstraint(fields=['member','name'],name='Unique combo of user and project')
#         ]
#     member=models.ManyToManyField(settings.AUTH_USER_MODEL)

#     name=models.CharField(max_length=100)

#     max_members=models.PositiveIntegerField()

#     STATUS_CHOICES = [[0, 'To be started'],[1, 'In progress'],[2, 'Completed']]
    
#     status = models.IntegerField(
#         choices=STATUS_CHOICES,
#         default=0
#     )

#     def __str(self):
#         return self.name
    
# class Project(models.Model):
#     class Meta:
#         constraints=[
#             models.UniqueConstraint(fields=['member','name'],name='Unique combo of user and project')
#         ]
#     member=models.ManyToManyField(settings.AUTH_USER_MODEL)

#     name=models.CharField(max_length=100)

#     max_members=models.PositiveIntegerField()

#     STATUS_CHOICES = [[0, 'To be started'],[1, 'In progress'],[2, 'Completed']]
    
#     status = models.IntegerField(
#         choices=STATUS_CHOICES,
#         default=0
#     )

#     def __str(self):
#         return self.name
    

class Project(models.Model):
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMember',
        related_name='project'
    )
    name = models.CharField(max_length=100)
    max_members = models.PositiveIntegerField()

    STATUS_CHOICES = [
        [0, 'To be started'],
        [1, 'In progress'],
        [2, 'Completed']
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='project_membership')

    class Meta:
        unique_together = ('project', 'member')

    def __str__(self):
        return f"{self.member.first_name} in {self.project.name}"



# class ProjectMember(models.Model):
#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE
#     )
#     member = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )

#     def __str(self):
#         return f"{self.project.name} by {self.member.first_name}"

"""
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """

"""
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)

        Add string representation for this model with project name.
    """