import asyncio
import boto3

from app.database import AsyncSessionLocal
from app.models import ServiceReport

BUCKET_NAME = "agricore-diagnostics-jac2478"
LOCAL_FILE_PATH = "scripts/journal-entry-2.txt"

S3_KEY = "diagnostics/barn_update1.txt"

#a function to upload the file to the s3 bucket and return the s3 url
def upload_to_s3() -> str:
    s3_client = boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
    return f"s3://{BUCKET_NAME}/{S3_KEY}"

async def record_service_report(file_url: str) -> None:
    async with AsyncSessionLocal() as session:
        log = ServiceReport(
            field_job_id=1,
            file_url=file_url,
            notes="Some one needs to clean the barn...",
        )
        session.add(log)
        await session.commit()
        await session.refresh(log)
        print(f"Created ServiceReport: id={log.id}, file_url={log.file_url}")

async def main() -> None:
    file_url = upload_to_s3()
    print(f"Uploaded to {file_url}")
    await record_service_report(file_url)

if __name__ == "__main__":
    asyncio.run(main())
