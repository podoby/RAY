from mistralai import Mistral
import os
import time
from pathlib import Path

API_KEY = os.environ["MISTRAL_API_KEY"]
BASE_MODEL = "ministral-3b-latest"

client = Mistral(api_key=API_KEY)


def upload_file(path: str):
    return client.files.upload(
        file={
            "file_name": Path(path).name,
            "content": open(path, "rb"),
        }
    )


def main():
    print("Uploading training dataset chunks...")
    training_files = []

    for path in Path("finetune/chunks").glob("train_part_*.jsonl"):
        uploaded = upload_file(str(path))
        print(f"Uploaded {path.name} → {uploaded.id}")

        training_files.append({
            "file_id": uploaded.id,
            "weight": 1
        })

    print("Uploading validation dataset...")
    validation_data = upload_file("finetune/valid.jsonl")
    print("Validation file ID:", validation_data.id)

    print("Creating fine-tuning job...")
    job = client.fine_tuning.jobs.create(
        model=BASE_MODEL,
        training_files=training_files,
        validation_files=[validation_data.id],
        hyperparameters={
            "training_steps": 50,
            "learning_rate": 5e-5
        },
        auto_start=True
    )

    print("Job created:", job.id)

    while True:
        status = client.fine_tuning.jobs.get(job_id=job.id)
        print("Status:", status.status)

        if status.status in ["succeeded", "failed"]:
            break

        time.sleep(20)

    if status.status == "succeeded":
        print("Fine-tuning completed successfully!")
        print("Fine-tuned model:", status.fine_tuned_model)
    else:
        print("Fine-tuning failed.")


if __name__ == "__main__":
    main()