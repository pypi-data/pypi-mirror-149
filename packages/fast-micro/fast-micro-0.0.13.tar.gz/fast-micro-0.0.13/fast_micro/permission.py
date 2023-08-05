from abc import ABC, abstractmethod
from typing import Callable, List

from starlette import status
from starlette.requests import Request
from starlette.exceptions import HTTPException


PERMISSION_FUNC: Callable[[Request, List[str]], bool] = lambda req, perms : True


class PermissionsDependency(object):
    """
    Permission dependency that is used to define and check all the permissions
    from one place inside route definition.

    Always returns true unless permission_handler has been set in create_app.

    Use it as an argument to FastAPI's `Depends` as follows:
    .. code-block:: python
        app = FastAPI()
        @app.get(
            "/teapot/",
            dependencies=[Depends(
                PermissionsDependency(["TeapotUserAgentPermission"]))]
        )
        async def teapot() -> dict:
            return {"teapot": True}
    """
    error_msg = "Forbidden"
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, permissions: List[str]):
        self.permissions = permissions

    def __call__(self, request: Request):
        if not self.has_required_permissions(request):
            raise HTTPException(
                status_code=self.status_code,
                detail=self.error_msg
            )

    def has_required_permissions(self, request: Request) -> bool:
        return PERMISSION_FUNC(request, self.permissions)