from django_unicorn.components import UnicornView

from medux.settings import Scope, ScopeIcons


class ScopeSwitcherView(UnicornView):
    active_scope = Scope.USER
    scope_icons = ScopeIcons.USER

    def set_scope(self, scope: int):
        # TODO: maybe check permissions here?
        self.active_scope = Scope(scope)
        self.scope_icons = ScopeIcons.USER  # bug?
