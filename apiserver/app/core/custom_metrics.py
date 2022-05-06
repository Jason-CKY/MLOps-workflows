from typing import Callable
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Gauge

def model_metrics_precision() -> Callable[[Info], None]:
    METRIC = Gauge('model_metrics_precision', 'Model Precision')

    def instrumentation(info: Info) -> None:
        METRIC.set("0.988")
    
    return instrumentation

def model_metrics_recall() -> Callable[[Info], None]:
    METRIC = Gauge('model_metrics_recall', 'Model Recall')

    def instrumentation(info: Info) -> None:
        METRIC.set("0.56")
    
    return instrumentation

def model_metrics_f1() -> Callable[[Info], None]:
    METRIC = Gauge('model_metrics_f1', 'Model F1 Score')

    def instrumentation(info: Info) -> None:
        METRIC.set("0.12")
    
    return instrumentation
