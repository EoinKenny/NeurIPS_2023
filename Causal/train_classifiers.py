import data_utils
import trainers

import numpy as np
import torch
import utils


def train(dataset, trainer, model, train_epochs, lambd, random_seed, learning_rate=0.01, verbose=True, tb_folder=None,
          save_dir=None, save_freq=10000):
    # For the TensorBoard logs
    if tb_folder is not None:
        tb_folder += utils.get_tensorboard_name(dataset, trainer, lambd, model, train_epochs, learning_rate, random_seed)

    # Set the relevant random seeds
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)

    # Load the relevant dataset
    X, Y, constraints = data_utils.process_data(dataset)
    X_train, Y_train, X_test, Y_test = data_utils.train_test_split(X, Y)

    actionable = constraints['actionable']
    # Load the relevant model
    if model == 'lin':
        model = trainers.LogisticRegression(X_train.shape[-1], allr_reg=trainer == 'ALLR',
                                            actionable_features=actionable, actionable_mask=trainer == 'AF')
    else:
        model = trainers.MLP(X_train.shape[-1], actionable_mask=trainer == 'AF', actionable_features=actionable)

    if trainer == 'ROSS':
        actionable_mask = np.zeros(X.shape[1])
        actionable_mask[actionable] = 1.
        trainer = trainers.Ross_Trainer(0.75, lambd, actionable_mask, lr=learning_rate, lambda_reg=lambd,
                                        verbose=verbose, tb_folder=tb_folder, save_dir=save_dir, save_freq=save_freq)
    elif trainer[:4] == 'ALLR':
        if model == 'lin':
            trainer = trainers.ERM_Trainer(lr=learning_rate, verbose=verbose, tb_folder=tb_folder, lambda_reg=lambd,
                                           save_dir=save_dir, save_freq=save_freq)
        else:
            actionable_mask = np.ones(X.shape[1])
            actionable_mask[actionable] = 0.  # we mask the ones that are actionable!
            mu2 = 3.
            if len(trainer) > 4:
                lambd = 0. if trainer[-1] == '0' else lambd
                mu2 = 0. if trainer[-1] == '1' else mu2
            trainer = trainers.LLR_Trainer(0.1, mu=lambd, lambd=mu2, verbose=verbose, reg_loss=False, grad_penalty=2,
                                           gradient_mask=actionable_mask, lr=learning_rate, use_abs=True,
                                           tb_folder=tb_folder, save_dir=save_dir, save_freq=save_freq)
    else:
            trainer = trainers.ERM_Trainer(lr=learning_rate, verbose=verbose, tb_folder=tb_folder, save_dir=save_dir,
                                           save_freq=save_freq)

    # Train!
    return trainer.train(model, X_train, Y_train, X_test, Y_test, train_epochs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, choices=['compas', 'bail', 'adult', 'german', 'loan'])
    parser.add_argument('--model', type=str, default='lin', choices=['lin', 'mlp'])
    parser.add_argument('--trainer', type=str, default='ERM', choices=['ERM', 'ALLR', 'AF', 'ROSS'])
    parser.add_argument('--epochs', type=int)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--tbfolder', type=str, default='exps/')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--lambd', type=float, default=0.5)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--save_model', action='store_true')
    parser.add_argument('--save_freq', type=int, default=10000)

    args = parser.parse_args()

    train(args.dataset, args.trainer, args.model, args.epochs, args.lambd, args.seed, args.lr, args.verbose,
          args.tbfolder, args.save_model, args.save_freq)
