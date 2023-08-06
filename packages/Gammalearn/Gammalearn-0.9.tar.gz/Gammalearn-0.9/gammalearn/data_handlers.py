import logging
import torch.multiprocessing as mp
from functools import partial
import tqdm

from pytorch_lightning import LightningDataModule
import torch
from torch.utils.data import DataLoader, Dataset, ConcatDataset, Subset
from torchvision import transforms
from gammalearn.datasets import DADataset

from gammalearn import utils as utils
from gammalearn.logging import LOGGING_CONFIG


def create_dataset_worker(file,
                          dataset_class,
                          train,
                          **kwargs):
    torch.set_num_threads(1)
    # Reload logging config (lost by spawn)
    logging.config.dictConfig(LOGGING_CONFIG)

    if utils.is_datafile_healthy(file):
        dataset = dataset_class(file,
                                train=train,
                                **kwargs
                                )
        if kwargs.get('image_filter') is not None:
            dataset.filter_image(kwargs.get('image_filter'))
        if kwargs.get('event_filter') is not None:
            dataset.filter_event(kwargs.get('event_filter'))
        if len(dataset) > 0:
            return dataset


def create_datasets(datafiles_list, experiment, train=True, **kwargs):
    """
    Create datasets from datafiles list, data are loaded in memory.
    Parameters
    ----------
    datafiles (List) : files to load data from
    experiment (Experiment): the experiment

    Returns
    -------
    Datasets
    """

    logger = logging.getLogger('gammalearn')
    assert datafiles_list, 'The data file list is empty !'

    logger.info('length of data file list : {}'.format(len(datafiles_list)))
    # We get spawn context because fork can cause deadlock in sub-processes
    # in multi-threaded programs (especially with logging)
    ctx = mp.get_context('spawn')
    if experiment.preprocessing_workers > 0:
        num_workers = experiment.preprocessing_workers
    else:
        num_workers = 1
    pool = ctx.Pool(processes=num_workers)
    datasets = list(tqdm.tqdm(pool.imap(partial(create_dataset_worker,
                                                dataset_class=experiment.dataset_class,
                                                train=train,
                                                **kwargs),
                                        datafiles_list),
                              total=len(datafiles_list),
                              desc='Load data files'
                              )
                    )

    return datasets


def split_dataset(datasets, ratio):
    """Split a list of datasets into a train and a validation set
    Parameters
    ----------
    datasets (list of Dataset): the list of datasets
    ratio (float): the ratio of data for validation

    Returns
    -------
    train set, validation set

    """
    # Creation of subset train and test
    assert 1 > ratio > 0, 'Validating ratio must be greater than 0 and smaller than 1.'

    train_max_index = int(len(datasets) * (1 - ratio))
    shuffled_indices = torch.randperm(len(datasets)).numpy()
    assert isinstance(datasets, Dataset)
    train_datasets = Subset(datasets, shuffled_indices[:train_max_index])
    val_datasets = Subset(datasets, shuffled_indices[train_max_index:])

    return train_datasets, val_datasets


def get_dataset_from_path(experiment, logger, data_type='source', train=True):
    if train:
        data_module = experiment.data_module_train[data_type]
    else:
        data_module = experiment.data_module_test[data_type]

    file_list = utils.find_datafiles(data_module['paths'], experiment.files_max_number)

    if train:
        logger.debug(file_list)

    file_list = list(file_list)
    file_list.sort()

    datasets = create_datasets(file_list, experiment, train=train, **data_module, **experiment.dataset_parameters)

    if train:
        return ConcatDataset(datasets)
    else:
        if experiment.merge_test_datasets:
            particle_dict = {}

            for dset in datasets:
                if dset.simu:
                    particle_type = dset.dl1_params['mc_type'][0]

                    if particle_type in particle_dict:
                        particle_dict[particle_type].append(dset)
                    else:
                        particle_dict[particle_type] = [dset]
                else:
                    if 'real_list' in particle_dict:
                        particle_dict['real_list'].append(dset)
                    else:
                        particle_dict['real_list'] = [dset]

            return [ConcatDataset(dset) for dset in particle_dict.values()]
        else:
            return datasets


