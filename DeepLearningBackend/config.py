import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Data set locations
eur_usd_loc = "EURUSD_15m_BID_01.01.2010-31.12.2016.csv"

# trained model locations
bi_rnn_weights = "bi_rnn_trained_models/weights.best.hdf5"
