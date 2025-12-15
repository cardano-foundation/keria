FROM weboftrust/keria:0.2.0-dev6

RUN sed -i 's/verify=True/verify=False/g' /keria/venv/lib/python3.12/site-packages/keri/core/serdering.py
