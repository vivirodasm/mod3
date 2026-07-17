from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):

        self.page = page

        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")

    def fill_shipping(self, first, last, zip_code):

        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(zip_code)

        return self

    def continue_to_overview(self):

        self.continue_button.click()

        return self

    def has_error(self):

        return self.page.locator("[data-test='error']").is_visible()