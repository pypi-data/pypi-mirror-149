import os
import torch
import tempfile
import numpy as np
import torchvision.models as models
import segmentation_models_pytorch as smp
from collections import OrderedDict

from ..models.vit.vision_transformer import vit_tiny


class Embedder:
    base_path = 'https://github.com/vm02-self-supervised-dermatology/self-supervised-models/raw/main'

    @staticmethod
    def load_resnet(ssl: str, debug: bool = False):
        if ssl in ['byol', 'simclr', 'colorme']:
            return Embedder.load_pretrained(ssl=ssl, debug=debug)
        else:
            raise ValueError('The given SSL model to load has not a ResNet architecture.')

    @staticmethod
    def load_vit(ssl: str, debug: bool = False):
        if ssl in ['dino', 'ibot']:
            return Embedder.load_pretrained(ssl=ssl, debug=debug)
        else:
            raise ValueError('The given SSL model to load has not a ViT architecture.')

    @staticmethod
    def load_pretrained(ssl: str, debug: bool = False):
        # get the model url
        model_url = Embedder.get_model_url(ssl)
        # download the model checkpoint
        with tempfile.NamedTemporaryFile() as tmp:
            torch.hub.download_url_to_file(model_url, tmp.name, progress=True)
            # get the loader function
            loader_func = Embedder.get_model_func(ssl)
            # load the model
            model = loader_func(ckp_path=tmp.name, debug=debug)
            # set the model in evaluation mode
            model.eval()
        return model

    @staticmethod
    def get_model_url(ssl: str):
        model_dict = {
            'byol': f'{Embedder.base_path}/byol/checkpoint-epoch100.pth',
            'simclr': f'{Embedder.base_path}/simclr/checkpoint-epoch100.pth',
            'colorme': f'{Embedder.base_path}/colorme/checkpoint-epoch100.pth',
            'dino': f'{Embedder.base_path}/dino/checkpoint-epoch100.pth',
            'ibot': f'{Embedder.base_path}/ibot/model_best.pth',
        }
        # get the model url
        model_url = model_dict.get(ssl, np.nan)
        if model_url is np.nan:
            raise ValueError('Unrecognized model name.')
        return model_url

    @staticmethod
    def get_model_func(ssl: str):
        model_dict_func = {
            'simclr': Embedder.load_simclr,
            'byol': Embedder.load_byol,
            'colorme': Embedder.load_colorme,
            'dino': Embedder.load_dino,
            'ibot': Embedder.load_ibot,
        }
        model_func = model_dict_func.get(ssl, np.nan)
        if model_func is np.nan:
            raise ValueError('Unrecognized model name.')
        return model_func

    @staticmethod
    def load_simclr(ckp_path: str, debug: bool = False):
        # load a dummy model
        model = models.resnet50(pretrained=False)
        # ResNet Model without last layer
        model = torch.nn.Sequential(*list(model.children())[:-1])
        # load the trained model
        Embedder.restart_from_checkpoint(
            ckp_path,
            state_dict=model,
            replace_ckp_str='model.',
            debug=debug,
        )
        return model

    @staticmethod
    def load_byol(ckp_path: str, debug: bool = False):
        # load a dummy model
        model = models.resnet50(pretrained=False)
        # load the trained model
        Embedder.restart_from_checkpoint(
            ckp_path,
            state_dict=model,
            replace_ckp_str='model.',
            debug=debug,
        )
        # ResNet Model without last layer
        model = torch.nn.Sequential(*list(model.children())[:-1])
        return model

    @staticmethod
    def load_colorme(ckp_path: str, debug: bool = False):
        # load a dummy model
        model = smp.Unet(encoder_name='resnet50', in_channels=1, classes=2)
        model = model.encoder
        # load the trained model
        Embedder.restart_from_checkpoint(
            ckp_path,
            state_dict=model,
            replace_ckp_str='enc_dec_model.encoder.',
            debug=debug,
        )
        return model

    @staticmethod
    def load_dino(ckp_path: str, debug: bool = False):
        # load a dummy model
        model = vit_tiny()
        # load the trained model
        Embedder.restart_from_checkpoint(
            ckp_path,
            student=model,
            replace_ckp_str='module.backbone.',
            debug=debug,
        )
        return model

    @staticmethod
    def load_ibot(ckp_path: str, debug: bool = False):
        # load a dummy model
        model = vit_tiny()
        # load the trained model
        Embedder.restart_from_checkpoint(
            ckp_path,
            student=model,
            replace_ckp_str='module.backbone.',
            debug=debug,
        )
        return model

    @staticmethod
    def restart_from_checkpoint(ckp_path,
                                run_variables=None,
                                replace_ckp_str='module.',
                                debug=False,
                                **kwargs):
        if not os.path.isfile(ckp_path):
            print("Pre-trained weights not found. Training from scratch.")
            return
        print("Found checkpoint at {}".format(ckp_path))

        # open checkpoint file
        checkpoint = torch.load(ckp_path, map_location="cpu")

        # key is what to look for in the checkpoint file
        # value is the object to load
        # example: {'state_dict': model}
        for key, value in kwargs.items():
            if key in checkpoint and value is not None:
                try:
                    msg = value.load_state_dict(checkpoint[key], strict=False)
                    if type(msg) is torch.nn.modules.module._IncompatibleKeys:
                        k = next(iter(checkpoint[key]))
                        if replace_ckp_str in k:
                            if debug:
                                print(f'=> Found `module` in {key}, trying to transform.')
                            transf_state_dict = OrderedDict()
                            for k, v in checkpoint[key].items():
                                # remove the module from the key
                                # this is caused by the distributed training
                                k = k.replace(replace_ckp_str, '')
                                transf_state_dict[k] = v
                            msg = value.load_state_dict(transf_state_dict,
                                                        strict=False)
                    if debug:
                        print("=> loaded '{}' from checkpoint '{}' with msg {}".
                              format(key, ckp_path, msg))
                except TypeError:
                    try:
                        msg = value.load_state_dict(checkpoint[key])
                        print("=> loaded '{}' from checkpoint: '{}'".format(key, ckp_path))
                    except ValueError:
                        print("=> failed to load '{}' from checkpoint: '{}'".format(key, ckp_path))
            else:
                print("=> key '{}' not found in checkpoint: '{}'".format(key, ckp_path))

        # reload variable important for the run
        if run_variables is not None:
            for var_name in run_variables:
                if var_name in checkpoint:
                    run_variables[var_name] = checkpoint[var_name]
