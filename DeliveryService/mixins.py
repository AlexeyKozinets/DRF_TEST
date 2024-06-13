from rest_framework.request import Request



class SessionManagementMixin:
    
    def ensure_session(self, request: Request):
        """
        Сreate session if there is none.

        Args:
            request: Request object.
        """

        if not request.session.session_key:
            request.session.create()
