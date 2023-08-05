from abc import ABC, abstractmethod
from typing import Optional, Union, Tuple
from datetime import datetime

import connexion
from pydantic import BaseModel
from flask import Response
import six

from odd_models import models


class ODDController(ABC):

    @abstractmethod
    def get_data_entities(self, changed_since=None, ) -> Optional[Tuple[models.DataEntityList, datetime]]:  # noqa: E501
        """
        HTTP method: GET
        path: /entities
        summary: 
        params:
            changed_since
        """
        raise NotImplementedError


class ControllerHolder:
    __controller: ODDController = None

    @classmethod
    def init_controller(cls, controller: ODDController):
        cls.__controller = controller

    @classmethod
    def get_controller(cls) -> ODDController:
        if cls.__controller is None:
            raise RuntimeError('ODD controller has never been initialized')

        return cls.__controller


def get_data_entities(changed_since=None, ):  # noqa: E501
    """
    HTTP method: GET
    path: /entities
    summary: 
    params:
        changed_since
    """

    try:
        result = ControllerHolder.get_controller().get_data_entities(locals())
        if result is None:
            return Response(status=503, headers={'Retry-After': 30})
        elif not isinstance(result[0], BaseModel):
            return 'Internal server error, return type mismatch', 503

        headers = {
            'Content-Type': 'application/json',
            'Last-Modified': result[1],
        }
        response = result[0]
        return Response(response=response.json(exclude_none=True), status=200, headers=headers)
    except NotImplementedError:
        return 'Method has not been implemented', 503

