# In the name of GOD
from .authenticate_service import AuthenticateService
from .notification_service import NotificationService
from .podcast_service import PodcastService

SERVICE_CLASSES = {
    "authentication":AuthenticateService,
    "notification": NotificationService,
    "podcast": PodcastService
    }
