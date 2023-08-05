from typing import Any, Dict, Type

from fastapi import FastAPI

from fast_boot.context.application import ApplicationContext, T
from fast_boot.security.access.hierarchical_roles import (
    RoleHierarchy
)
from fast_boot.security.access.permission_evaluator import (
    PermissionEvaluator
)
from fast_boot.security.authentication import AuthenticationTrustResolver
from fast_boot.security.core import GrantedAuthorityDefaults
from fast_boot.security_lite.access_decision_manager import AccessDecisionManager


class FastApplication(FastAPI, ApplicationContext):
    bean_factory: Dict[Type, Any] = {}
    INSTANCE: ApplicationContext

    def setup(self) -> None:
        super().setup()
        beans = {
            RoleHierarchy,
            GrantedAuthorityDefaults,
            PermissionEvaluator,
            AuthenticationTrustResolver,
            AccessDecisionManager
        }
        self.bean_factory = {bean: bean() for bean in beans}
        self.INSTANCE = self

    def get_id(self):
        return id(self)

    def get_application_name(self) -> str:
        return self.title

    def get_display_name(self) -> str:
        return self.title

    def set_bean(self, bean: Any) -> None:
        self.bean_factory.update({type(bean): bean})

    def put_bean(self, bean_name: Type, bean: Any) -> None:
        assert isinstance(bean, bean_name), TypeError("Bean must be an instance of bean_name")
        self.bean_factory.update({bean_name: bean})

    def update_bean(self, bean_dict: Dict) -> None:
        for bean_name, bean in bean_dict.items():
            assert isinstance(bean, bean_name), TypeError("Bean must be an instance of bean_name")
        self.bean_factory.update(bean_dict)

    def get_bean(self, type: Type[T]) -> T:
        return self.bean_factory.get(type)
