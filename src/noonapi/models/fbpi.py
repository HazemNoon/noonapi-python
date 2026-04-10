from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FbpiUpdateOrderItemStatus(str, Enum):
    UNSPECIFIED = "UPDATE_ORDER_REQUEST_ITEM_STATUS_UNSPECIFIED"
    OUT_OF_STOCK = "UPDATE_ORDER_REQUEST_ITEM_STATUS_OUT_OF_STOCK"


class FbpiMpItemStatus(str, Enum):
    UNSPECIFIED = "MP_ITEM_STATUS_UNSPECIFIED"
    CONFIRMED = "MP_ITEM_STATUS_CONFIRMED"
    CANCELLED = "MP_ITEM_STATUS_CANCELLED"


class FbpiIntegrationItemStatus(str, Enum):
    UNSPECIFIED = "INTEGRATION_ITEM_STATUS_UNSPECIFIED"
    ACKNOWLEDGED = "INTEGRATION_ITEM_STATUS_ACKNOWLEDGED"
    OUT_OF_STOCK = "INTEGRATION_ITEM_STATUS_OUT_OF_STOCK"
    SHIPPED = "INTEGRATION_ITEM_STATUS_SHIPPED"


@dataclass(frozen=True)
class FbpiActionResponse:
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiActionResponse:
        return cls(raw=dict(data))


@dataclass(frozen=True)
class FbpiShipmentCourierAwb:
    courier: str
    awb_nr: str

    def to_dict(self) -> dict[str, Any]:
        return {"courier": self.courier, "awb_nr": self.awb_nr}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiShipmentCourierAwb:
        return cls(courier=str(data["courier"]), awb_nr=str(data["awb_nr"]))


@dataclass(frozen=True)
class FbpiCreateShipmentItem:
    mp_item_nr: str

    def to_dict(self) -> dict[str, Any]:
        return {"mp_item_nr": self.mp_item_nr}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiCreateShipmentItem:
        return cls(mp_item_nr=str(data["mp_item_nr"]))


@dataclass(frozen=True)
class FbpiCreateShipmentRequest:
    warehouse_code: str
    integration_shipment_nr: str
    fbpi_order_nr: str
    awbs: list[FbpiShipmentCourierAwb]
    items: list[FbpiCreateShipmentItem]

    def to_dict(self) -> dict[str, Any]:
        return {
            "warehouse_code": self.warehouse_code,
            "integration_shipment_nr": self.integration_shipment_nr,
            "fbpi_order_nr": self.fbpi_order_nr,
            "awbs": [awb.to_dict() for awb in self.awbs],
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True)
class FbpiAddShipmentCourierAwbsRequest:
    warehouse_code: str
    integration_shipment_nr: str
    awbs: list[FbpiShipmentCourierAwb]

    def to_dict(self) -> dict[str, Any]:
        return {
            "warehouse_code": self.warehouse_code,
            "integration_shipment_nr": self.integration_shipment_nr,
            "awbs": [awb.to_dict() for awb in self.awbs],
        }


@dataclass(frozen=True)
class FbpiCancelShipmentRequest:
    warehouse_code: str
    integration_shipment_nr: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "warehouse_code": self.warehouse_code,
            "integration_shipment_nr": self.integration_shipment_nr,
        }


@dataclass(frozen=True)
class FbpiGetShipmentRequest:
    warehouse_code: str
    integration_shipment_nr: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "warehouse_code": self.warehouse_code,
            "integration_shipment_nr": self.integration_shipment_nr,
        }


@dataclass(frozen=True)
class FbpiGetNoonLogisticsAwbsRequest:
    country_code: str
    qty: int

    def to_dict(self) -> dict[str, Any]:
        return {"country_code": self.country_code, "qty": self.qty}


@dataclass(frozen=True)
class FbpiListOrdersFilters:
    warehouse_code: str
    created_after: str | None = None
    created_before: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"warehouse_code": self.warehouse_code}
        if self.created_after is not None:
            data["created_after"] = self.created_after
        if self.created_before is not None:
            data["created_before"] = self.created_before
        return data


