import logging
import os
from typing import Type, Optional, Mapping, Any

import mlflow
import torch
from pytorch_lightning import LightningModule, Trainer

import sfu_torch_lib.io as io


logger = logging.getLogger(__name__)


def get_checkpoint_path(run_id: str, filename: str = 'last') -> Optional[str]:
    run = mlflow.get_run(run_id)

    checkpoint_path = os.path.join(run.info.artifact_uri, f'{filename}.ckpt')

    if not io.exists(checkpoint_path):
        return None

    return checkpoint_path


def get_localized_checkpoint_path(run_id: str, filename: str = 'last') -> Optional[str]:
    checkpoint_path = get_checkpoint_path(run_id, filename)
    checkpoint_path = io.localize_file(checkpoint_path) if checkpoint_path else None

    return checkpoint_path


def get_resumable_checkpoint_path(
        run_id: Optional[str],
        restart: bool = False,
        filename: str = 'last',
) -> Optional[str]:

    if restart or not run_id:
        return None

    checkpoint_path = get_localized_checkpoint_path(run_id, filename)

    if not checkpoint_path:
        run = mlflow.get_run(run_id)

        if len(run.data.metrics) > 0:
            logging.warning('Could not find checkpoint. The model will not be initialized.')

    return checkpoint_path


def load_model(run_id: str, module_class: Type[LightningModule], filename: str = 'last', **kwargs) -> LightningModule:
    checkpoint_path = get_checkpoint_path(run_id, filename)
    assert checkpoint_path

    with io.open(checkpoint_path) as checkpoint_file:
        model = module_class.load_from_checkpoint(checkpoint_file, **kwargs)

    return model


def load_trainer_state(trainer: Trainer, checkpoint: Mapping[str, Any], model: LightningModule) -> None:
    trainer.fit_loop.current_epoch = checkpoint['epoch']  # type: ignore
    trainer.fit_loop.global_step = checkpoint['global_step']  # type: ignore

    optimizers, _, _ = trainer.init_optimizers(model)

    for optimizer, state in zip(optimizers, checkpoint['optimizer_states']):
        optimizer.load_state_dict(state)

    for callback in trainer.callbacks:
        if callback.state_key in checkpoint['callbacks']:
            for key, value in checkpoint['callbacks'][callback.state_key].items():
                setattr(callback, key, value)


def load_state(run_id: str, model: LightningModule, trainer: Optional[Trainer] = None, filename: str = 'last') -> None:
    device = torch.device('cuda') if torch.cuda.device_count() else torch.device('cpu')

    checkpoint_path = get_checkpoint_path(run_id, filename)
    assert checkpoint_path

    with io.open(checkpoint_path) as checkpoint_file:
        checkpoint = torch.load(checkpoint_file, device)

    model.load_state_dict(checkpoint['state_dict'])

    if trainer:
        load_trainer_state(trainer, checkpoint, model)
