import logging
import uuid

from typing import Dict, Optional, Callable

from ..service.template import ServiceClass
# from .service.rest_api import RestAPI

from .device import Device

from ..schema import base_schema as WSchema
from ..schema.iot_schema import WappstoMethod

from ..utils import name_check


# #############################################################################
#                                 Network Setup
# #############################################################################

class Network(object):

    schema = WSchema.Network

    def __init__(
        self,
        name: str,
        connection: ServiceClass,
        network_uuid: uuid.UUID,
        description: str = "",
    ) -> None:
        """
        Configure the WappstoIoT settings.
        """
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

        kwargs = locals()
        self.__uuid: uuid.UUID = network_uuid
        self.element: WSchema.Network = self.schema()

        self.children_uuid_mapping: Dict[uuid.UUID, Device] = {}
        self.children_name_mapping: Dict[str, uuid.UUID] = {}

        self.cloud_id_mapping: Dict[int, uuid.UUID] = {}

        self.connection: ServiceClass = connection

        self.element = self.schema(
            name=name,
            description=description,
            meta=WSchema.NetworkMeta(
                version=WSchema.WappstoVersion.V2_0,
                type=WSchema.WappstoMetaType.NETWORK,
                id=self.uuid
            )
        )

        element = self.connection.get_network(self.uuid)
        if element:
            self.__update_self(element)
            # self.log.debug(
            #     type(self.element.meta)
            # )
            # self.log.debug(
            #     self.element.meta
            # )
            # self.log.debug(
            #     type(element.meta)
            # )
            # self.log.debug(
            #     element.meta
            # )
            if self.element != element:
                # TODO: Post diff only.
                self.log.info("Data Models Differ. Sending Local.")
                self.connection.post_network(self.element)
        else:
            self.connection.post_network(self.element)

    @property
    def name(self) -> Optional[str]:
        """Returns the name of the value."""
        return self.element.name

    @property
    def uuid(self) -> uuid.UUID:
        """Returns the name of the value."""
        return self.__uuid

    # -------------------------------------------------------------------------
    #   Save/Load helper methods
    # -------------------------------------------------------------------------

    def __update_self(self, element: WSchema.Network):
        # TODO(MBK): Check if new devices was added! & Check diff.
        # NOTE: If there was a diff, post local one.
        self.element = element.copy(update=self.element.dict(exclude_none=True))
        self.element.meta = element.meta.copy(update=self.element.meta)
        for nr, device in enumerate(self.element.device):
            self.cloud_id_mapping[nr] = device

    # -------------------------------------------------------------------------
    #   Network 'on-' methods
    # -------------------------------------------------------------------------

    def onChange(
        self,
        callback: Callable[['Network'], None],
    ) -> None:
        """
        Configure a callback for when a change to the Network have occurred.

        # UNSURE(MBK): How should it get the data back?
        """
        def _cb(obj, method):
            try:
                if method == WappstoMethod.PUT:
                    callback(...)
            except Exception:
                self.log.exception("OnChange callback error.")
                raise

        self.connection.subscribe_network_event(
            uuid=self.uuid,
            callback=_cb
        )

    def onCreate(
        self,
        callback: Callable[['Network'], None],
    ) -> None:
        """
        Configure a callback for when a create have been make for the Device.
        """
        def _cb(obj, method):
            try:
                if method == WappstoMethod.POST:
                    callback()
            except Exception:
                self.log.exception("onCreate callback error.")
                raise

        self.connection.subscribe_network_event(
            uuid=self.uuid,
            callback=_cb
        )

    def onRefresh(
        self,
        callback: Callable[['Network'], None]
    ):
        """
        Configure an action when a refresh Network have been Requested.

        Normally when a refresh have been requested on a Network, ...
        ...
        # It can not! there is no '{"status":"update"}' that can be set.
        """
        def _cb(obj, method):
            try:
                if method == WappstoMethod.GET:
                    callback()
            except Exception:
                self.log.exception("onRefresh callback error.")
                raise

        self.connection.subscribe_network_event(
            uuid=self.uuid,
            callback=_cb
        )

    def onDelete(
        self,
        callback: Callable[['Network'], None]
    ):
        """
        Configure an action when a Delete Network have been Requested.

        Normally when a Delete have been requested on a Network,
        it is when it is not wanted anymore, and the Network have been
        unclaimed. Which mean that all the devices & value have to be
        recreated, and/or the program have to close.
        """
        def _cb(obj, method):
            try:
                if method == WappstoMethod.DELETE:
                    callback(self)
            except Exception:
                self.log.exception("onDelete callback error.")
                raise

        self.connection.subscribe_network_event(
            uuid=self.uuid,
            callback=_cb
        )

    # -------------------------------------------------------------------------
    #   Network methods
    # -------------------------------------------------------------------------

    def refresh(self):
        raise NotImplementedError("Method: 'refresh' is not Implemented.")

    def change(self):
        pass

    def delete(self):
        """
        Normally it is used to unclaim a Network & delete all children.

        If a network delete itself, it will prompt a factory reset.
        This means that manufacturer and owner will be reset (or not),
        in relation of the rules set up in the certificates.
        """
        self.connection.delete_network(uuid=self.uuid)

    # -------------------------------------------------------------------------
    #   Create methods
    # -------------------------------------------------------------------------

    def createDevice(
        self,
        name: str,
        manufacturer: Optional[str] = None,
        product: Optional[str] = None,
        version: Optional[str] = None,
        serial: Optional[str] = None,
        protocol: Optional[str] = None,
        communication: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Device:
        """
        Create a new Wappsto Device.

        A Wappsto Device is references something that is attached to the network
        that can be controlled or have values that can be reported to Wappsto.

        This could be a button that is connected to this unit,
        or in the case of this unit is a gateway, it could be a remote unit.
        """
        kwargs = locals()
        kwargs.pop('self')

        if not name_check.legal_name(name):
            raise ValueError(
                "Given name contain a ilegal character."
                f"May only contain: {name_check.wappsto_letters}"
            )

        device_uuid = self.connection.get_device_where(
            network_uuid=self.uuid,
            name=name
        )

        device_obj = Device(
            parent=self,
            device_uuid=device_uuid,
            **kwargs
        )
        self.__add_device(device_obj, kwargs['name'])
        return device_obj

    def __add_device(self, device: Device, name: str):
        """Helper function for Create, to only localy create it."""
        self.children_uuid_mapping[device.uuid] = device
        self.children_name_mapping[name] = device.uuid

    def close(self):
        pass
