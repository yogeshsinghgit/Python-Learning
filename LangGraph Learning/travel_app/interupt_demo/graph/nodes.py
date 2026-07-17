from loguru import logger
from langgraph.types import interrupt

from graph.state import BookingState


def prepare_booking(state: BookingState) -> BookingState:
    logger.info("Preparing hotel booking...")

    destination = "Japan"
    hotel_name = "Tokyo Grand Hotel"

    logger.info(
        f"Prepared booking for destination='{destination}', hotel='{hotel_name}'"
    )

    return {
        "destination": destination,
        "hotel_name": hotel_name,
    }


def wait_for_approval(state: BookingState) -> BookingState:
    logger.info("Waiting for user approval...")

    approval = interrupt(
        {
            "message": (
                f"Do you want to book "
                f"{state['hotel_name']} in {state['destination']}?"
            ),
            "options": ["yes", "no"],
        }
    )

    logger.info(f"Received approval response: {approval}")

    return {
        "approved": approval.lower() == "yes",
    }


def confirm_booking(state: BookingState) -> BookingState:
    logger.info("Processing booking confirmation...")

    if state["approved"]:
        logger.success(
            f"Booking confirmed for '{state['hotel_name']}' "
            f"in '{state['destination']}'."
        )
    else:
        logger.warning(
            f"Booking cancelled for '{state['hotel_name']}' "
            f"in '{state['destination']}'."
        )

    return {}