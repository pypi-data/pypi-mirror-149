from gdaps.api import Interface


@Interface
class IDashboardURL:
    """This interface offers an urlpattern that is included dynamically
    into the dashboard of ClientManagementSite domains.

    Add a IDashBoardURL implementation to your urls.py, and it's
    urlpatterns will show up under any ClientManagementSite.
    """

    urlpatterns = []
