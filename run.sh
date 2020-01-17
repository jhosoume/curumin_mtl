python3.6 -m venv venv
source venv/bin/activate
pip install -e .
python examples/automl/toy.py data=abalone3.arff storage=sqlite db=/tmp/paje iter=10 seed=123
deactivate 
