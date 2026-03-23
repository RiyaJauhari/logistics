from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Role(models.Model):
    roleId=models.CharField(
        max_length=64, unique=True, blank=False, null=False)
    roleName=models.CharField(
        max_length=64,  blank=False, null=False)
    roleDescription=models.CharField(
        max_length=64,  blank=True, null=True)
    
    class Meta:
        db_table = 'role'

    def __str__(self):
        return self.roleId

class User(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    userId = models.CharField(
        max_length=64, unique=True, blank=False, null=False,primary_key=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    middleName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipCode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.userId
       
class Order(models.Model):
    orderId = models.CharField(
        max_length=64, unique=True, blank=False, null=False,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, default="pending")  
    orderDate=models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.orderId
    
class Shipment(models.Model):
    shipmentId = models.CharField(
        max_length=64, unique=True, blank=False, null=False,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, default="pending")  
    shipmentDate=models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'shipment'

    def __str__(self):
        return self.shipmentId

class Transport(models.Model):
    transportId=models.CharField(
        max_length=64, unique=True, blank=False, null=False,primary_key=True)
    vehicle=models.CharField(
        max_length=64,  blank=False, null=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    driver=models.CharField(
        max_length=64,  blank=False, null=False)
    vehicleNumber=models.CharField(
        max_length=64,  blank=False, null=False)
    vehicleOwner=models.CharField(
        max_length=64,  blank=False, null=False)
    
    class Meta:
        db_table = 'transport'

    def __str__(self):
        return self.transportId
    
class Transactions(models.Model):
    pass
    class Meta:
        db_table = 'Transaction'

    def __str__(self):
        return self.transactionId
    
class Billing(models.Model):
    billId = models.CharField(
        max_length=64, unique=True, blank=False, null=False,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    billType=models.CharField(
        max_length=50, null=True,blank=True) 
    status = models.CharField(
        max_length=50, default="pending")  
    billDate=models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'billing'

    def __str__(self):
        return self.billingId

@receiver(post_save, sender=User)
def create_documents(sender, instance, created, **kwargs):
    if created:
        Role.objects.create(user=instance)
        Order.objects.create(user=instance)
        Shipment.objects.create(user=instance)
        Transport.objects.create(user=instance)
        Transactions.objects.create(user=instance)
        Billing.objects.create(user=instance)
        