def get_DA_dataset(experiment, logger, train=True):
    source_datasets = get_dataset_from_path(experiment, logger, data_type='source', train=train)
    target_datasets = get_dataset_from_path(experiment, logger, data_type='target', train=train)

    max_index = min(len(source_datasets), len(target_datasets))
    shuffled_indices_source = torch.randperm(len(source_datasets)).numpy()
    shuffled_indices_target = torch.randperm(len(target_datasets)).numpy()

    source_datasets = Subset(source_datasets, shuffled_indices_source[:max_index])
    target_datasets = Subset(target_datasets, shuffled_indices_target[:max_index])

    return DADataset(source_datasets, target_datasets)


class BaseDataModule(LightningDataModule):
    """
    Create datasets and dataloaders.
    Parameters
    ----------
    experiment (Experiment): the experiment

    Returns
    -------
    """
    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment
        self.logger = logging.getLogger(__name__)
        self.train_set = None
        self.val_set = None
        self.test_sets = None

    def setup(self, stage=None):
        raise NotImplementedError

    def train_dataloader(self):
        training_loader = DataLoader(self.train_set,
                                     batch_size=self.experiment.batch_size,
                                     shuffle=True,
                                     drop_last=True,
                                     num_workers=self.experiment.dataloader_workers,
                                     pin_memory=self.experiment.pin_memory)
        self.logger.info('training loader length : {} batches'.format(len(training_loader)))
        return training_loader

    def val_dataloader(self):
        validating_loader = DataLoader(self.val_set,
                                       batch_size=self.experiment.batch_size,
                                       shuffle=False,
                                       num_workers=self.experiment.dataloader_workers,
                                       drop_last=False,
                                       pin_memory=self.experiment.pin_memory)
        self.logger.info('validating loader length : {} batches'.format(len(validating_loader)))
        return validating_loader

    def test_dataloaders(self):
        test_loaders = [DataLoader(test_set, batch_size=self.experiment.test_batch_size, shuffle=False,
                                   drop_last=False, num_workers=self.experiment.dataloader_workers)
                        for test_set in self.test_sets]
        self.logger.info('test loader length : {} batches'.format(torch.tensor([len(t) for t in test_loaders]).sum()))
        return test_loaders


class GLearnDataModule(BaseDataModule):
    """
    Create datasets and dataloaders.
    Parameters
    ----------
    experiment (Experiment): the experiment

    Returns
    -------
    """
    def __init__(self, experiment):
        super().__init__(experiment)

    def setup(self, stage=None):

        self.logger.info('Start creating datasets')

        if self.experiment.train:
            self.logger.info('look for data files')

            if not self.experiment.data_module_train['target']['paths']: # source only
                datasets = get_dataset_from_path(self.experiment, self.logger)
            else: # source + target
                datasets = get_DA_dataset(self.experiment, self.logger)

            assert datasets, 'Dataset is empty !'

            # Creation of subset train and test
            train_datasets, val_datasets = split_dataset(datasets, self.experiment.validating_ratio)

            self.train_set = train_datasets
            self.logger.info('training set length : {}'.format(len(self.train_set)))

            self.val_set = val_datasets
            try:
                assert len(self.val_set) > 0
            except AssertionError as e:
                self.logger.exception('Validating set must contain data')
                raise e
            self.logger.info('validating set length : {}'.format(len(self.val_set)))
        else:
            self.train_set = None
            self.val_set = None
        if self.experiment.test:
            if self.experiment.data_module_test is not None:
                # Look for specific data parameters
                if self.experiment.test_dataset_parameters is not None:
                    self.experiment.dataset_parameters.update(self.experiment.test_dataset_parameters)
                # Create data sets
                self.test_sets = get_dataset_from_path(self.experiment, self.logger, train=False)
                if self.experiment.data_module_test['target']['paths']: # if target are provided
                    self.test_sets.extend(get_dataset_from_path(self.experiment, self.logger, data_type='target', train=False))
            else:
                assert self.val_set is not None, 'Test is required but no test file is provided and val_set is None'
                self.test_sets = [self.val_set]
            self.logger.info('test set length : {}'.format(torch.tensor([len(t) for t in self.test_sets]).sum()))
