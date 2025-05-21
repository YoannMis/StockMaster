from django.db import models


# Product model
class Product(models.Model):
    # Enum type choices for the different types of products available
    class Types(models.TextChoices):
        CONSUMABLE = "Consumable"
        GLASS = "Glass"
        CHEMICAL = "Chemical"

    # Stock Keeping Unit: a unique internal reference for each product
    sku = models.CharField(max_length=10, unique=True, verbose_name="internal product reference")
    # Product name
    name = models.CharField(max_length=100, verbose_name="product name")
    # A short description of the product
    description = models.TextField(max_length=255, blank=True, verbose_name="product description")
    # The type of product among the choices available in the enum type "Types"
    product_type = models.CharField(choices=Types, null=True, verbose_name="product type")
    # Product price
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="price")
    # Supplier from whom to order the product
    supplier = models.CharField(max_length=30, verbose_name="supplier")
    # Supplier reference to order the product
    supplier_ref = models.CharField(max_length=30, verbose_name="supplier_reference")
    # Manufacturer who produces the product
    manufacturer = models.CharField(max_length=30, verbose_name="manufacturer")
    # Manufacturer product's reference
    manufacturer_ref = models.CharField(max_length=30, verbose_name="manufacturer_reference")
    # If the product is critical, there must always be at least one in stock in the building store
    critical = models.BooleanField(default=False, verbose_name="is critical product ?")

    def __str__(self):
        return f"{self.name} - {self.sku}"


# Warehouse model
class Warehouse(models.Model):
    # Enum type choices for the different types of warehouse available
    class Types(models.TextChoices):
        # The main store where all the products available for the other warehouses are stored
        MAIN = "Main store"
        # The building's central warehouse where the products available for the building's various kanbans are stored
        STORE = "Store"
        # Small local store named Kanban where users can pick up the products they need
        KANBAN = "Kanban"

    # Warehouse name
    name = models.CharField(max_length=50, verbose_name="name")
    # Warehouse location
    location = models.CharField(max_length=50, verbose_name="location")
    # The type of product among the choices available in the enum type "Types"
    warehouse_type = models.CharField(choices=Types, default=Types.STORE, verbose_name="type")
    # Link to the Product model: all the products present in the warehouse
    # products = models.ManyToManyField(Product,
    #                                   blank=True,
    #                                   on_delete=models.CASCADE,
    #                                   related_name="products",
    #                                   verbose_name="products in the store")

    def __str__(self):
        return f"{self.name} ({self.location})"


# Stock model
class Stock(models.Model):
    # Different product storage units
    class StockUnits(models.TextChoices):
        LITER = "L", "Liter"
        MILLILITER = "ML", "Milliliter"
        GRAM = "G", "Gram"
        KILOGRAM = "KG", "Kilogram"
        MILLIGRAM = "MG", "Milligram"
        # Add more stock units

    # Different stock packaging units
    class StockPackaging(models.TextChoices):
        CARDBOARD = "CDB", "Cardboard"
        BOTTLE = "BTL", "Bottle"
        PACK = "PCK", "Pack"
        BAG = "BAG", "Bag"

    # Quantity of stock unit
    unit_quantity = models.IntegerField(blank=True, verbose_name="stock unit quantity")
    # Product storage units
    stock_unit = models.CharField(choices=StockUnits, blank=True, verbose_name="product unit")
    # Quantity of stock packaging
    pack_quantity = models.IntegerField(blank=True, verbose_name="stock packaging quantity")
    # Product stock packaging
    stock_packaging = models.CharField(choices=StockPackaging, blank=True, verbose_name="packaging")
    # Stock update date
    last_updated = models.DateTimeField(auto_now=True, verbose_name="last update date")
    # Stock location on shelves in the warehouse
    shelving = models.CharField(max_length=4, verbose_name="shelving")
    # Stock batch number
    batch = models.CharField(max_length=20, verbose_name="batch number")
    # Expiration date of the product if it exists
    expiration_date = models.DateField(null=True, verbose_name="expiration date")
    # Reception date of the product if needed
    reception_date = models.DateField(blank=True, verbose_name="reception date")
    # The alert threshold when the minimum stock is reached
    threshold = models.IntegerField(default=1, verbose_name="alert threshold")
    # Link to the Product model: product to which the stock is attached
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product", verbose_name="product")
    # Link to the Warehouse model: warehouse where the stock is stored
    warehouse = models.ForeignKey(Warehouse,
                                  on_delete=models.CASCADE,
                                  related_name="warehouse",
                                  verbose_name="warehouse")

    def __str__(self):
        return f"stock of {Stock.product.__str__()}"


# Stock movement model
class StockMovement(models.Model):
    # Movement type: if the product go in or go out
    movement_type = models.CharField(max_length=10, choices=[('IN', 'In'), ('OUT', 'Out')]) # Pourquoi pas un TextChoices ?
    # The quantity of product that is moved
    quantity = models.IntegerField(default=1, verbose_name="quantity")
    # The timestamp when the stock movement is recorded
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")
    # The reason of the stock movement
    reason = models.CharField(max_length=250, blank=True, verbose_name="reason")
    # Link to the Stock model: which stock is moved
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="stock")
    # Think about if it's nécessary to add theses attributes:
    # The location from where the stock has moved
    # old_location = models.OneToOneField(Warehouse, on_delete=models.CASCADE, related_name="old", verbose_name="from warehouse")
    # The location to where the stock is moving
    # new_location = models.OneToOneField(Warehouse, on_delete=models.CASCADE, related_name="new", verbose_name="to warehouse")

    def __str__(self):
        return f"stock movement of {self.timestamp}"
