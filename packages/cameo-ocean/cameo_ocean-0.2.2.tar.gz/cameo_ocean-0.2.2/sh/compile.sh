source .env/bin/activate
unset CONDA_PREFIX
maturin develop --release
sh/du.sh
