import glob
import os
from typing import Union, List, Dict, Any, Tuple

TRAIN_SCRIPT_TEMPLATE = """
#!/bin/bash

# load the python module
module load gcc/6.3.0 python_gpu/3.8.5

python {train_runner} --config {config_path}
"""

PREDICT_SCRIPT_TEMPLATE = """
#!/bin/bash

# load the python env
module load gcc/6.3.0 python_gpu/3.8.5

python {predict_runner} --config {config_path}
"""

SUBMISSION_FILE_STUB = """
#!/bin/bash

env2lmod

# load the python env
module load gcc/6.3.0 python_gpu/3.8.5

"""
SUBMISSION_LINE_TEMPLATE = (
    'bsub -n {n_cpus} -W {hours:02d}:{minutes:02d} -N -B '
    + '-J "{job_name}" -R "rusage[mem={mem_per_cpu}, ngpus_excl_p={n_gpus}]" '
    + '-R "select[gpu_model0==GeForceRTX2080Ti]" < {runner_path}\n'
)


def _write_predict_script(
    predict_runner: str,
    config_path: Union[str, os.PathLike],
    output_dir: Union[str, os.PathLike],
) -> str:
    """Write the bash script to run prediction

    Parameters
    ----------
    predict_runner : str
        The command to call the predict runner. This us generally a bash
        or python script.
    config_path : Union[str, os.PathLike]
        The path to the configuration file.
    output_dir : Union[str, os.PathLike]
        The path to folder the bash script will be saved.

    Returns
    -------
    script_path : str
        The path the bash script was saved to.
    """
    predict_script = PREDICT_SCRIPT_TEMPLATE.format(
        predict_runner=predict_runner, config_path=config_path
    )
    script_path = os.path.join(output_dir, 'run_prediction.sh')
    with open(script_path, 'w') as out_file:
        out_file.write(predict_script)

    return script_path


def _write_train_script(
    train_runner: str,
    config_path: Union[str, os.PathLike],
    output_dir: Union[str, os.PathLike],
) -> str:
    """Write the bash script to run prediction

    Parameters
    ----------
    train_runner : str
        The command to call the train runner. This us generally a bash
        or python script.
    config_path : Union[str, os.PathLike]
        The path to the configuration file.
    output_dir : Union[str, os.PathLike]
        The path to folder the bash script will be saved.

    Returns
    -------
    script_path : str
        The path the bash script was saved to.
    """
    train_script = TRAIN_SCRIPT_TEMPLATE.format(
        train_runner=train_runner, config_path=config_path
    )
    script_path = os.path.join(output_dir, 'run_training.sh')
    with open(script_path, 'w') as out_file:
        out_file.write(train_script)

    return script_path


def _write_submission_script(
    runner_paths: List[str],
    n_cpus: int,
    mem_per_cpu: int,
    n_gpus: int,
    job_time: List[int],
    job_prefix: str,
    script_path: Union[str, os.PathLike],
):
    """Write a script to submit a batch of jobs

    Parameters
    ----------
    runner_paths : List[str]
        The list of paths to the runner scripts to submit.
    n_cpus : int
        The number of CPUS to request for each job.
    mem_per_cpu : int
        The amount of RAM per CPU to request in MB.
    n_gpus : int
        The number of GPUS to request.
    job_time : List[int]
        The maximum job wall clock time in [hours, minutes].
    job_prefix : str
        The prefix used for naming the job. Job names will be
        {job_prefix}_i
    script_path : Union[str, os.PathLike]
        The path to save the script to.
    """
    submission_script = SUBMISSION_FILE_STUB

    for i, runner in enumerate(runner_paths):
        job_name = job_prefix + f'_{i}'
        submission_line = SUBMISSION_LINE_TEMPLATE.format(
            n_cpus=n_cpus,
            mem_per_cpu=mem_per_cpu,
            hours=job_time[0],
            minutes=job_time[1],
            n_gpus=n_gpus,
            job_name=job_name,
            runner_path=runner,
        )
        submission_script += submission_line

    with open(script_path, 'w') as out_file:
        out_file.write(submission_script)


def write_batch_submission_script(
    submission_script_path: str,
    runner_scripts: List[str],
    job_prefix: str,
    job_settings: Dict[str, Any],
):
    """Write a submission script for a set of jobs.

    Parameters
    ----------
    submission_script_path : str
        The path to which the submission script will be saved.
    runner_scripts : List[str]
        The list of runners to submit as jobs. One job will be created for
        each runner script.
    job_prefix : str
        The name to prepend to each submitted job.
    job_settings : Dict[str, Any]
        The LSF job settings for each job.
    """

    job_settings.update(
        {
            'runner_paths': runner_scripts,
            'job_prefix': job_prefix,
            'script_path': submission_script_path,
        }
    )
    _write_submission_script(**job_settings)


def _get_fold_index(fold_path: str, separator: str = '_') -> int:
    """Get the fold index from a fold directory (used for crossval).

    Parameters
    ----------
    fold_path : str
        The path to the folder
    separator : str
        The separator to split the folder name by. The last segment
        of the split string is returned as the fold index.
        The default value is '_'

    Returns
    -------
    fold_index : int
        The index for the fold contained in fold_path.
    """
    folder_name = os.path.basename(fold_path)
    return int(folder_name.split(separator)[-1])


def get_fold_directories(
    base_dir: str, fold_dir_pattern: str = 'fold_*'
) -> List[Tuple[int, str]]:
    """

    Parameters
    ----------
    base_dir : str
        The base directory containing the crossvalidation folds.
    fold_dir_pattern : str
        The pattern used to filter for fold directories. This is
        passed to glob. Default value is 'fold_*'

    Returns
    -------
    fold_dirs : List[Tuple[int, str]]
        The fold indices and folder directories. Each tuple is
        (fold_index, fold_dir).
    """
    folder_pattern = os.path.join(base_dir, fold_dir_pattern)
    fold_candidates = glob.glob(folder_pattern)

    # make sure they are directories
    fold_dirs = [
        (_get_fold_index(f), f) for f in fold_candidates if os.path.isdir(f)
    ]

    return fold_dirs
