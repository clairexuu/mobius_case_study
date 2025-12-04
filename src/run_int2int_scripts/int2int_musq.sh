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

# Parse parameters (defaults: interCRT100, natural, mobius)
ENCODING=${1:-interCRT100}
DATASET_TYPE=${2:-natural}
FUNCTION=${3:-mobius}

# Set function-specific prefix
if [ "$FUNCTION" = "mobius" ]; then
    FUNC_PREFIX="musq"
    EXP_NAME="musq"
elif [ "$FUNCTION" = "liouville" ]; then
    FUNC_PREFIX="lambdasq"
    EXP_NAME="lambdasq"
else
    echo "Unknown function: $FUNCTION"
    exit 1
fi

# Set encoding-specific parameters
if [ "$ENCODING" = "interCRT100" ]; then
    DATA_TYPES='int[200]:range(-1,2)'
    BASE_FILENAME="${FUNC_PREFIX}_interCRT100"
elif [ "$ENCODING" = "CRT100" ]; then
    DATA_TYPES='int[100]:range(-1,2)'
    BASE_FILENAME="${FUNC_PREFIX}_CRT100"
elif [ "$ENCODING" = "interCRT100_with_n" ]; then
    DATA_TYPES='int[201]:range(-1,2)'
    BASE_FILENAME="${FUNC_PREFIX}_interCRT100_with_n"
elif [ "$ENCODING" = "CRT100_with_stats" ]; then
    DATA_TYPES='int[103]:range(-1,2)'
    BASE_FILENAME="${FUNC_PREFIX}_CRT100_with_stats"
else
    echo "Unknown encoding: $ENCODING"
    exit 1
fi

# Construct filenames with dataset type
TRAIN_FILE="${BASE_FILENAME}_${DATASET_TYPE}.txt.train"
EVAL_FILE="${BASE_FILENAME}_${DATASET_TYPE}.txt.test"

INPUT_DIR="../../input/input_dir_${ENCODING}_${DATASET_TYPE}"
MODEL_DIR="../../models/model_${ENCODING}_${DATASET_TYPE}_${FUNCTION}"

echo "Training with encoding: $ENCODING"
echo "  Function: $FUNCTION"
echo "  Dataset type: $DATASET_TYPE"
echo "  Data types: $DATA_TYPES"
echo "  Input directory: $INPUT_DIR"
echo "  Model directory: $MODEL_DIR"

mkdir -p "$MODEL_DIR"

# Use virtual environment's Python directly
PYTHON_BIN="${VIRTUAL_ENV:-../../venv}/bin/python"

# Workaround for Intel VTune/JIT library issue
export DISABLE_VTUNE=1

$PYTHON_BIN ../../Int2Int/train.py --env_base_seed 100 --num_workers 0 --dump_path "`abspath ${MODEL_DIR}`" --exp_name $EXP_NAME --exp_id 1 --train_data "`abspath ${INPUT_DIR}/${TRAIN_FILE}`" --eval_data "`abspath ${INPUT_DIR}/${EVAL_FILE}`" --eval_size 10000 --epoch_size 50000 --operation data --data_types "$DATA_TYPES" --optimizer 'adam_inverse_sqrt,lr=0.00025' --max_epoch 201 --batch_size 48
