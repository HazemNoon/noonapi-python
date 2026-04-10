from noonapi import NoonSession
from noonapi.models.fbpi import (
    FbpiAddShipmentCourierAwbsRequest,
    FbpiCancelShipmentRequest,
    FbpiCreateShipmentItem,
    FbpiCreateShipmentRequest,
    FbpiGetNoonLogisticsAwbsRequest,
    FbpiGetShipmentRequest,
    FbpiListOrdersFilters,
    FbpiShipmentCourierAwb,
    FbpiUpdateOrderItem,
    FbpiUpdateOrderItemStatus,
    FbpiUpdateOrderRequest,
)

session = NoonSession("noon_credentials_sensitive.json")


def show(name: str, value: object) -> None:
    print(f"\n{name}")
    print(value)


warehouse_code = "YOUR_WAREHOUSE_CODE"
fbpi_order_nr = "YOUR_FBPI_ORDER_NR"
integration_shipment_nr = "YOUR_INTEGRATION_SHIPMENT_NR"
mp_item_nr = "YOUR_MP_ITEM_NR"
country_code = "ae"
next_token = ""

shipment_awbs = [
    FbpiShipmentCourierAwb(
        courier="noon",
        awb_nr="YOUR_AWB_NR",
    )
]

shipment_items = [
    FbpiCreateShipmentItem(
        mp_item_nr=mp_item_nr,
    )
]

show(
    "create_shipment",
    session.fbpi.create_shipment(
        FbpiCreateShipmentRequest(
            warehouse_code=warehouse_code,
            integration_shipment_nr=integration_shipment_nr,
            fbpi_order_nr=fbpi_order_nr,
            awbs=shipment_awbs,
            items=shipment_items,
        )
    ),
)

show(
    "add_shipment_courier_awbs",
    session.fbpi.add_shipment_courier_awbs(
        FbpiAddShipmentCourierAwbsRequest(
            warehouse_code=warehouse_code,
            integration_shipment_nr=integration_shipment_nr,
            awbs=shipment_awbs,
        )
    ),
)

show(
    "cancel_shipment",
    session.fbpi.cancel_shipment(
        FbpiCancelShipmentRequest(
            warehouse_code=warehouse_code,
            integration_shipment_nr=integration_shipment_nr,
        )
    ),
)

show(
    "get_shipment",
    session.fbpi.get_shipment(
        FbpiGetShipmentRequest(
            warehouse_code=warehouse_code,
            integration_shipment_nr=integration_shipment_nr,
        )
    ),
)

show(
    "get_noon_logistics_awbs",
    session.fbpi.get_noon_logistics_awbs(
        FbpiGetNoonLogisticsAwbsRequest(
            country_code=country_code,
            qty=1,
        )
    ),
)

show(
    "get_fbpi_order",
    session.fbpi.get_fbpi_order(fbpi_order_nr),
)

show(
    "list_fbpi_orders",
    session.fbpi.list_fbpi_orders(
        FbpiListOrdersFilters(
            warehouse_code=warehouse_code,
        ),
        next_token=next_token,
    ),
)

show(
    "get_fbpi_order_customer_data",
    session.fbpi.get_fbpi_order_customer_data(fbpi_order_nr),
)

show(
    "update_order",
    session.fbpi.update_order(
        FbpiUpdateOrderRequest(
            fbpi_order_nr=fbpi_order_nr,
            items=[
                FbpiUpdateOrderItem(
                    mp_item_nr=mp_item_nr,
                    status=FbpiUpdateOrderItemStatus.OUT_OF_STOCK,
                )
            ],
        )
    ),
)
