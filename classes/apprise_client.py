import apprise


class AppriseClient:
    APPRISE_CONFIG = './configs/apprise_config.yml'

    def __init__(self):
        self.app_obj = apprise.Apprise()
        config = apprise.AppriseConfig()
        config.add(self.APPRISE_CONFIG)
        self.app_obj.add(config)

    def send_notification(self, title, body):
        self.app_obj.notify(title=title, body=body)
