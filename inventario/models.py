from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo_sku = models.CharField(
        max_length=50, unique=True, verbose_name="Código / SKU"
    )
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock / Cantidad")
    
    # =========================================================================
    # UBICACIÓN DE LA LLAVE FORÁNEA (RELACIÓN MUCHOS A UNO)
    # =========================================================================
    # Un Producto pertenece a una Categoría; una Categoría tiene muchos Productos.
    categoria = models.ForeignKey(
        # 1. 'Categoria' (String): Evita NameError e importaciones circulares.
        'Categoria',
        
        # 2. on_delete=models.SET_NULL: Si borras la categoría, el producto NO se borra;
        # su columna "categoria_id" simplemente queda vacía (NULL) en la base de datos.
        on_delete=models.SET_NULL,
        
        # 3. Requisito para SET_NULL: Permite que el campo acepte valores vacíos.
        null=True,
        blank=True,
        
        # 4. related_name="productos": Te permite consultar desde el objeto categoría 
        # todos sus productos vinculados usando: mi_categoria.productos.all()
        related_name="productos",
        
        verbose_name="Categoría"
    )
    # =========================================================================
    
    numero_serie = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Número de serie"
    )

    disponible = models.BooleanField(
        default=True, 
        verbose_name="Disponible para préstamo"
    )

    ubicacion = models.CharField(
        max_length=150, 
        blank=True, 
        null=True, 
        verbose_name="Almacén / Estante"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]
        # NUEVO: Índices optimizados para búsquedas rápidas en la base de datos
        indexes = [
            models.Index(fields=['codigo_sku']),
            models.Index(fields=['nombre']),
            models.Index(fields=['stock']),
        ]

    def __str__(self):
        return f"[{self.codigo_sku}] {self.nombre}"