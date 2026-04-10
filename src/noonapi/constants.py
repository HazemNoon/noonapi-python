NOON_GATEWAY_BASE_URL = "https://noon-api-gateway.noon.partners"


def url(path: str) -> str:
    """
    Join noon gateway base url with an absolute path like:
      /identity/v1/whoami
    """
    if not path.startswith("/"):
        path = "/" + path
    return NOON_GATEWAY_BASE_URL + path


# Identity
def identity_login_url() -> str:
    return url("/identity/public/v1/api/login")


def identity_whoami_url() -> str:
    return url("/identity/v1/whoami")


# FBPI
def fbpi_create_shipment_url() -> str:
    return url("/fbpi/v1/shipment/create")


def fbpi_add_shipment_courier_awbs_url() -> str:
    return url("/fbpi/v1/shipment/courier-awbs/add")


def fbpi_cancel_shipment_url() -> str:
    return url("/fbpi/v1/shipment/cancel")


def fbpi_get_shipment_url() -> str:
    return url("/fbpi/v1/shipment/get")


def fbpi_get_noon_logistics_awbs_url() -> str:
    return url("/fbpi/v1/shipment/noon-logistics-awbs/get")


def fbpi_get_order_url(fbpi_order_nr: str) -> str:
    return url(f"/fbpi/v1/fbpi-order/{fbpi_order_nr}/get")


def fbpi_list_orders_url() -> str:
    return url("/fbpi/v1/fbpi-orders/list")


def fbpi_get_order_customer_data_url(fbpi_order_nr: str) -> str:
    return url(f"/fbpi/v1/fbpi-order/{fbpi_order_nr}/customer-details/get")


def fbpi_update_order_url() -> str:
    return url("/fbpi/v1/fbpi-order/update")
