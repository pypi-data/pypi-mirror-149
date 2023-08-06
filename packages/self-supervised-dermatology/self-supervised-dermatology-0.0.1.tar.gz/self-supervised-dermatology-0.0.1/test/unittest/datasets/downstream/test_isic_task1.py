import unittest
import numpy as np
from pathlib import Path
from PIL import Image
from typing import Tuple
from torchvision import transforms

from src.datasets.downstream.isic_task1_dataset import ISICTask1Dataset


class TestFitzpatrick17Dataset(unittest.TestCase):
    def setUp(self):
        self.data_path = Path('data/ISIC_Task1/')
        self.data_type = 'train'

    def test_iterator(self):
        dataset = ISICTask1Dataset(self.data_path, dataset_type=self.data_type)
        for sample in dataset:
            self.assertEqual(type(sample), tuple)
            self.assertEqual(len(sample), 2)
            self.assertEqual(type(sample[0]), Image.Image)
            self.assertEqual(type(sample[1]), Image.Image)
            self.assertIsNotNone(sample[0])
            self.assertIsNotNone(sample[1])
            img = np.asarray(sample[0])
            mask = np.asarray(sample[1])
            self.assertEqual(len(img.shape), 3)
            self.assertEqual(img.shape[-1], 3)
            self.assertEqual(len(mask.shape), 2)
            break

    def test_iterator_transform(self):
        transform = transforms.Resize((10, 10))
        dataset = ISICTask1Dataset(self.data_path,
                                   dataset_type=self.data_type,
                                   transform=transform,
                                   mask_transform=transform)
        for image, mask in dataset:
            self.assertIsNotNone(image)
            self.assertIsNotNone(mask)
            self.assertEqual((10, 10), image.size)
            self.assertEqual((10, 10), mask.size)
            break


if __name__ == '__main__':
    unittest.main()
