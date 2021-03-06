# PyTorch StudioGAN: https://github.com/POSTECH-CVLab/PyTorch-StudioGAN
# The MIT License (MIT)
# See license file or visit https://github.com/POSTECH-CVLab/PyTorch-StudioGAN for details

# main.py


from argparse import ArgumentParser
import json
import os

from make_hdf5 import make_hdf5
from train import train_framework



def main():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-c', '--config_path', type=str, default='./configs/Table1/contra_biggan_cifar32_hinge_no.json')
    parser.add_argument('--checkpoint_folder', type=str, default=None)
    parser.add_argument('--load_current', type=bool, default=True, help='choose whether you load current or best weights')
    parser.add_argument('--log_output_path', type=str, default=None)

    parser.add_argument('--seed', type=int, default=0, help='seed for generating random number')
    parser.add_argument('--num_workers', type=int, default=8, help='')
    
    parser.add_argument('--reduce_train_dataset', type=float, default=1.0, help='control the number of train dataset')
    parser.add_argument('-l', '--load_all_data_in_memory', action='store_true')
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-e', '--eval', action='store_true')
    parser.add_argument('-knn', '--k_nearest_neighbor', action='store_true', help='select whether conduct k-nearest neighbor analysis')
    parser.add_argument('-knn_mode', '--criterion_4_k_nearest_neighbor', type=str, default="real", help='[real, fake]: select a type of an anchor image for K-NN analysis')
    parser.add_argument('-k', '--number_of_nearest_samples', type=int, default=1, help='"k"NN')

    parser.add_argument('--print_every', type=int, default=100, help='control log interval')
    parser.add_argument('--save_every', type=int, default=2000, help='control evaluation and save interval')
    parser.add_argument('--type4eval_dataset', type=str, default='test', help='[train/valid/test]')
    args = parser.parse_args()

    if args.config_path is not None:
        with open(args.config_path) as f:
            model_config = json.load(f)
        train_config = vars(args)
    else:
        raise NotImplementedError
    
    dataset = model_config['data_processing']['dataset_name']
    if dataset == 'cifar10':
        assert args.type4eval_dataset == 'train' or args.type4eval_dataset == 'test', "cifar10 does not contain dataset for validation"
    elif dataset == 'imagenet' or dataset == 'tiny imagenet':
        if args.type4eval_dataset == 'test':
            raise NotImplementedError

    hdf5_path_train = make_hdf5(**model_config['data_processing'], **train_config, mode='train') if args.load_all_data_in_memory else None
    
    train_framework(**train_config,
                    **model_config['data_processing'],
                    **model_config['train']['model'],
                    **model_config['train']['optimization'],
                    **model_config['train']['loss_function'],
                    **model_config['train']['initialization'],
                    **model_config['train']['training_and_sampling_setting'],
                    train_config=train_config, model_config=model_config['train'], hdf5_path_train=hdf5_path_train)

if __name__ == '__main__':
    main()
