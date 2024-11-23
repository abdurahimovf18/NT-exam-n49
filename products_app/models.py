from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)

    image = models.ImageField(upload_to="category_images", 
                              default="category_images/category_default_image.png")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ProductModel(models.Model):
    categories = models.ManyToManyField(CategoryModel, related_name="products")

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    image = models.ImageField(upload_to="product_images", 
                              default="product_images/product_default_image.png")
    current_price = models.DecimalField(decimal_places=2, max_digits=6)
    last_price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class OrderModel(models.Model):
    product = models.ForeignKey(ProductModel, related_name="orders", on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, related_name="orders", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    
    @property
    def total_price(self):
        return self.product.current_price * self.quantity
    
    def __str__(self) -> str:
        return f"{self.user}'s order {self.product}"
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        unique_together = (
            ("product", "user")
            )
