import os
import mlflow
import psutil
import seaborn as sns
import matplotlib.pyplot as plt
import typing as tp
from torch import Tensor
from TakeSentimentAnalysis import model


def save_metrics(confusion_matrix: Tensor, labels: list) -> None:
    """Receive a confusion matrix from tensor,
    calculates desirable metrics and log in mlflow experiment

    Parameters
    ----------
    confusion_matrix: torch.Tensor
        Tensor of confusion matrix
    labels: list
        Classification labels
    """
    precision = confusion_matrix.diag() / confusion_matrix.sum(dim=0)
    recall = confusion_matrix.diag() / confusion_matrix.sum(dim=1)
    f1_score = 2*(precision*recall / (precision + recall))

    for index, label in enumerate(labels):
        mlflow.log_metric(label + ' Precision',
                          precision[index].numpy().item())
        mlflow.log_metric(label + ' Recall', recall[index].numpy().item())
        mlflow.log_metric(label + ' F1-score', f1_score[index].numpy().item())

    mlflow.log_metric('Model Precision',
                      precision[precision >= 0].mean().numpy().item())
    mlflow.log_metric(
        'Model Recall', recall[recall >= 0].mean().numpy().item())
    mlflow.log_metric('Model F1-score',
                      f1_score[f1_score >= 0].mean().numpy().item())


def save_confusion_matrix_from_tensor(confusion_matrix: Tensor, labels: list,
                                      current_epoch: int, save_dir: str) -> None:
    """Receive a confusion matrix from tensor, generate a image
    with seaborn and save as .png in mlflow experiment

    Parameters
    ----------
    confusion_matrix: torch.Tensor
        Tensor of confusion matrix
    labels: list
        Classification labels
    current_epoch: int
        Current epoch number
    save_dir: str
        Directory to save
    """
    image_file_name = 'confusion_matrix_validation_{}.png'.format(
        current_epoch)
    plt.figure(figsize=(16, 10))
    matrix = sns.heatmap(confusion_matrix.long().numpy(), annot=True,
                         cmap=plt.cm.Blues, xticklabels=labels,
                         yticklabels=labels, fmt='d')
    plt.yticks(rotation=0)
    plt.savefig(os.path.join(save_dir, image_file_name))
    mlflow.log_artifact(os.path.join(
        save_dir, image_file_name), artifact_path="images")


def save_param(name: str, variable: tp.Union[int, float]):
    """Save parameter in mlflow experiment

    Parameters
    ----------
    name: str
        Name to log on mlflow
    variable: Union[int, float]
        Variable that is going to be logged
    """
    mlflow.log_param(name, variable)


def save_model(model: model.LSTM, model_name: str) -> None:
    """Save model as artifact in mlflow experiment

    Parameters
    ----------
    model: model.LSTM
        Trained LSTM model on pytorch
    model_name: str
        Name of the saved model
    """
    mlflow.sklearn.log_model(model, artifact_path='models',
                             registered_model_name=model_name)


def save_system_metrics():
    """Log system metrics in mlflow experiment
    """
    mlflow.log_metric('cpu_percent', float(psutil.cpu_percent()))
    mlflow.log_metric('memory_percent', float(psutil.virtual_memory().percent))


def save_metric(name: str, variable: tp.Union[int, float]):
    """Save metric in mlflow experiment

    Parameters
    ----------
    name: str
        Name to log on mlflow
    variable: Union[int, float]
        Variable that is going to be logged
    """
    mlflow.log_metric(name, variable)
