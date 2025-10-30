from fastapi import APIRouter

from src.modules.vehicle.dependencies.company_vehicle import (
    DepRegisterVehicleEntrance,
    DepRegisterVehicleExit,
)
from src.modules.vehicle.dependencies.customer_vehicle import (
    DepDeleteCustomerVehicle,
    DepGetVehicleStatistics,
    DepListCustomerActiveVehicles,
    DepListVehiclesByCustomer,
    DepUpsertCustomerVehicle,
)


router = APIRouter(tags=["Vehicle"])


@router.post("/customer/vehicle", status_code=201)
async def upsert_vehicle(
    response: DepUpsertCustomerVehicle,
):
    """
    Add a vehicle for a customer.
    """
    return response


@router.get("/customer/vehicle", status_code=200)
async def list_vehicles_by_customer(
    response: DepListVehiclesByCustomer,
):
    """
    List all vehicles for a customer.
    """
    return response


@router.delete("/customer/vehicle/{vehicle_id}", status_code=204)
async def delete_vehicle(
    response: DepDeleteCustomerVehicle,
):
    """
    Delete a vehicle for a customer.
    """
    return response


@router.get("/customer/vehicle/{vehicle_plate}", status_code=200)
async def get_vehicle_by_plate(
    response: DepGetVehicleStatistics,
):
    """
    Get vehicle statistics by its plate.
    """
    return response


@router.get("/customer/active-vehicles", status_code=200)
async def list_active_vehicles_by_customer(
    response: DepListCustomerActiveVehicles,
):
    """
    List all active vehicles for a customer including parking prices.
    """
    return response


@router.post("/company/{company_id}/register-entrance", status_code=201)
async def register_vehicle_entrance(
    response: DepRegisterVehicleEntrance,
):
    """
    Register a vehicle entrance for a company.
    """
    return response


@router.post("/company/{company_id}/register-exit", status_code=201)
async def register_vehicle_exit(
    response: DepRegisterVehicleExit,
):
    """
    Register a vehicle exit for a company.
    """
    return response


@router.get("/company/{company_id}/active-vehicles", status_code=200)
async def list_active_vehicles():
    """
    List all active vehicles for a company.
    """
    pass


@router.get("/company/{company_id}/report", status_code=200)
async def list_vehicle_history():
    """
    List vehicle history report for a company including entrances and exits.
    """
    pass


@router.get("/company/{company_id}/statistics", status_code=200)
async def get_vehicle_statistics():
    """
    Get vehicle statistics for a company specific for income.
    """
    pass
