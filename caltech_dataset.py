from torchvision.datasets import VisionDataset

from PIL import Image

import os
import os.path
import sys

banned_classes = ['BACKGROUND_Google']

def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


def make_dataset(root, class_to_idx, split):
    instances = []
    parent_dir, _ = os.path.split(root)
    split_path =  os.path.join(parent_dir, split)
    
    with open(split_path) as f:
        for line in f:
            target_class, _ = os.path.split(line.strip('\n'))
            if target_class not in banned_class:
                class_index = class_to_idx[target_class]
                path = os.path.join(root, line.strip('\n'))
                item = path, class_index
                instances.append(item)
     
    return instances
            
    
class Caltech(VisionDataset):
    def __init__(self, root, split='train', transform=None, target_transform=None):
        super(Caltech, self).__init__(root, transform=transform, target_transform=target_transform)

        self.split = split # This defines the split you are going to use
                           # (split files are called 'train.txt' and 'test.txt')
        
        classes, class_to_idx = self._find_classes(self.root)
        samples = make_dataset(self.root, class_to_idx, self.split)
        
        if len(samples) == 0:
            raise (RuntimeError("Found 0 files in subfolders of: " + self.root))
        
        self.classes = classes
        self.class_to_idx = class_to_idx
        self.samples = samples
        self.targets = [s[1] for s in samples]
        
    def _find_classes(self, dir):
        """
        Finds the class folders in a dataset.

        Args:
            dir (string): Root directory path.

        Returns:
            tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.

        Ensures:
            No class is a subdirectory of another.
        """
        classes = [d.name for d in os.scandir(dir) if (d.is_dir() and (d.name not in banned_classes))]
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx


    def __getitem__(self, index):
        '''
        __getitem__ should access an element through its index
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        '''

        image, label = self.samples[index]
        image = pil_loader(image)

        # Applies preprocessing when accessing the image
        if self.transform is not None:
            image = self.transform(image)

        return image, label

    def __len__(self):
  
        length = len(self.samples)
        return length
