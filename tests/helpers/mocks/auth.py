from typing import Any
from src.modules.shared.models.user.user import User
from src.modules.shared.dependencies import auth as auth_deps


class _OverrideHandle:
    def __init__(self, app):
        self.app = app
        self._apps = []
        self._stopped = False

    def stop(self) -> None:
        if not self._stopped:
            targets = [self.app] + self._apps
            for a in targets:
                a.dependency_overrides.pop(auth_deps._get_current_user_token, None)
            self._stopped = True


def mock_get_current_user(target: Any, user: User) -> _OverrideHandle:
    app = getattr(target, "app", target)

    async def _override_current_user(
        token: str | None = None,
        auth_service: object | None = None,
        user_service: object | None = None,
    ):
        return user

    app.dependency_overrides[auth_deps._get_current_user_token] = _override_current_user

    handle = _OverrideHandle(app)
    for route in getattr(app, "routes", []):
        sub = getattr(route, "app", None)
        if sub is not None and hasattr(sub, "dependency_overrides"):
            sub.dependency_overrides[auth_deps._get_current_user_token] = (
                _override_current_user
            )
            handle._apps.append(sub)

    return handle
