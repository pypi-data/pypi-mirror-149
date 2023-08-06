import yaml
import argparse
from pathlib import Path

from src.trainers.simclr_trainer import SimCLRTrainer
from src.trainers.byol_trainer import BYOLTrainer
from src.trainers.colorme_trainer import ColorMeTrainer
from src.trainers.dino_trainer import DINOTrainer
from src.trainers.ibot_trainer import iBOTTrainer
from src.trainers.imagenet_trainer import ImageNetTrainer
from src.utils.utils import fix_random_seeds
from src.utils.loader import Loader

my_parser = argparse.ArgumentParser(
    description='Evaluates SSL models on downstream tasks.')
my_parser.add_argument('--config_path',
                       type=str,
                       required=True,
                       help='Path to the config yaml.')
args = my_parser.parse_args()

if __name__ == "__main__":
    # load config yaml
    args.config_path = Path(args.config_path)
    if not args.config_path.exists():
        raise ValueError(
            f'Unable to find config yaml file: {args.config_path}')
    config = yaml.load(open(args.config_path, "r"), Loader=Loader)

    # seed everything
    fix_random_seeds(config['seed'])

    # get the correct trainer
    trainer_dict = {
        'ImageNet': ImageNetTrainer,
        'SimCLR': SimCLRTrainer,
        'BYOL': BYOLTrainer,
        'ColorMe': ColorMeTrainer,
        'DINO': DINOTrainer,
        'iBOT': iBOTTrainer,
    }
    trainer_cls = trainer_dict.get(config['SSL_model'], None)
    if trainer_cls is None:
        raise ValueError('Unknown SSL model.')

    # initialize the trainer
    trainer = trainer_cls(None,
                          None,
                          config,
                          args.config_path,
                          evaluation=True)

    # evaluate
    trainer.eval()
