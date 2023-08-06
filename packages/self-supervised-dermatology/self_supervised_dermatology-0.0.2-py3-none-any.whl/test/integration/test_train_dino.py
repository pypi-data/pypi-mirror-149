import yaml
import copy
import torch
import unittest
from pathlib import Path
from torchvision import datasets
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import transforms

from src.augmentations.dino import DINODataAugmentation
from src.trainers.dino_trainer import DINOTrainer
from src.utils.utils import compare_models
from src.utils.utils import fix_random_seeds, init_distributed_mode, cleanup
from src.utils.loader import Loader
from src.datasets.encrypted_image_folder import EncryptedImageFolder


class TestDINOTraining(unittest.TestCase):
    def setUp(self):
        # set the paths
        self.config_path = Path('arguments') / 'dino.yaml'
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

    def test_training(self):
        # load the datasets (train and val are the same for testing)
        val_path = self.config['dataset']['val_path']
        transform = DINODataAugmentation(**self.config['dataset']['augmentations'])
        val_transform = transforms.Compose([
            transforms.Resize(256, interpolation=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])

        train_dataset = EncryptedImageFolder(
            val_path,
            enc_keys=self.config['decryption']['keys'],
            transform=transform)
        sampler = DistributedSampler(train_dataset, shuffle=True)
        train_dataset = DataLoader(train_dataset,
                                   sampler=sampler,
                                   batch_size=self.config['batch_size'],
                                   **self.config['dataset']['val_loader'])
        val_dataset = datasets.ImageFolder(val_path, transform=val_transform)
        val_dataset = DataLoader(val_dataset,
                                 batch_size=self.config['batch_size'],
                                 **self.config['dataset']['val_loader'])

        # initialize the trainer and train the model
        trainer = DINOTrainer(train_dataset,
                              val_dataset,
                              self.config,
                              self.config_path,
                              debug=True)
        start_model = copy.deepcopy(trainer.student).to(trainer.device)
        trainer.fit()

        # compare models (check that the models are not equal)
        end_model = trainer.student.to(trainer.device)
        n_differs = compare_models(start_model, end_model)
        self.assertTrue(n_differs > 0)

        # check if the output is different between the models
        img_shape = (1, 3, 224, 224)
        rand_img = torch.rand(img_shape).to(trainer.device)
        out_start = start_model(rand_img)
        out_end = end_model(rand_img)
        self.assertFalse(torch.equal(out_start, out_end))


if __name__ == '__main__':
    unittest.main()
