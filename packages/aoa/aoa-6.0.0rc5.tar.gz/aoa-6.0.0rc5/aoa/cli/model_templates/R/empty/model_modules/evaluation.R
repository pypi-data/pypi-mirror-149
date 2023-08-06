library(methods)
library(gbm)
library(jsonlite)
library(caret)


evaluate <- function(data_conf, model_conf, ...) {
  model <- readRDS("artifacts/input/model.rds")

  # implement evaluation

  # write(jsonlite::toJSON(metrics, auto_unbox = TRUE, null = "null", keep_vec_names=TRUE), "artifacts/output/metrics.json")
}
