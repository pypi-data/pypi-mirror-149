import abc
import logging
from collections.abc import Iterator

import pydicom
import pynetdicom
from pynetdicom import AE
from pynetdicom.presentation import build_context

from aide.pacs_client.pacs_config import PacsConfiguration

STATUS_SUCCESS = 0x0000


class PacsError(Exception):
    pass


class AbstractPacsClient(abc.ABC):

    @abc.abstractmethod
    def store_dicom_dataset(self, dataset):
        raise NotImplementedError

    @abc.abstractmethod
    def store_dicom_series(self, datasets):
        raise NotImplementedError


class PacsClient(AbstractPacsClient):

    def __init__(self, config: PacsConfiguration):
        self.ae_title = config.ae_title
        self.host = config.host
        self.port = config.port
        self.dimse_timeout = config.dimse_timeout

    @staticmethod
    def _build_context(ds: pydicom.Dataset):
        return [build_context(ds.SOPClassUID, ds.file_meta.TransferSyntaxUID)]

    def _associate(self,
                   dataset: pydicom.Dataset):
        ae = AE(self.ae_title)
        ae.requested_contexts = self._build_context(dataset)
        assoc = ae.associate(self.host, self.port)
        assoc.dimse_timeout = self.dimse_timeout
        return assoc

    @staticmethod
    def _release_association(assoc: pynetdicom.Association):
        if assoc:
            assoc.release()

    @staticmethod
    def _save_dicom(assoc: pynetdicom.Association,
                    dataset: pydicom.Dataset):
        if assoc and assoc.is_established:
            status = assoc.send_c_store(dataset)
            if getattr(status, 'Status', None) == STATUS_SUCCESS:
                logging.info("Saved dicom to Pacs")
            else:
                raise PacsError()
        else:
            raise PacsError("Association not established")

    def store_dicom_series(self, datasets: Iterator):
        assoc = None
        try:
            for i, ds in enumerate(datasets):
                if i == 0:
                    assoc = self._associate(ds)
                self._save_dicom(assoc, ds)
        except Exception:
            logging.exception("Could not save dicom series")
            raise
        finally:
            self._release_association(assoc)

    def store_dicom_dataset(self, dataset: pydicom.Dataset):
        assoc = None
        try:
            assoc = self._associate(dataset)
            self._save_dicom(assoc, dataset)
        finally:
            self._release_association(assoc)
