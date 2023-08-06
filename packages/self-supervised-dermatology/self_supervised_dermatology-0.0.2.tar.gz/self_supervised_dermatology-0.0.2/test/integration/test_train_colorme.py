import yaml
import copy
import torch
import unittest
from pathlib import Path
from torchvision import datasets
from torch.utils.data import DataLoader, DistributedSampler

from src.datasets.wrappers.colorme_wrapper import ColorMeDatasetWrapper
from src.trainers.colorme_trainer import ColorMeTrainer
from src.utils.utils import compare_models
from src.utils.utils import fix_random_seeds, init_distributed_mode, cleanup
from src.utils.loader import Loader
from src.datasets.encrypted_image_folder import EncryptedImageFolder


class TestColorMeTraining(unittest.TestCase):
    def setUp(self):
        # set the paths
        self.config_path = Path('arguments') / 'colorme.yaml'
        # load config yaml
        self.config = yaml.load(open(self.config_path, "r"),
                                Loader=Loader)
        # change to "smoke test"
        self.config['batch_size'] = 8
        self.config['epochs'] = 1
        self.config['warmup_epochs'] = 0
        self.config['save_every_n_epochs'] = 1
        self.config['downstream_every_n_epochs'] = 1
        self.config['downstream_train_epochs'] = 1
        self.config['embed_vis_every_n_epochs'] = 1

        # initialize distribution
        init_distributed_mode()
        # seed everything
        fix_random_seeds(self.config['seed'])

    def tearDown(self):
        cleanup()

    def test_colorme_training(self):
        # load the datasets (train and val are the same for testing)
        val_path = self.config['dataset']['val_path']
        train_dataset = EncryptedImageFolder(
            val_path,
            enc_keys=self.config['decryption']['keys'],
            transform=None)
        train_dataset = ColorMeDatasetWrapper(
            train_dataset, **self.config['dataset']['wrapper'])
        sampler = DistributedSampler(train_dataset, shuffle=True)
        train_dataset = DataLoader(train_dataset,
                                   sampler=sampler,
                                   batch_size=self.config['batch_size'],
                                   **self.config['dataset']['val_loader'])

        val_dataset = datasets.ImageFolder(val_path, transform=None)
        val_dataset = ColorMeDatasetWrapper(
            val_dataset, **self.config['dataset']['wrapper'])
        val_dataset = DataLoader(val_dataset,
                                 batch_size=self.config['batch_size'],
                                 **self.config['dataset']['val_loader'])

        # initialize the trainer and train the model
        trainer = ColorMeTrainer(train_dataset,
                                 val_dataset,
                                 self.config,
                                 self.config_path,
                                 debug=True)
        start_model = copy.deepcopy(trainer.model)
        trainer.fit()

        # compare models (check that the models are not equal)
        end_model = copy.deepcopy(trainer.model)
        n_differs = compare_models(start_model, end_model)
        self.assertTrue(n_differs > 0)

        # check if the output is different between the models
        img_shape = eval(self.config['dataset']['wrapper']['target_shape'])
        img_shape = (1, 1, img_shape[0], img_shape[1])
        rand_img = torch.rand(img_shape).to(trainer.device)
        out_start = start_model(rand_img)
        out_end = end_model(rand_img)
        self.assertFalse(torch.equal(out_start[0], out_end[0]))
        self.assertFalse(torch.equal(out_start[1], out_end[1]))

        # check the ranges of the output
        self.assertAlmostEqual(out_start[1].sum().item(), 1.0)
        self.assertAlmostEqual(out_end[1].sum().item(), 1.0)


if __name__ == '__main__':
    unittest.main()
