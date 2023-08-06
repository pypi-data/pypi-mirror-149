from ovary_analysis.train.follicle_seg import create_cross_validation_datasets

training_job_settings = {
    'n_cpus': 4,
    'mem_per_cpu': 6144,
    'n_gpus': 1,
    'job_time': [96, 0]
}

prediction_job_settings = {
    'n_cpus': 10,
    'mem_per_cpu': 6144,
    'n_gpus': 8,
    'job_time': [1, 30]
}

CROSSVAL_DIR = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/ovary_crossval'
OVARY_DATASETS_DIR = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/converted_data/ovary_datasets_20211101'
TRAINING_CONFIG_PATH = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/follicle_crossval_20211118/train_follicle_crossval_20211118.yaml'
PREDICTION_CONFIG_PATH = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/follicle_crossval_20211118/predict_follicle_crossval_20211118.yaml'
OUTPUT_BASE_DIR = '/cluster/work/cobi/kevin/ivf/cross_validation_20211031/follicle_crossval_20211118'

TRAINING_RUNNER = '/cluster/home/kyamauch/.local/lib/python3.8/site-packages/pytorch3dunet/train.py'
PREDICTION_RUNNER = '/cluster/home/kyamauch/.local/lib/python3.8/site-packages/pytorch3dunet/predict.py'

create_cross_validation_datasets(
    crossval_dir=CROSSVAL_DIR,
    ovary_data_table_name='ovary_crossvalidation_20211101.csv',
    follicle_data_table_name='follicle_cross_validation_20211118.csv',
    ovary_seg_dir_name='segmentations',
    ovary_datasets_dir=OVARY_DATASETS_DIR,
    training_config_path=TRAINING_CONFIG_PATH,
    training_runner=TRAINING_RUNNER,
    training_job_settings=training_job_settings,
    prediction_config_path=PREDICTION_CONFIG_PATH,
    prediction_runner=PREDICTION_RUNNER,
    prediction_job_settings=prediction_job_settings,
    output_base_dir=OUTPUT_BASE_DIR,
    raw_name='raw_rescaled',
    follicle_name='follicle_labels_rescaled',
    ovary_name='ovary_labels_rescaled',
    ovary_seg_name='ovary_segmentation_rescaled',
    weights_name='weights',
    mask_raw_im=False,
    min_shape=[80, 80, 80],
    follicle_erosion=2,
    follicle_dilation=8,
    ovary_weight=0.2,
    follicle_weight=0.2,
    boundary_weight=1,
)