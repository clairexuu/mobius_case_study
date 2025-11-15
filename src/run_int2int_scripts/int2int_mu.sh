# https://stackoverflow.com/a/13087801/1141805
function abspath {
    if [[ -d "$1" ]]
    then
        pushd "$1" >/dev/null
        pwd
        popd >/dev/null
    elif [[ -e "$1" ]]
    then
        pushd "$(dirname "$1")" >/dev/null
        echo "$(pwd)/$(basename "$1")"
        popd >/dev/null
    else
        echo "$1" does not exist! >&2
        return 127
    fi
}

# Parse encoding parameter (default: interCRT100)
ENCODING=${1:-interCRT100}
DATASET_TYPE=${2:-natural}

# Set encoding-specific parameters
if [ "$ENCODING" = "interCRT100" ]; then
    DATA_TYPES='int[200]:range(-1,2)'
    BASE_FILENAME="mu_interCRT100"
elif [ "$ENCODING" = "CRT100" ]; then
    DATA_TYPES='int[100]:range(-1,2)'
    BASE_FILENAME="mu_CRT100"
elif [ "$ENCODING" = "interCRT100_with_n" ]; then
    DATA_TYPES='int[201]:range(-1,2)'
    BASE_FILENAME="mu_interCRT100_with_n"
elif [ "$ENCODING" = "CRT100_with_stats" ]; then
    DATA_TYPES='int[103]:range(-1,2)'
    BASE_FILENAME="mu_CRT100_with_stats"
else
    echo "Unknown encoding: $ENCODING"
    exit 1
fi

# Construct filenames with dataset type
TRAIN_FILE="${BASE_FILENAME}_${DATASET_TYPE}.txt.train"
EVAL_FILE="${BASE_FILENAME}_${DATASET_TYPE}.txt.test"

INPUT_DIR="../../input/input_dir_${ENCODING}_${DATASET_TYPE}"
MODEL_DIR="../../models/model_${ENCODING}_${DATASET_TYPE}"

echo "Training with encoding: $ENCODING"
echo "  Dataset type: $DATASET_TYPE"
echo "  Data types: $DATA_TYPES"
echo "  Input directory: $INPUT_DIR"
echo "  Model directory: $MODEL_DIR"

mkdir -p "$MODEL_DIR"

# Use conda environment's Python directly
PYTHON_BIN="${CONDA_PREFIX:-/home/ziwen/miniconda3/envs/DLNT}/bin/python"

$PYTHON_BIN ../../Int2Int/train.py --seed 42 --env_base_seed 100 --num_workers 0 --dump_path "`abspath ${MODEL_DIR}`" --exp_name mu --exp_id 1 --train_data "`abspath ${INPUT_DIR}/${TRAIN_FILE}`" --eval_data "`abspath ${INPUT_DIR}/${EVAL_FILE}`" --eval_size 10000 --epoch_size 50000 --operation data --data_types "$DATA_TYPES" --optimizer 'adam_inverse_sqrt,lr=0.00025' --max_epoch 201
