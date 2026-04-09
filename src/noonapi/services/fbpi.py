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

if TYPE_CHECKING:
    from ..session import NoonSession


class FbpiService:
    """
    FBPI service.

    Hand-written service wrapper based on the synced swagger definitions while
    following the same SDK style as the existing auth service.
    """

    def __init__(self, session: "NoonSession") -> None:
        self._session = session

    def create_shipment(self, body: dict[str, Any]) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_create_shipment_url(),
            json=body,
        )
        return self._decode_json_response(res)

    def add_shipment_courier_awbs(self, body: dict[str, Any]) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_add_shipment_courier_awbs_url(),
            json=body,
        )
        return self._decode_json_response(res)

    def cancel_shipment(self, body: dict[str, Any]) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_cancel_shipment_url(),
            json=body,
        )
        return self._decode_json_response(res)

    def get_shipment(self, body: dict[str, Any]) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_get_shipment_url(),
            json=body,
        )
        return self._decode_json_response(res)

    def get_noon_logistics_awbs(self, body: dict[str, Any]) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_get_noon_logistics_awbs_url(),
            json=body,
        )
        return self._decode_json_response(res)

    def get_fbpi_order(self, fbpi_order_nr: str) -> dict[str, Any]:
        res = self._session.request(
            "GET",
            fbpi_get_order_url(fbpi_order_nr),
        )
        return self._decode_json_response(res)

    def list_fbpi_orders(self, filters: dict[str, Any], *, next_token: str) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_list_orders_url(),
            json=filters,
            params={"next_token": next_token},
        )
        return self._decode_json_response(res)

    def get_fbpi_order_customer_data(self, fbpi_order_nr: str) -> dict[str, Any]:
        res = self._session.request(
            "GET",
            fbpi_get_order_customer_data_url(fbpi_order_nr),
        )
        return self._decode_json_response(res)

    def update_order(self, body: dict[str, Any]) -> dict[str, Any]:
        res = self._session.request(
            "POST",
            fbpi_update_order_url(),
            json=body,
        )
        return self._decode_json_response(res)

    def _decode_json_response(self, res: requests.Response) -> dict[str, Any]:
        self._raise_for_error(res)

        data = res.json()
        if not isinstance(data, dict):
            raise NoonApiError(
                http_status=200,
                message=f"Unexpected FBPI response type: {type(data)}",
            )

        return data

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
