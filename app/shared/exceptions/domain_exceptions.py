class DomainException(Exception):
    """Excepción base para errores de dominio"""
    pass

class ProductCreationError(DomainException):
    """Excepción para errores al crear productos"""
    pass

class ProductNotFoundError(DomainException):
    """Excepción para productos no encontrados"""
    pass

class ProductUpdateError(DomainException):
    """Excepción para errores al actualizar productos"""
    pass

class ProductDeletionError(DomainException):
    """Excepción para errores al eliminar productos"""
    pass

class ProductValidationError(DomainException):
    """Excepción para errores de validación de productos"""
    pass

class InsufficientStockError(DomainException):
    """Excepción para stock insuficiente"""
    pass

class InvalidPriceError(DomainException):
    """Excepción para precios inválidos"""
    pass

class InvalidCategoryError(DomainException):
    """Excepción para categorías inválidas"""
    pass 