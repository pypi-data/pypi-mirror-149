class Helper:

  @staticmethod
  def concatenate_metrics (metrics: list) -> str:
    return '\n'.join([ Helper.concatenate_metrics(metric) if type(metric) == list else str(metric) for metric in metrics ])

  @staticmethod
  def concatenate_metrics_arrays (metrics: list) -> list:
    if metrics == []: return metrics
    if isinstance(metrics[0], list): return Helper.concatenate_metrics_arrays(metrics[0]) + Helper.concatenate_metrics_arrays(metrics[1:])
    return metrics[:1] + Helper.concatenate_metrics_arrays(metrics[1:])
