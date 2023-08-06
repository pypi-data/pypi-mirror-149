source .env/bin/activate
unset CONDA_PREFIX
python3 -m pip install cameo_ocean --upgrade
python3 -c 'import cameo_ocean;cameo_ocean.actix_server("0.0.0.0",20430)'
