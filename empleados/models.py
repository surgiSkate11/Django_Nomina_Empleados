from django.db import models
from decimal import Decimal

class Cargo(models.Model):
    descripcion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.descripcion

class Departamento(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class TipoContrato(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Empleado(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Rol(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    #El null y blank es para q los roles tengan obligatoriamente un empleado.
    
    aniomes = models.DateField()
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extra = models.DecimalField(max_digits=10, decimal_places=2)
    bono = models.DecimalField(max_digits=10, decimal_places=2)
    iess = models.DecimalField(max_digits=10, decimal_places=2)
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2)
    neto = models.DecimalField(max_digits=10, decimal_places=2)
     
    def __str__(self):
        return f"Rol de {self.empleado.nombre} para {self.aniomes}"

    # Aquí va la lógica para calcular el IESS, tot_ing, tot_des y neto
    
    def save(self):
        # Traime el sueldo del empleado:
         self.sueldo = self.empleado.sueldo
        
        # Calcular IESS (9.45% del sueldo)
        self.iess = round(self.sueldo * Decimal('0.0945'), 2)
        
        # Calcular total ingresos (sueldo + horas_extra + bono)
        self.tot_ing = round(self.sueldo + self.horas_extra + self.bono, 2)
        
        # Calcular total descuentos (iess)
        self.tot_des = self.iess
        
        # Calcular neto a pagar (tot_ing - tot_des)
        self.neto = round(self.tot_ing - self.tot_des, 2)
        
        super(Rol, self).save()
        
        # save(*args, **kwargs)

