import mlflow
import mlflow.pyfunc
import joblib
import pandas as pd

class RFModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = joblib.load(context.artifacts["model"])

    def predict(self, context, model_input):
        if isinstance(model_input, dict):
            model_input = pd.DataFrame(model_input)
        return self.model.predict(model_input)

if __name__ == "__main__":
    mlflow.set_experiment("serve_model_experiment")

    with mlflow.start_run():
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=RFModel(),
            artifacts={
                "model": "C:\\monitoring-dan-serving\\membangun_model\\mlruns\\0\\6a19dbd62414d3b9d34020a66fa697c2\\artifacts\\model.htrf.joblib"
            }
        )
        run_id = mlflow.active_run().info.run_id
        print(f"Logged model to runs:/{run_id}/model")