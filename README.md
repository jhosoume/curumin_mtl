# curumim

Install
-------

    sudo apt install python3.7-dev    # For Debian-like systems.
    git clone https://github.com/automated-data-science/curumim-automl-sandbox/
    cd curumim-automl-sandbox/
    python3.7 -m venv venv
    source venv/bin/activate
    pip install -e .
    deactivate
    cd ..

Use
---

    cd curumim-automl-sandbox/
    source venv/bin/activate
    python examples/automl/toy.py data=abalone3.arff storage=sqlite db=/tmp/paje iter=10 seed=123
    deactivate 


    
