from flet import AlertDialog, Text, FontWeight, Page, TextButton


class InfoDialog:
    def __init__(self, page: Page):
        self.page = page

    def open(self, title: str, content_text: str):
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(size=20, weight=FontWeight.W_400, value=title),
            content=Text(size=16, value=content_text),
            actions=[
                TextButton(text="OK", on_click=lambda _: self.close())
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def close(self):
        self.page.dialog.open = False
        self.page.update()
