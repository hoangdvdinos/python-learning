# Thiết kế exception hierarchy cho hệ thống thương mại điện tử
class EcommerceError(Exception):
    """Root exception — bắt tất cả lỗi của domain này."""
    pass

class ProductError(EcommerceError):
    pass

class OrderError(EcommerceError):
    pass

class PaymentError(EcommerceError):
    pass

# ProductError subtypes
class ProductNotFoundError(ProductError):
    def __init__(self, product_id: int):
        super().__init__(f"Sản phẩm #{product_id} không tồn tại")
        self.product_id = product_id

class OutOfStockError(ProductError):
    def __init__(self, product_id: int, requested: int, available: int):
        super().__init__(
            f"Sản phẩm #{product_id} không đủ hàng "
            f"(yêu cầu: {requested}, còn: {available})"
        )
        self.product_id = product_id
        self.requested = requested
        self.available = available

# PaymentError subtypes
class InsufficientFundsError(PaymentError):
    def __init__(self, required: float, available: float):
        super().__init__(
            f"Không đủ tiền: cần {required:,.0f} VND, có {available:,.0f} VND"
        )
        self.shortfall = required - available

class PaymentGatewayError(PaymentError):
    def __init__(self, gateway: str, reason: str):
        super().__init__(f"[{gateway}] Thanh toán thất bại: {reason}")
        self.gateway = gateway

# Service sử dụng
def place_order(product_id: int, quantity: int, user_balance: float) -> dict:
    # Giả lập data
    products = {1: {"name": "Laptop", "price": 25_000_000, "stock": 2}}

    if product_id not in products:
        raise ProductNotFoundError(product_id)

    product = products[product_id]

    if product["stock"] < quantity:
        raise OutOfStockError(product_id, quantity, product["stock"])

    total = product["price"] * quantity
    if user_balance < total:
        raise InsufficientFundsError(total, user_balance)

    return {"product": product["name"], "quantity": quantity, "total": total}

# Client code — bắt theo mức độ cụ thể cần thiết
def process_order(product_id: int, quantity: int, balance: float):
    try:
        order = place_order(product_id, quantity, balance)
        print(f"Đặt hàng thành công: {order}")

    except OutOfStockError as e:
        print(f"Hết hàng: {e} | Thiếu: {e.requested - e.available} sản phẩm")

    except InsufficientFundsError as e:
        print(f"Không đủ tiền: {e} | Cần thêm: {e.shortfall:,.0f} VND")

    except ProductError as e:
        # Bắt mọi ProductError — kể cả ProductNotFoundError
        print(f"Lỗi sản phẩm: {e}")

    except EcommerceError as e:
        # Bắt tất cả lỗi domain — fallback
        print(f"Lỗi hệ thống: {e}")

process_order(1, 5, 100_000_000)    # OutOfStockError
process_order(1, 1, 10_000_000)     # InsufficientFundsError
process_order(99, 1, 100_000_000)   # ProductNotFoundError