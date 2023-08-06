import json
import threading
import time

import requests

from .config import HUB_API_ROOT
from .yolov5_utils.general import LOGGER, PREFIX


class HUBLogger:
    api_url = HUB_API_ROOT + "model-checkpoint"

    def __init__(self, model_id, auth):
        self.model_id = model_id
        self.auth = auth
        self.rate_limit = 60.0  # minimum seconds between checkpoint uploads
        self.t = time.time()  # last upload time
        self.keys = [
            'train/box_loss',
            'train/obj_loss',
            'train/cls_loss',  # train loss
            'metrics/precision',
            'metrics/recall',
            'metrics/mAP_0.5',
            'metrics/mAP_0.5:0.95',  # metrics
            'val/box_loss',
            'val/obj_loss',
            'val/cls_loss',  # val loss
            'x/lr0',
            'x/lr1',
            'x/lr2']  # metrics keys

    def on_fit_epoch_end(self, *args, **kwargs):
        """
        Runs after each val each epoch

        Args:
             *args     log_vals, epoch
        """
        vals, epoch = args[:2]
        metrics = json.dumps({k: float(v) for k, v in zip(self.keys, vals)})  # json string
        # print(f"{PREFIX}Uploading metrics for {self.model_id}: {metrics}")  # debug
        threading.Thread(target=self._upload_epoch, args=(epoch, metrics), daemon=True).start()

    def _upload_epoch(self, epoch, metrics):
        payload = {"modelId": self.model_id, "epoch": epoch, "metrics": metrics, "type": "metrics"}
        payload.update(self.auth.get_auth_string())
        requests.post(self.api_url, data=payload, files={"void": None})

    def on_model_save(self, *args, **kwargs):
        """
        Runs after each model save

        Args:
             *args     last, epoch, final_epoch, best_fitness, fi
        """

        # Set args
        last, epoch, final_epoch, best_fitness, fi = args[:5]
        is_best = best_fitness == fi

        if (time.time() - self.t) > self.rate_limit:
            LOGGER.info(f"{PREFIX}Uploading checkpoint for {self.model_id}")
            threading.Thread(target=self._upload_model, args=(epoch, is_best, last), daemon=True).start()
            self.t = time.time()

    def _upload_model(self, epoch, is_best, weights):
        payload = {"modelId": self.model_id, "epoch": epoch, "isBest": bool(is_best), "type": "epoch"}
        payload.update(self.auth.get_auth_string())
        with open(weights, "rb") as last:
            r = requests.post(self.api_url, data=payload, files={"last.pt": last})
            if r.status_code != 200:
                LOGGER.info(f"{PREFIX}Unable to upload checkpoint!")

    def on_pretrain_routine_end(self, *args, **kwargs):
        # Tell HUB that training has started
        payload = {"modelId": self.model_id, "type": "initial"}
        payload.update(self.auth.get_auth_string())
        requests.post(self.api_url, data=payload, files={"void": None})

    def on_train_end(self, *args, **kwargs):
        """"
        Args:

            *args   last, best, plots, epoch
        """
        # Set args
        last, best, plots, epoch, results = args[:5]

        # mAP0.5:0.95
        map_new = results[3]

        payload = {"modelId": self.model_id, "epoch": epoch, "map": map_new, "type": "final"}
        payload.update(self.auth.get_auth_string())

        LOGGER.info(f"{PREFIX}Uploading final models for {self.model_id}")
        with open(best, "rb") as best:
            r = requests.post(self.api_url, data=payload, files={"best.pt": best})
            if r.status_code != 200:
                LOGGER.info(f"{PREFIX}Unable to upload final models!")
        LOGGER.info(f"{PREFIX}🚀 View model at https://hub.ultralytics.com/models/{self.model_id}")
