from ovary_analysis.train.ovary_seg import create_cross_validation

training_job_settings = {
    'n_cpus': 4,
    'mem_per_cpu': 6144,
    'n_gpus': 1,
    'job_time': [96, 0]
}

prediction_job_settings = {
    'n_cpus': 6,
    'mem_per_cpu': 6144,
    'n_gpus': 8,
    'job_time': [0, 30]
}

training_runner = '/cluster/home/kyamauch/.local/lib/python3.8/site-packages/pytorch3dunet/train.py'
prediction_runner = '/cluster/home/kyamauch/.local/lib/python3.8/site-packages/pytorch3dunet/predict.py'

create_cross_validation(
    data_table_path='/cluster/work/cobi/kevin/ivf/cross_validation_20211031/converted_data/ovary_datasets_20211101.csv',
    dataset_dir='/cluster/work/cobi/kevin/ivf/cross_validation_20211031/converted_data/ovary_datasets_20211101',
    training_config_path='/cluster/work/cobi/kevin/ivf/cross_validation_20211031/cross_validation_ovary_train_20211102.yaml',
    training_runner=training_runner,
    training_job_settings=training_job_settings,
    prediction_config_path='/cluster/work/cobi/kevin/ivf/cross_validation_20211031/crossvalidation_ovary_test_20211102.yaml',
    prediction_runner=prediction_runner,
    prediction_job_settings=prediction_job_settings,
    output_dir='/cluster/work/cobi/kevin/ivf/cross_validation_20211031/ovary_crossval',
    df_output_fname='ovary_crossvalidation_20211101.csv',
    n_folds=10,
    frac_train=0.89,
    random_seed=0
)