from typing import Any, Dict, List, Union
import os
import yaml


def _load_config(config_path: Union[str, os.PathLike]) -> Dict[str, Any]:
    """Load a YAML configuration file.

    Parameters
    ----------
    config_path : Union[str, os.PathLike]
        The path to the configuration file.

    Returns
    -------
    config : Dict[str, Any]
        The configuration file loaded into a dictionary.
    """
    with open(config_path) as f_config:
        config = yaml.safe_load(f_config)
    return config


def _load_and_update_training_config(
    config_path: Union[str, os.PathLike],
    fold_index: int,
    checkpoint_dir: Union[str, os.PathLike],
    train_file_dir: List[Union[str, os.PathLike]],
    val_file_dir: List[Union[str, os.PathLike]],
    config_output_directory: Union[str, os.PathLike],
) -> str:
    """Load a template training config and update it with the file paths for
    a given experiment.

    The config should be in the format of the pytorch-3dunet library
    https://github.com/wolny/pytorch-3dunet

    Parameters
    ----------
    config_path : Union[str, os.PathLike]
        The path to the template config file.
    fold_index : int
        The index of the fold the prediction config is being updated for.
    checkpoint_dir: Union[str, os.PathLike]
        The directory in which to save the checkpoint files.
    train_file_dir: List[Union[str, os.PathLike]]
        The directory containing the data for training.
    val_file_dir: List[Union[str, os.PathLike]]
        The directory the containing the data for vaildation.
    config_output_directory: Union[str, os.PathLike]
        The directory in which to save the updated config file.

    Returns
    -------
    updated_config_path : str
        The path to which the updated config file was saved.
    """
    config = _load_config(config_path)

    # update checkpoint_dir
    if not os.path.isdir(checkpoint_dir):
        os.mkdir(checkpoint_dir)
    config['trainer']['checkpoint_dir'] = checkpoint_dir

    # update train file paths
    for directory in train_file_dir:
        assert os.path.isdir(directory)
    config['loaders']['train']['file_paths'] = train_file_dir

    # update validation file paths
    for directory in val_file_dir:
        assert os.path.isdir(directory)
    config['loaders']['val']['file_paths'] = val_file_dir

    # save the updated file
    config_name = os.path.basename(config_path).replace(
        '.yaml', f'_fold_{fold_index}.yaml'
    )
    updated_config_path = os.path.join(config_output_directory, config_name)
    with open(updated_config_path, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    return updated_config_path


def _load_and_update_prediction_config(
    config_path: Union[str, os.PathLike],
    fold_index: int,
    model_path: Union[str, os.PathLike],
    image_files: List[Union[str, os.PathLike]],
    prediction_output_directory: Union[str, os.PathLike],
    config_output_directory: Union[str, os.PathLike],
) -> str:
    """Load a template prediction config and update it with the model and file paths for
    a given experiment.

    The config should be in the format of the pytorch-3dunet library
    https://github.com/wolny/pytorch-3dunet

    Parameters
    ----------
    config_path : Union[str, os.PathLike]
        The path to the template config file.
    fold_index : int
        The index of the fold the prediction config is being updated for.
    model_path : Union[str, os.PathLike]
        The path to the model to use for prediction.
    image_files : List[Union[str, os.PathLike]]
        The list of folders to make predictions on.
    prediction_output_directory : Union[str, os.PathLike]
        The directory the predictions will be saved to.
    config_output_directory: Union[str, os.PathLike]
        The directory in which to save the updated config file.

    Returns
    -------
    updated_config_path : str
        The path to which the updated config file was saved.
    """
    config = _load_config(config_path)

    # update model path
    if model_path is not None:
        config['model_path'] = model_path

    # update the prediction output directory
    config['loaders']['output_dir'] = prediction_output_directory

    # update image file paths
    config['loaders']['test']['file_paths'] = image_files

    # save the updated file
    config_name = os.path.basename(config_path).replace(
        '.yaml', f'_fold_{fold_index}.yaml'
    )
    updated_config_path = os.path.join(config_output_directory, config_name)
    with open(updated_config_path, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    return updated_config_path
