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


mkdir -p ../../models/

# Use conda environment's Python directly
PYTHON_BIN="${CONDA_PREFIX:-/home/ziwen/miniconda3/envs/DLNT}/bin/python"

$PYTHON_BIN ../../Int2Int/train.py --num_workers 0 --dump_path "`abspath ../../models/`" --exp_name basic --exp_id 1 --train_data "`abspath ../../input/mu_modp_and_p.txt.train`" --eval_data "`abspath ../../input/mu_modp_and_p.txt.test`" --eval_size 10000 --epoch_size 50000 --operation data --data_types 'int[200]:range(-1,2)' --optimizer 'adam_inverse_sqrt,lr=0.00025' --max_epoch 201 --cpu True
