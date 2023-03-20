# Train model
python train.py -o train_test -d data/train_sample1.csv,data/train_sample2.csv -n 268,268 -e 5 -s 101

# Prediction based on this training
python predict.py -o pred_test -m train_test -d data/predict_sample1.csv -n 268