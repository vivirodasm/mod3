"""Tests del checkout usando el patrón Screenplay."""

from screenplay.actor import Actor
from screenplay.abilities.browse_web import BrowseTheWeb
from screenplay.tasks.login import Login
from screenplay.tasks.add_to_cart import AddToCart
from screenplay.tasks.complete_checkout import CompleteCheckout


def test_actor_completa_checkout(page):
    """Un Actor puede completar los datos iniciales del checkout."""
    viviana = Actor("Viviana").can(BrowseTheWeb.using(page))

    viviana.attempts_to(
        Login.as_user("standard_user", "secret_sauce"),
        AddToCart.the_item("Sauce Labs Backpack"),
        CompleteCheckout.with_info(
            "Viviana",
            "Rodas",
            "110111",
        ),
    )

    assert page.url.endswith("/checkout-step-two.html"), (
        "Viviana debería llegar a la pantalla de resumen del checkout."
    )