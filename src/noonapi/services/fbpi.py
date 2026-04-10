from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests

from ..constants import (
    fbpi_add_shipment_courier_awbs_url,
    fbpi_cancel_shipment_url,
    fbpi_create_shipment_url,
    fbpi_get_noon_logistics_awbs_url,
    fbpi_get_order_customer_data_url,
    fbpi_get_order_url,
    fbpi_get_shipment_url,
    fbpi_list_orders_url,
    fbpi_update_order_url,
)
from ..errors import NoonApiError
from ..models.fbpi import (
    FbpiActionResponse,
    FbpiAddShipmentCourierAwbsRequest,
    FbpiCancelShipmentRequest,
    FbpiCreateShipmentRequest,
    FbpiGetFbpiOrderCustomerDataResponse,
    FbpiGetFbpiOrderResponse,
    FbpiGetNoonLogisticsAwbsRequest,
    FbpiGetNoonLogisticsAwbsResponse,
    FbpiGetShipmentRequest,
    FbpiGetShipmentResponse,
    FbpiListOrdersFilters,
    FbpiListOrdersResponse,
    FbpiUpdateOrderRequest,
)

if TYPE_CHECKING:
    from ..session import NoonSession


class FbpiService:
    """
    FBPI service.
    - Creates and manages FBPI shipments
    - Retrieves FBPI orders, shipment details, and customer details
    - Updates orders and fetches noon logistics AWBs
    """

    def __init__(self, session: NoonSession) -> None:
        self._session = session

    def create_shipment(self, request: FbpiCreateShipmentRequest) -> FbpiActionResponse:
        res = self._session.request(
            "POST",
            fbpi_create_shipment_url(),
            json=request.to_dict(),
        )
        return self._decode_action_response(res)

    def add_shipment_courier_awbs(
        self, request: FbpiAddShipmentCourierAwbsRequest
    ) -> FbpiActionResponse:
        res = self._session.request(
            "POST",
            fbpi_add_shipment_courier_awbs_url(),
            json=request.to_dict(),
        )
        return self._decode_action_response(res)

    def cancel_shipment(self, request: FbpiCancelShipmentRequest) -> FbpiActionResponse:
        res = self._session.request(
            "POST",
            fbpi_cancel_shipment_url(),
            json=request.to_dict(),
        )
        return self._decode_action_response(res)

    def get_shipment(self, request: FbpiGetShipmentRequest) -> FbpiGetShipmentResponse:
        res = self._session.request(
            "POST",
            fbpi_get_shipment_url(),
            json=request.to_dict(),
        )
        return self._decode_model_response(res, FbpiGetShipmentResponse)

    def get_noon_logistics_awbs(
        self, request: FbpiGetNoonLogisticsAwbsRequest
    ) -> FbpiGetNoonLogisticsAwbsResponse:
        res = self._session.request(
            "POST",
            fbpi_get_noon_logistics_awbs_url(),
            json=request.to_dict(),
        )
        return self._decode_model_response(res, FbpiGetNoonLogisticsAwbsResponse)

    def get_fbpi_order(self, fbpi_order_nr: str) -> FbpiGetFbpiOrderResponse:
        res = self._session.request(
            "GET",
            fbpi_get_order_url(fbpi_order_nr),
        )
        return self._decode_model_response(res, FbpiGetFbpiOrderResponse)

    def list_fbpi_orders(
        self, filters: FbpiListOrdersFilters, *, next_token: str
    ) -> FbpiListOrdersResponse:
        res = self._session.request(
            "POST",
            fbpi_list_orders_url(),
            json=filters.to_dict(),
            params={"next_token": next_token},
        )
        return self._decode_model_response(res, FbpiListOrdersResponse)

    def get_fbpi_order_customer_data(
        self, fbpi_order_nr: str
    ) -> FbpiGetFbpiOrderCustomerDataResponse:
        res = self._session.request(
            "GET",
            fbpi_get_order_customer_data_url(fbpi_order_nr),
        )
        return self._decode_model_response(res, FbpiGetFbpiOrderCustomerDataResponse)

    def update_order(self, request: FbpiUpdateOrderRequest) -> FbpiActionResponse:
        res = self._session.request(
            "POST",
            fbpi_update_order_url(),
            json=request.to_dict(),
        )
        return self._decode_action_response(res)

    def _decode_action_response(self, res: requests.Response) -> FbpiActionResponse:
        self._raise_for_error(res)
        return FbpiActionResponse.from_dict(self._decode_json_dict(res))

    def _decode_model_response(self, res: requests.Response, model_cls: type[Any]) -> Any:
        self._raise_for_error(res)
        return model_cls.from_dict(self._decode_json_dict(res))

    @staticmethod
    def _decode_json_dict(res: requests.Response) -> Any:
        try:
            return res.json()
        except Exception as err:
            raise NoonApiError(
                http_status=res.status_code,
                message=res.text,
            ) from err

    @staticmethod
    def _raise_for_error(res: requests.Response) -> None:
        if res.status_code < 400:
            return

        http_status = res.status_code

        try:
            data = res.json()
        except Exception as err:
            raise NoonApiError(http_status=http_status, message=res.text) from err

        if isinstance(data, dict):
            message = data.get("message") or res.text
            details = data.get("details")
            raise NoonApiError(
                http_status=http_status,
                message=str(message),
                status_code=data.get("status_code"),
                status_id=data.get("status_id"),
                details=details if isinstance(details, list) else None,
            )

        raise NoonApiError(http_status=http_status, message=str(data))
