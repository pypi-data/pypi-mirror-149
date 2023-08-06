library(methods)
library(gbm)
library(jsonlite)
library(caret)

initialise_model <- function() {
    print("Loading model...")
    model <- readRDS("artifacts/input/model.rds")
}

score.restful <- function(model, data, ...) {
    print("Scoring model...")

    # implement if restful model serving
}

score.batch <- function(data_conf, model_conf, model_version, ...) {
    print("Batch scoring model...")

    # implement if batch scoring

}