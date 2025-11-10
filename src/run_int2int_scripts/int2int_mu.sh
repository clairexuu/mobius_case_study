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

# Set encoding-specific parameters
if [ "$ENCODING" = "interCRT100" ]; then
    DATA_TYPES='int[200]:range(-1,2)'
    TRAIN_FILE="mu_modp_and_p.txt.train"
    EVAL_FILE="mu_modp_and_p.txt.test"
elif [ "$ENCODING" = "CRT100" ]; then
    DATA_TYPES='int[100]:range(-1,2)'
    TRAIN_FILE="mu_CRT100.txt.train"
    EVAL_FILE="mu_CRT100.txt.test"
elif [ "$ENCODING" = "interCRT100_with_n" ]; then
    DATA_TYPES='int[201]:range(-1,2)'
    TRAIN_FILE="mu_interCRT100_with_n.txt.train"
    EVAL_FILE="mu_interCRT100_with_n.txt.test"
elif [ "$ENCODING" = "CRT100_with_stats" ]; then
    DATA_TYPES='int[103]:range(-1,2)'
    TRAIN_FILE="mu_CRT100_with_stats.txt.train"
    EVAL_FILE="mu_CRT100_with_stats.txt.test"
else
    echo "Unknown encoding: $ENCODING"
    exit 1
fi

INPUT_DIR="../../input/input_dir_${ENCODING}"
MODEL_DIR="../../models/model_${ENCODING}"

echo "Training with encoding: $ENCODING"
echo "  Data types: $DATA_TYPES"
echo "  Input directory: $INPUT_DIR"
echo "  Model directory: $MODEL_DIR"

mkdir -p "$MODEL_DIR"

# Use conda environment's Python directly
PYTHON_BIN="${CONDA_PREFIX:-/home/ziwen/miniconda3/envs/DLNT}/bin/python"

$PYTHON_BIN ../../Int2Int/train.py --seed 42 --env_base_seed 100 --num_workers 0 --dump_path "`abspath ${MODEL_DIR}`" --exp_name mu --exp_id 1 --train_data "`abspath ${INPUT_DIR}/${TRAIN_FILE}`" --eval_data "`abspath ${INPUT_DIR}/${EVAL_FILE}`" --eval_size 10000 --epoch_size 50000 --operation data --data_types "$DATA_TYPES" --optimizer 'adam_inverse_sqrt,lr=0.00025' --max_epoch 201