@dataclass(frozen=True)
class FbpiUpdateOrderItem:
    mp_item_nr: str
    status: FbpiUpdateOrderItemStatus

    def to_dict(self) -> dict[str, Any]:
        return {"mp_item_nr": self.mp_item_nr, "status": self.status.value}


@dataclass(frozen=True)
class FbpiUpdateOrderRequest:
    fbpi_order_nr: str
    items: list[FbpiUpdateOrderItem]

    def to_dict(self) -> dict[str, Any]:
        return {
            "fbpi_order_nr": self.fbpi_order_nr,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True)
class FbpiGetShipmentResponseItem:
    mp_item_nr: str
    partner_sku: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiGetShipmentResponseItem:
        return cls(
            mp_item_nr=str(data["mp_item_nr"]),
            partner_sku=str(data["partner_sku"]),
        )


@dataclass(frozen=True)
class FbpiGetShipmentResponse:
    fbpi_order_nr: str
    awbs: list[FbpiShipmentCourierAwb]
    items: list[FbpiGetShipmentResponseItem]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiGetShipmentResponse:
        return cls(
            fbpi_order_nr=str(data["fbpi_order_nr"]),
            awbs=[FbpiShipmentCourierAwb.from_dict(item) for item in data.get("awbs", [])],
            items=[FbpiGetShipmentResponseItem.from_dict(item) for item in data.get("items", [])],
        )


@dataclass(frozen=True)
class FbpiGetNoonLogisticsAwbsResponse:
    awb_nrs: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiGetNoonLogisticsAwbsResponse:
        return cls(awb_nrs=[str(item) for item in data.get("awb_nrs", [])])


@dataclass(frozen=True)
class FbpiGetFbpiOrderResponseItem:
    mp_item_nr: str
    partner_sku: str
    mp_status: FbpiMpItemStatus
    integration_status: FbpiIntegrationItemStatus
    delivered_invoice_price: float
    cancellation_reason_code: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiGetFbpiOrderResponseItem:
        return cls(
            mp_item_nr=str(data["mp_item_nr"]),
            partner_sku=str(data["partner_sku"]),
            mp_status=FbpiMpItemStatus(data["mp_status"]),
            integration_status=FbpiIntegrationItemStatus(data["integration_status"]),
            delivered_invoice_price=float(data["delivered_invoice_price"]),
            cancellation_reason_code=(
                None
                if data.get("cancellation_reason_code") is None
                else str(data["cancellation_reason_code"])
            ),
        )


@dataclass(frozen=True)
class FbpiGetFbpiOrderResponse:
    fbpi_order_nr: str
    mp_code: str
    mp_order_nr: str
    mp_country_code: str
    customer_country_code: str
    merchant_code: str
    currency_code: str
    warehouse_code: str
    items: list[FbpiGetFbpiOrderResponseItem]
    order_created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiGetFbpiOrderResponse:
        return cls(
            fbpi_order_nr=str(data["fbpi_order_nr"]),
            mp_code=str(data["mp_code"]),
            mp_order_nr=str(data["mp_order_nr"]),
            mp_country_code=str(data["mp_country_code"]),
            customer_country_code=str(data["customer_country_code"]),
            merchant_code=str(data["merchant_code"]),
            currency_code=str(data["currency_code"]),
            warehouse_code=str(data["warehouse_code"]),
            items=[FbpiGetFbpiOrderResponseItem.from_dict(item) for item in data.get("items", [])],
            order_created_at=str(data["order_created_at"]),
        )


@dataclass(frozen=True)
class FbpiListOrdersResponse:
    next_token: str
    orders: list[FbpiGetFbpiOrderResponse]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiListOrdersResponse:
        return cls(
            next_token=str(data["next_token"]),
            orders=[FbpiGetFbpiOrderResponse.from_dict(item) for item in data.get("orders", [])],
        )


@dataclass(frozen=True)
class FbpiGetFbpiOrderCustomerDataResponse:
    first_name: str
    last_name: str
    city: str
    administrative_division: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FbpiGetFbpiOrderCustomerDataResponse:
        return cls(
            first_name=str(data["first_name"]),
            last_name=str(data["last_name"]),
            city=str(data["city"]),
            administrative_division=str(data["administrative_division"]),
        )
